import datetime
import os
import paramiko
import getpass
import pandas as pd
import matplotlib.pyplot as plt

def add_quest(quest_number,quest_owner,bonus_points):
        qu_types = {"quest_number":int, "quest_description":str, "quest_value":int, "quest_repeat":str, "quest_owner":str}
        da_types = {"time":str, "quest_number":int, "quest_value":int, "bonus":int, "pitty_points":int, "glufs":int, "bol":int, "lemur":int, "snys":int}
        quests = pd.read_csv("quest_list.csv", encoding="utf8", delimiter=";", header=0, dtype=qu_types)
        data = pd.read_csv("data.csv", encoding="utf8", delimiter=";", header=0, dtype=da_types)
        
        #Gets the quest value from the quest list
        quest_number=int(quest_number)
        bonus_points=int(bonus_points)
        quest_value = int(quests["quest_value"].loc[quests['quest_number'] == quest_number])
        quest_owner_onfile = quests.loc[quests['quest_number'] == quest_number,'quest_owner'].values[0]
        quest_repeat_onfile = quests.loc[quests['quest_number'] == quest_number,'quest_repeat'].values[0]

        #If the quest already has an owner and it cannot be repeated multiple times:
        if(quest_owner_onfile != "none" and
            quest_repeat_onfile == "single"):
                print("This quest has been taken")
                pitty_points = int(input("Pitty Point >>> "))
                quest_value=0
                bonus_points=0
                #quest_owner=quests.loc[quests['quest_number'] == quest_number,'quest_owner'].values[0]
        else:
                pitty_points = 0
                #Only update the quest owner when the quest is done for the first time
                quests.loc[quests['quest_number'] == quest_number, "quest_owner"] = quest_owner
                quests.to_csv("quest_list.csv", header=True, index=False, sep=";")
                
        new_score = {"time":datetime.datetime.now(),
                   "quest_number":quest_number,
                   "quest_value":quest_value,
                   "bonus":bonus_points,
                   "pitty_points":pitty_points,
                   "glufs":0,
                   "bol":0,
                   "lemur":0,
                   "snys":0}

        new_score[quest_owner]=quest_value+bonus_points+pitty_points
        data = data.append(new_score, ignore_index=True)
        data.to_csv("data.csv", header=True, index=False, sep=";")
        
        

def add_event(number_of_entries):
        da_types = {"time":str, "quest_number":int, "quest_value":int, "bonus":int, "pitty_points":int, "glufs":int, "bol":int, "lemur":int, "snys":int}
        data = pd.read_csv("data.csv", encoding="utf8", delimiter=";", header=0, dtype=da_types)
        i=0
        while i<number_of_entries:
                new_score = {"time":datetime.datetime.now(),
                   "quest_number":0,
                   "quest_value":0,
                   "bonus":0,
                   "pitty_points":0,
                   "glufs":0,
                   "bol":0,
                   "lemur":0,
                   "snys":0}
                
                entry=input("Enter <TeamName Points>\n")
                if(entry.split(" ")[0]=="glufs"
                           or entry.split(" ")[0]=="bol"
                           or entry.split(" ")[0]=="lemur"
                           or entry.split(" ")[0]=="snys"):
                        entry_owner=entry.split(" ")[0]
                        entry_points=entry.split(" ")[1]
                        new_score[entry_owner]=entry_points

                        data = data.append(new_score, ignore_index=True)
                        data.to_csv("data.csv", header=True, index=False, sep=";")
                        i+=1
                elif entry.split(" ")[0] == 'exit':
                    i=number_of_entries                    
                else:
                        print("Not valid team name")
            
