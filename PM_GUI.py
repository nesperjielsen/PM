# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 15:14:31 2018

@author: jespe
"""

import tkinter as tk

class PM:
    
    def __init__(self, master):
        
        frame = tk.Frame(master)
        frame.pack()
    
        menu = self.menu = tk.Menu(master)
        root.config(menu=menu)
        filemenu = tk.Menu(menu)
        menu.add_cascade(label = "Options", menu = filemenu)
        filemenu.add_command(label = "Help", command = self.Help)
        filemenu.add_command(label = "Exit", command = frame.quit)
       
        quest_button = self.quest_button = tk.Button(text = "Quest", command = self.quest)
        quest_button.pack()
        
        event_button = self.event_button = tk.Button(text = "Event", command = self.event)
        event_button.pack()
        
            
    def Help(self):
        top = self.top = tk.Toplevel()
        
        label = tk.Label(top, text = "Welcome to the pointmaster program! \n Press the corresponding button to the type of point you want to give to the teams \n"
                         "For example, if you want to add a quest, press that button and input the team and amount of points given in the right box \n")
        
        label.pack()
    
    def quest(self):
        
        win = tk.Toplevel()
        win.wm_title("Quest")
        
        team = self.team = tk.Label(win, text = "Team: ")
        team.grid(row = 0)
        
        points = self.points = tk.Label(win, text = "Points")
        points.grid(row = 1)
        
        self.teamname = tk.Entry()
        self.points = tk.Entry()
        
        self.teamname.grid(row = 0, column = 1)
        self.points.grid(row = 1, column = 1)
        
        
    def event(self):
        print("Sup")

root = tk.Tk()

app = PM(root)

root.title("PM")
root.mainloop()