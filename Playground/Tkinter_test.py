# import PySimpleGUI as sg
# sg.Window(title="Hello World", layout=[[]], margins=(100, 50)).read()
from tkinter import *
import tkinter as tk
from tkinter.dnd import Tester as DragWindow, Icon as Dragable


from generate_keyboard import Generate_key, Generate_menu



Keyboard_App = tk.Tk()

Keyboard_App.title("Tkinter Onscreen Keyboard")
Keyboard_App.resizable()
Keyboard_App.geometry("1500x1000")
# Keyboard_App.grid_rowconfigure(0, weight=1)
# Keyboard_App.grid_columnconfigure(0, weight=1)

# frame = DnDFrame(Keyboard_App, bd=4, bg="grey")
# frame.place(x=10, y=10)
# make_draggable(frame)

# notes = tk.Text(frame)
# notes.pack()

# textFrame = DnDFrame(Keyboard_App, bd=4)


Generate_menu.create_menu(Keyboard_App)


# createTextbox()

entry = Entry(Keyboard_App, font=('Calibri', 18))
entry.place(height=50, width=1100, x=20, y=10)

letterPad = Generate_key()
letterPad.create_letterpad(Keyboard_App,entry)



Keyboard_App.mainloop()