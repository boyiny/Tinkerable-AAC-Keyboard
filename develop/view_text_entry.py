from os import system
import tkinter as tk
from tkinter import ttk

class View_text_edit:
    
    BOOL_ENTRY_BY_KEYWORDS = False

    def __init__(self):
        self.previousEntry = ''
        self.entry = ''
        self.prediction = ''

    def edit_text_letter(self, caption):
        if caption == "<-":
            self.previousEntry = self.entry
            self.entry = self.entry[:-1]
        elif caption == "Space":
            self.entry = self.entry + ' '
        elif caption == "Tab":
            self.entry = self.entry + '    '
        elif caption == "Speak":
            system(f'say {self.entry}')
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


    def conversation_partner_input_kwickchat(self, recgnisedSpeech):
        self.root = tk.Tk()
        self.root.title("Speaking partner")

        baseFrame = ttk.Frame(self.root)
        baseFrame.pack(padx=5, pady=5)
        
        rs = tk.StringVar(baseFrame, recgnisedSpeech)
        partnerInput = tk.Entry(baseFrame, width=50, textvariable=rs, font='Calibri 18')
        partnerInput.pack(padx=5, pady=15, expand=True)

        cancelBtn = ttk.Button(baseFrame, text="Cancel", command=None)
        cancelBtn.pack(padx=5, pady=15, side=tk.RIGHT)

        confirmBtn = ttk.Button(baseFrame, text="Confirm", command=None)
        confirmBtn.pack(padx=5, pady=15, side=tk.RIGHT)

        self.root.mainloop() 

if __name__ == '__main__':
    view = View_text_edit()
    view.conversation_partner_input_kwickchat("How are you")