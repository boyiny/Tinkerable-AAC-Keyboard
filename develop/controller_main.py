from model_main import Model_main
from view_main import View_main, View_menu, View_entry, View_keypad



class Controller_main():
    
    def __init__(self):
        self.modelMain = Model_main()
        self.viewMain = View_main(self)
        
        self.viewEntry = View_entry(self, self.viewMain)
        self.viewKeypad = View_keypad(self, self.viewMain, self.viewEntry)
        self.viewMenu = View_menu(self, self.viewMain)

        self.currentPressedKey = ""
        
        self.boolBm25 = False
        self.boolRoberta = False
        self.boolGpt2 = False

    def main(self):
        self.viewMain.mainloop()

    """ On button click below """

    def on_key_button_click(self, caption): # , boolWordPred, boolSenPred

        self.currentPressedKey = caption
        text = self.modelMain.edit_text_letter(caption) 
        self.viewMain.textBox.set(text)
        self._set_word_pred_display()

    
    def on_predicted_word_button_click(self, entry):
        """ Present selected pred word on textbox """
        predictedWord = self.modelMain.edit_text_word(entry)
        self._set_word_pred_display()
        self.viewMain.textBox.set(predictedWord)

        """ Update the word prediction """
        self._set_word_pred_display()


    """ On button click above """

    """ Word Prediction Below """

    def set_word_pred_num(self, num):
        self.viewKeypad.WORD_PRED_NUM = self.modelMain.set_word_pred_num(num)

    def _set_word_pred_display(self):
        boolWordDisplay = self.modelMain.set_bool_word_pred(self.viewKeypad.BOOL_WORD_PRED_DISPLAY)

        if boolWordDisplay:
            # turn on the display
            # print(f"Set word prediction display: On")
            self.set_word_pred_on_last_pressed_key(self.viewKeypad.BOOL_WORD_PRED_PRESSED_KEY)
        else:
            # turn off the display
            self.viewKeypad.clear_placed_words()
            # print(f"Set word prediction display: Off")

    
    def set_word_pred_on_last_pressed_key(self, bool):
        """ Called in viewMenu """
        entry = self.viewEntry.entry.get()
        predictedWord = self._make_word_prediction(entry)
        # self.currentPressedKey= "h"
        self.viewKeypad.BOOL_WORD_PRED_PRESSED_KEY = self.modelMain.set_word_pred_on_last_pressed_key(bool)
        self.viewKeypad.clear_placed_words()

        if bool:
            # on_last_pressed_key
            self.viewKeypad.place_predicted_words(self.currentPressedKey, predWords=predictedWord)
        else:
            # on fixed location
            self.viewKeypad.place_predicted_words(self.currentPressedKey, predWords=predictedWord)
    
    def set_word_pred_method(self, method):
        if method == "BM25":
            self.modelMain.load_bm25()
        elif method == "RoBERTa":
            self.boolBm25 = False
            self.boolRoberta = True
            self.boolGpt2 = False
            self.modelMain.load_roberta()
        elif method == "GPT-2":
            self.boolBm25 = False
            self.boolRoberta = False
            self.boolGpt2 = True
            self.modelMain.load_gpt2()
        else:
            self.boolBm25 = False
            self.boolRoberta = False
            self.boolGpt2 = False

    def _make_word_prediction(self, entry):
        predictedWord = self.modelMain.make_word_prediction(entry)
        return predictedWord
        # show word pred


    """ Word Prediction Above """

    """ Set dragable keys below """
    
    def set_drag(self, boolDrag):
        self.viewKeypad.KEY_DRAGABLE = self.modelMain.set_drag(boolDrag)
        self.viewKeypad.record_button_position()
        self.viewKeypad.refresh(self, self.viewMain, self.viewEntry)

    """ Set dragable keys above """


if __name__ == '__main__':
    keyboard = Controller_main()
    keyboard.main()