import tkinter as tk

class Model_main:
    def __init__(self):
        self.previousEntry = ''
        self.entry = ''
        

    def edit_text(self, caption):
        if caption == "<-":
            self.previousEntry = self.entry
            self.entry = self.entry[:-1]
        elif caption == "Space":
            self.entry = self.entry + ' '
        elif caption == "Tab":
            self.entry = self.entry + '    '
        elif caption == "Speak":
            pass
        elif caption == "Clear All":
            self.entry = ''
            self.previousEntry = ''
        else:
            self.entry = self.entry + caption

        return self.entry



# def _on_button_click(self, button, entry):
#         # result = self.modelMain
#         if button == "<-":
#             entry2 = entry.get()
#             pos = entry2[:-1]
#             entry.delete(0 ,tk.END)
#             entry.insert(0, pos)
#         elif button == "Space":
#             entry.insert(tk.END, ' ')
#         elif button == "Tab ":
#             entry.insert(tk.END, '    ')
#         elif button == "Speak":
#             pass
#         elif button == "Clear All":
#             entry.delete(0,tk.END)
#         else:
#             entry.insert(tk.END,button)
#         # print(f'Button {caption} is clicked')