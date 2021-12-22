# import tkinter as tk

class Model_main:
    wordPredTest = ['hey', 'hello', 'have', 'has', 'happy', 'happen']

    def __init__(self):
        self.previousEntry = ''
        self.entry = ''
        self.prediction = ''
        

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
    
    def set_drag(self, boolDrag):
        return boolDrag
    
    """ Word prediction below """
    def set_bool_word_pred(self, bool):
        return bool
        
    def set_word_pred_num(self, num):
        return num

    def set_word_pred_on_last_pressed_key(self, bool):
        return bool


    def make_word_prediction(self, entry):
        return self.wordPredTest

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