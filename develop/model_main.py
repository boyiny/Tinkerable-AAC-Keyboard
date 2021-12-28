import threading
from os import system
from model_bm25 import Model_Bm25
from model_gpt2 import Model_Gpt2
from model_roberta import Model_Roberta


class Model_main:
    wordPredTest = ['hey', 'hello', 'have', 'has', 'happy', 'happen']

    def __init__(self):
        self.previousEntry = ''
        self.entry = ''
        self.prediction = ''
        self.boolBm25 = False
        self.boolRoberta = False
        self.boolGpt2 = False
        self.wordPredNum = 4
        # self.speachEngine = pyttsx.init()
        
    # """ Speak below """
    # def _speak_text(self, text):
    #     self.speachEngine.say(text)
    #     self.speachEngine.runAndWait()
    # """ Speak above """

    """ Textbox below"""

    def edit_text(self, caption):
        if caption == "<-":
            self.previousEntry = self.entry
            self.entry = self.entry[:-1]
        elif caption == "Space":
            self.entry = self.entry + ' '
        elif caption == "Tab":
            self.entry = self.entry + '    '
        elif caption == "Speak":
            system(f'say {self.entry}')
            # self._speak_text(self.entry)
            # self.speachEngine.stop()
            # self.entry = ""
        elif caption == "Clear All":
            self.entry = ''
            self.previousEntry = ''
        else:
            if caption[-1] == " " and len(caption) > 1:
                """ Caption is a word prediction """
                # print(f"Caption is a word: {caption}")
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
                        indexOfLastWord = self.entry.find(lastWord)
                        self.entry = self.entry[0:indexOfLastWord] + caption
                        
            else:
                """ Caption is a letter """
                if self.entry == "":
                    """ Blank textbox """
                    self.entry = self.entry + caption.upper()
                        # self.entry = self.entry + caption[0].upper() + caption[1:]
                else:
                    """ Textbox has content """
                    if caption == "," or caption == "." or caption == "?" or caption == "!":
                        self.entry = self.entry[0:-1] + caption
                    else:
                        self.entry = self.entry + caption


        return self.entry

    """ Textbox above"""
    """ Word prediction below """

    def set_drag(self, boolDrag):
        return boolDrag

    def set_bool_word_pred(self, bool):
        return bool
        
    def set_word_pred_num(self, num):
        self.wordPredNum = num
        return num

    def set_word_pred_on_last_pressed_key(self, bool):
        return bool
    
    """ Word prediction above """
    """ Word prediction method below """

    def load_bm25(self):
        self.bm25 = Model_Bm25()
        self.boolBm25 = True
        self.boolRoberta = False
        self.boolGpt2 = False
        # Add loading screen
    
    def load_roberta(self):
        self.roberta = Model_Roberta()
        self.boolBm25 = False
        self.boolRoberta = True
        self.boolGpt2 = False
    
    def load_gpt2(self):
        self.gpt2 = Model_Gpt2()
        self.boolBm25 = False
        self.boolRoberta = False
        self.boolGpt2 = True

    def make_word_prediction(self, entry):
        predWords = []
        predSentences = []
        if self.boolBm25:
            predWords, predSentences = self.bm25.predict(entry, self.wordPredNum)
        elif self.boolGpt2:
            pass
        elif self.boolRoberta:
            pass
        
        return predWords

    """ Word prediction method above """

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