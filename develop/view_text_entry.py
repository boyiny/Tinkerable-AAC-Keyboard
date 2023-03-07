from os import system
import tkinter as tk
from tkinter import ttk


class View_text_edit:
    
    BOOL_ENTRY_BY_KEYWORDS = False

    def __init__(self, controller):
        self.previousEntry = ''
        self.entry = ''
        self.prediction = ''
        self.controller = controller

    def edit_text_letter(self, caption):
        if caption == "<-":
            self.previousEntry = self.entry
            self.entry = self.entry[:-1]
        elif caption == "Space":
            self.entry = self.entry + ' '
        elif caption == "Tab":
            self.entry = self.entry + '    '
        elif caption == "Speak":
            # system(f'say {self.entry}')
            self.controller.speak_text(self.entry)
            self.entry = ''
        elif caption == "Clear All":
            self.entry = ''
            self.previousEntry = ''
        else:
            """ Caption is a letter """
            if self.entry == "":
                """ Blank textbox """
                self.entry = self.entry + caption.upper()
                    # self.entry = self.entry + caption[0].upper() + caption[1:]
            else:
                """ Textbox has content """
                if caption == "," or caption == "." or caption == "?" or caption == "!":
                    if self.entry[-1] == " ":
                        self.entry = self.entry[0:-1] + caption
                    else:
                        self.entry = self.entry + caption
                else:
                    self.entry = self.entry + caption

        return self.entry


    def edit_text_word(self, caption):
        """ Caption is a word prediction """
        if caption[0] == "'":
            self.entry = self.entry + caption
        else:
            if self.entry == "":
                """ Blank textbox """
                self.entry = self.entry + caption[0].upper() + caption[1:]
            else:
                """ Textbox has content """
                if self.entry[-1] == " ":
                    """ A word is finished """
                    self.entry = self.entry + caption
                else:
                    """ A word is not finished """
                    wordList = self.entry.split()
                    lastWord = wordList[-1]
                    indexOfLastWord = self.entry.rfind(lastWord) 
                    self.entry = self.entry[0:indexOfLastWord] + caption
        
        return self.entry

    def edit_text_sentence(self, caption):
        """ Caption is a sentence prediction """
        if self.BOOL_ENTRY_BY_KEYWORDS:
            self.entry = caption
            self.entry = self.entry[0].upper() + self.entry[1:]
        else:
            if self.entry == "":
                """ Blank textbox """
                self.entry = self.entry + caption[0].upper() + caption[1:]
            elif " " not in self.entry:
                self.entry = caption[0].upper() + caption[1:]
            else:
                """ Textbox has content """
                # entryWordList = self.entry.split()
                captionWordList = caption.split()
                captionFirstWord = captionWordList[0]
                indexOfFirstWordOfCaptionInEntry = self.entry.lower().rfind(captionFirstWord.lower())
                self.entry = self.entry[0:indexOfFirstWordOfCaptionInEntry] + caption
                self.entry = self.entry[0].upper() + self.entry[1:] + " "

        return self.entry

    def _close(self):
        self.root.destroy()

    def _confirm(self):
        print(f"partnerInput is {self.partnerInput.get()}")
        self.controller.modelLogData.record_conversation_partner_input(self.partnerInput.get())
        self.controller.add_conv_partner_input_to_history(self.partnerInput.get())
        self.root.destroy()

    def _recognize(self):
        self.controller.recognize_speech()

    def pop_up_conv_partner_window_kwickchat(self):
        self.root = tk.Tk()
        self.root.title("Speaking partner")

        self.baseFrame = ttk.Frame(self.root)
        self.baseFrame.pack(padx=5, pady=5)
        
        rs = tk.StringVar(self.baseFrame, '')
        self.partnerInput = tk.Entry(self.baseFrame, width=50, textvariable=rs, font='Calibri 18')
        self.partnerInput.pack(padx=5, pady=15, expand=True)

        cancelBtn = ttk.Button(self.baseFrame, text="Cancel", command=self._close)
        cancelBtn.pack(padx=5, pady=15, side=tk.RIGHT)

        confirmBtn = ttk.Button(self.baseFrame, text="Confirm", command=self._confirm)
        confirmBtn.pack(padx=5, pady=15, side=tk.RIGHT)

        recognizeBtn = ttk.Button(self.baseFrame, text="Recognize", command=self._recognize)
        recognizeBtn.pack(padx=5, pady=15, side=tk.LEFT)

        # self.root.mainloop() 


    def show_conversation_partner_input_kwickchat(self, recgnisedSpeech):
        rs = tk.StringVar(self.baseFrame, recgnisedSpeech)
        self.partnerInput.config(textvariable=rs)
        self.root.update()



        

if __name__ == '__main__':
    view = View_text_edit()
    view.show_conversation_partner_input_kwickchat("How are you")