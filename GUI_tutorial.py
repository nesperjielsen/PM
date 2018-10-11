# -*- coding: utf-8 -*-
"""
Created on Tue Oct  9 15:39:51 2018

@author: jespe
"""

import tkinter as tk
#Create buttons
'''
class App:
    
    def __init__(self, master):
        
        frame = tk.Frame(master)
        frame.pack()
        
        self.hi = tk.Button(frame, text="Hello", fg ="blue", command=self.hi)
        self.hi.pack(side=tk.LEFT)
        
        self.button = tk.Button(frame, text = "Quit", fg = "red", command=frame.quit)
        self.button.pack(side=tk.LEFT)
    
    def hi(self):
        print("Hello")

root = tk.Tk()

app = App(root)

root.mainloop()
'''
#capture mouse clicks
'''
root = tk.Tk()

def callback(event):
    print("clicked at", event.x, event.y)

frame = tk.Frame(root, width = 100, height = 100)
frame.bind("<Button-1>", callback)
frame.pack()

root.mainloop()
'''
#Capture keyboard presses
'''
root = tk.Tk()

def key(event):
    print("pressed", repr(event.char))

def callback(event):
    frame.focus_set()
    print("clicked at", event.x, event.y)

frame = tk.Frame(root, width=100, height=100)
frame.bind("<Key>", key)
frame.bind("<Button-1>", callback)
frame.pack()

root.mainloop()
'''
#Creating menu

def callback():
    print("called the callback!")

root = tk.Tk()

menu = tk.Menu(root)
root.config(menu = menu)
frame = tk.Frame(root, width = 100, height = 100)

filemenu = tk.Menu(menu)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="New", command=callback)
filemenu.add_command(label="Open...", command=callback)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=frame.quit)

helpmenu = tk.Menu(menu)
menu.add_cascade(label = "Help", menu=helpmenu)
helpmenu.add_command(label="About...", command=callback)

tk.mainloop()

#Creating a toolbar
'''
root = tk.Tk()

def callback():
    print("Called the callback!")
    
toolbar = tk.Frame(root)

b = tk.Button(toolbar, text = "new", width=6, command = callback)
b.pack(side=tk.LEFT, padx = 2, pady = 2)

b = tk.Button(toolbar, text = "Open", width = 6, command = callback)
b.pack(side = tk.LEFT, padx = 2, pady = 2)

toolbar.pack(side = tk.TOP, fill = tk.X)

tk.mainloop()
'''
#Creating a dialog
'''
class MyDialog:
    
    def __init__(self, parent):
        
        top = self.top = tk.Toplevel(parent)
        
        tk.Label(top, text = "Value").pack()
        
        self.e = tk.Entry(top)
        self.e.pack(padx = 5)
        
        b = tk.Button(top, text = "Value", command=self.ok)
        b.pack(pady=5)
        
    def ok(self):
        
        print("value is", self.e.get())

        self.top.destroy()

root = tk.Tk()
tk.Button(root, text = "Hello").pack()
root.update()

d = MyDialog(root)

root.wait_window(d.top)
'''
