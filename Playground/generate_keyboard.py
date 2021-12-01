from tkinter import *
import tkinter as tk

def select(value,entry):
    if value == "<-":
        entry2 = entry.get()
        pos = entry2.find("")
        pos2 = entry2[:-1]
        entry.delete(0 ,tk.END)
        entry.insert(0, pos2)
    elif value == "Space":
        entry.insert(tk.END, ' ')
    elif value == "Tab ":
        entry.insert(tk.END, '    ')
    else:
        entry.insert(tk.END,value)


def create_letterpad(f_frame, entry):

    btn_list = [['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '<-'], 
    ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'],  
    ['z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.'],
    ['Space']]

    row1, row2, row3, row4 = None, None, None, None
    row_frame_list = [row1, row2, row3, row4]
    for i in range(len(row_frame_list)):
        row_frame_list[i] = tk.Frame(f_frame)
        row_frame_list[i].grid(row=i+1) # row 0 is for the textbox

        for b in btn_list[i]:
            column = btn_list[i].index(b)
            command = lambda value=b: select(value,entry)
            if b == "Space":
                b = tk.Button(row_frame_list[i], text=b, width=12, height=2, command=command, bg='#C0C0C0', fg='black',
                          font=('Calibri', 27)).grid(
                row=i,
                column=column,
                padx=6,
                pady=13)
            else:
                b = tk.Button(row_frame_list[i], text=b, width=3, height=2, command=command, bg='#C0C0C0', fg='black',
                          font=('Calibri', 26)).grid(
                row=i,
                column=column,
                padx=6,
                pady=13)