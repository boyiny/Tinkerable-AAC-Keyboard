# import PySimpleGUI as sg
# sg.Window(title="Hello World", layout=[[]], margins=(100, 50)).read()
from tkinter import *
import tkinter as tk

from generate_keyboard import *

Keyboard_App = tk.Tk()
Keyboard_App.title("Tkinter Onscreen Keyboard")
Keyboard_App.resizable(0,0)


entry = Entry(Keyboard_App, width=110, font=('Calibri', 18))
entry.grid(row=0, columnspan=15)

create_letterpad(Keyboard_App,entry)



Keyboard_App.mainloop()