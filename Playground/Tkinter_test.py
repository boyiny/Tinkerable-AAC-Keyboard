# import PySimpleGUI as sg
# sg.Window(title="Hello World", layout=[[]], margins=(100, 50)).read()
from tkinter import *
import tkinter as tk

# from tkinter.dnd import Tester as DragWindow, Icon as Dragable

from generate_keyboard import *



Keyboard_App = tk.Tk()
Keyboard_App.title("Tkinter Onscreen Keyboard")
Keyboard_App.resizable()
# Keyboard_App.grid_rowconfigure(0, weight=1)
# Keyboard_App.grid_columnconfigure(0, weight=1)

# frame = DnDFrame(Keyboard_App, bd=4, bg="grey")
# frame.place(x=10, y=10)
# make_draggable(frame)

# notes = tk.Text(frame)
# notes.pack()

# textFrame = DnDFrame(Keyboard_App, bd=4)
entry = Entry(Keyboard_App, width=110, font=('Calibri', 18))
entry.grid(row=0, columnspan=15)

create_letterpad(Keyboard_App,entry)



Keyboard_App.mainloop()