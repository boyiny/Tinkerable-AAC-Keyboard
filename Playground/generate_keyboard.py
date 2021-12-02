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


def create_letterpad(root_frame, entry):

    keyList = [['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '<-'], 
    ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'],  
    ['z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.'],
    ['Space']]

    row1, row2, row3, row4 = None, None, None, None
    rowFrameList = [row1, row2, row3, row4]
    keyIndex = 0
    keyFrameList = []
    for i in range(len(rowFrameList)):
        rowFrameList[i] = DnDFrame(root_frame)
        # wordPred = tk.Text(rowFrameList[i], 'pred', bd=4, bg="grey", )
        # wordPred.grid(row=i+1) # row 0 is for the textbox
        
        for keyChar in keyList[i]:
            column = keyList[i].index(keyChar)
            command = lambda value=keyChar: select(value,entry)
            keyFrameList.append(DnDFrame(root_frame))
            if (i<1):
                keyFrameList[keyIndex].grid(row=i+1, column=column)
            else:
                keyFrameList[keyIndex].grid(row=i+1, column=column+1)
            
            if keyChar == "Space":
                
                keyBtn = tk.Button(keyFrameList[keyIndex], text=keyChar, width=12, height=2, command=command, bg='#C0C0C0', fg='black',
                          font=('Calibri', 26)).grid(
                row=i,
                column=column+3,
                padx=10,
                pady=10)
                # keyChar.grid_rowconfigure(1, weight=1)
                
            else:
                keyBtn = tk.Button(keyFrameList[keyIndex], text=keyChar, width=3, height=2, command=command, bg='#C0C0C0', fg='black',
                          font=('Calibri', 26)).grid(
                row=i,
                column=column,
                padx=10,
                pady=10)

            keyBtn

            keyIndex+=1
         

# Make the widget draggable
def make_draggable(widget):
    widget.bind("<Button-1>", on_drag_start)
    widget.bind("<B1-Motion>", on_drag_motion)

def on_drag_start(event):
    widget = event.widget
    widget._drag_start_x = event.x
    widget._drag_start_y = event.y

def on_drag_motion(event):
    widget = event.widget
    x = widget.winfo_x() - widget._drag_start_x + event.x
    y = widget.winfo_y() - widget._drag_start_y + event.y
    widget.place(x=x, y=y)

class DragDropMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        make_draggable(self)

class DnDFrame(DragDropMixin, tk.Frame):
    pass