def generate_html():

        with open("quest_list.csv",'r', encoding="utf8") as f,open("list.html",'a', encoding="utf8") as html_file:
                open("list.html", 'w', encoding="utf8").close()
                f.readline()
                for row in f:
                        split_row=row.split(";")
                        quest_owner=split_row[4][:-1]

                        color="Black"
                        repetition=""
                        if(split_row[3]=="multiple"):
                                repetition=" (Can be done multiple times!)"
                        if(quest_owner != 'none' and split_row[3]!="multiple"):
                                if(quest_owner=="glufs"):
                                        color="Turquoise"
                                elif(quest_owner=="bol"):
                                        color="Purple"
                                elif(quest_owner=="snys"):
                                        color="Orange"
                                elif(quest_owner=="lemur"):
                                        color="red"
                                line = '<p style="color: ' + color + ';"><strike>' +  split_row[0]+": "+split_row[1] + " " + split_row[2] + "p" + repetition +'</strike></p>'
                        else:
                                line = '<p>' + split_row[0]+": "+split_row[1] + " " + split_row[2] + "p"+ repetition + '</p>'
                        html_file.write(line)
                
def upload():
        generate_html()
        make_plot()
        ssh = paramiko.SSHClient() 
        ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
        password=getpass.getpass("Password: ")
        ssh.connect("ssh.binero.se", username="200351_nycklis", password=password)
        sftp = ssh.open_sftp()
        sftp.put("list.html", "/storage/content/51/200351/lundsnaturvetarkar.se/public_html/nycklistest1.html")
        sftp.put("Figure_1.png", "/storage/content/51/200351/lundsnaturvetarkar.se/public_html/novisch_standings.png")
        sftp.close()
        ssh.close()

def make_plot():
        with open("data.csv",'r', encoding="utf8") as f:
                f.readline()
                sum_list=[[],[],[],[]]
                time_list=[]
                i=0
                for row in f:
                        row_split = row.split(";")

                        glufs_entry = int(row_split[5])
                        bol_entry = int(row_split[6])
                        lemur_entry = int(row_split[7])
                        snys_entry = int(row_split[8])
                        time_entry = row_split[0]

                        if i==0:
                                sum_list[0].append(glufs_entry)
                                sum_list[1].append(bol_entry)
                                sum_list[2].append(lemur_entry)
                                sum_list[3].append(snys_entry)
                        else:
                                sum_list[0].append(glufs_entry+sum_list[0][i-1])
                                sum_list[1].append(bol_entry+sum_list[1][i-1])
                                sum_list[2].append(lemur_entry+sum_list[2][i-1])
                                sum_list[3].append(snys_entry+sum_list[3][i-1])

                        time_list.append(time_entry)
                        i=i+1
        
        day0=int(time_list[0].split(" ")[0].split("-")[1])*30+int(time_list[1].split(" ")[0].split("-")[2])
        #print(day0)

        time_list_fake=[]
        for entry in time_list:
                #hours
                time_list_fake.append((int(entry.split(" ")[0].split("-")[1])*30+int(entry.split(" ")[0].split("-")[2]))*24+int(entry.split(" ")[1].split(":")[0])-day0*24+12)
                #days
                #time_list_fake.append((int(entry.split(" ")[0].split("-")[1])*30+int(entry.split(" ")[0].split("-")[2]))-day0)

        with plt.xkcd():
                fig = plt.figure()
                plt.plot(time_list_fake,sum_list[0],'xkcd:sky blue',label="GLuFS: "+str(sum_list[0][-1])+"p")
                plt.plot(time_list_fake,sum_list[1],'xkcd:violet',label="BÖÖL: "+str(sum_list[1][-1])+"p")
                plt.plot(time_list_fake,sum_list[2],'xkcd:red',label="LEMUR: "+str(sum_list[2][-1])+"p")
                plt.plot(time_list_fake,sum_list[3],'xkcd:yellow',label="SNYS: "+str(sum_list[3][-1])+"p")

                plt.legend()
                plt.xlabel('Time (hours after introductory meeting)')
                plt.ylabel('Awesomeness (points)')
 
                fig.text(0.5, 0.95,'Team Awesomeness vs Time',ha='center')
                fig.set_figheight(9)
                fig.set_figwidth(16)
                fig.savefig("Figure_1.png")
def score():
    with open("data.csv", "r", encoding="utf8") as f:
        f.readline()
        points=[[],[],[],[]]
        for row in f:
            row_split = row.split(";")
            
            glufs_entries = int(row_split[5])
            bol_entries = int(row_split[6])
            lemur_entries = int(row_split[7])
            snys_entries = int(row_split[8])
            
            points[0].append(glufs_entries)
            points[1].append(bol_entries)
            points[2].append(lemur_entries)
            points[3].append(snys_entries)

    glufs_points = sum(points[0])
    bol_points = sum(points[1])
    lemur_points = sum(points[2])
    snys_points = sum(points[3])

    print("GLuFS has:", glufs_points, "points \n","BÖÖL has:", bol_points, "points \n","LEMUR has:", lemur_points, "points \n","SNYS has:", snys_points, "points")

def reset():
        open("data.csv", 'w', encoding="utf8").write("time;quest_number;quest_value;bonus;pitty_points;glufs;bol;lemur;snys")
        with open("quest_list.csv",'r', encoding="utf8") as f:
                temp_list=[]
                header = f.readline()
                temp_list.append(header)
                for row in f:
                        string = row.split(";")[:-1][0]+";"+row.split(";")[:-1][1]+";"+row.split(";")[:-1][2]+";"+row.split(";")[:-1][3]+";none\n"
                        temp_list.append(string)
        open("quest_list.csv",'w', encoding="utf8").close()
        write_quest_list = open("quest_list.csv",'a', encoding="utf8")
        for element in temp_list:
                write_quest_list.write(str(element))
        write_quest_list.close()
        
def test():
########################
#glufs;bol;lemur;snys;
#170;117;172;118
########################
        reset()
        with open("alpha2.txt",'r', encoding="utf8") as f:
                for command in f:
                        if command.split()[0]=="q":
                                add_quest(command.split()[1],command.split()[2],command.split()[3])
                        elif command.split()[0]=="e":
                                add_event(int(command.split()[1]))
        score()
def main():
       #make_plot()
        command=input("Command: >>> ")
        while command!="exit":
                
                if command.split()[0]=="q":
                        if(command.split()[2]=="glufs"
                           or command.split()[2]=="bol"
                           or command.split()[2]=="lemur"
                           or command.split()[2]=="snys"):
                                try:
                                        add_quest(command.split()[1],command.split()[2],command.split()[3])
                                except KeyError:
                                        print("KeyError")
                                except IndexError:
                                        print("IndexError")
                        else:
                                print("Not valid team name")
                elif command.split()[0]=="e":
                        try:
                                add_event(int(command.split()[1]))
                        except KeyError:
                                print("KeyError")
                        except IndexError:
                                print("IndexError")
                        except ValueError:
                                print("ValueError")
                elif command.split()[0]=="upload":
                        try:
                                upload()
                        except KeyError:
                                print("KeyError")
                        except IndexError:
                                print("IndexError")
                elif command.split()[0]=="score":
                        try:
                                score()
                        except KeyError:
                                print("KeyError")
                        except IndexError:
                                print("IndexError")
                elif command.split()[0]=="reset":
                        ask = input("Do you really want to reset the data? [y/n] \n")
                        if ask == "y":
                            reset()
                        elif ask == "n":
                                print("Did not reset")
                        else:
                                print('Unknown command')
                elif command.split()[0]=="plot":
                        try:
                                make_plot()
                        except KeyError:
                                print("KeyError")
                        except IndexError:
                                print("IndexError")
                elif command.split()[0]=="test":
                        try:
                                test()
                        except KeyError:
                                print("KeyError")
                else:
                    print("Unknown command")
                command=input("Command: >>> ")
if __name__ == '__main__':
        #test()
        #reset()
        main()
