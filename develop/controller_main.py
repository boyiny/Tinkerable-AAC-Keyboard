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

    def on_key_button_click(self, caption): # , boolWordPred, boolSenPred
        # if boolWordPred:
        # # get current entry
        #     entry = self.viewEntry.entry.get()
        self.currentPressedKey = caption

        text = self.modelMain.edit_text(caption) 
        self.viewMain.textBox.set(text)

        self.set_word_pred_display(self.viewKeypad.BOOL_WORD_PRED_DISPLAY)

        # print(f'button in lambda is: {caption}')
        # if boolWordPred:
        #     self.viewKeypad.make_word_prediction()

    """ Word Prediction Below """

    def set_word_pred_num(self, num):
        self.viewKeypad.WORD_PRED_NUM = self.modelMain.set_word_pred_num(num)

    def set_word_pred_display(self, bool):
        self.viewKeypad.BOOL_WORD_PRED_DISPLAY = self.modelMain.set_bool_word_pred(bool)
        if bool:
            # turn on the display
            # print(f"Set word prediction display: On")
            self.set_word_pred_on_last_pressed_key(self.viewKeypad.BOOL_WORD_PRED_PRESSED_KEY)
        else:
            # turn off the display
            self.viewKeypad.clear_placed_words()
            # print(f"Set word prediction display: Off")

    
    def set_word_pred_on_last_pressed_key(self, bool):
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

   

    def on_word_prediction_click(self, entry, boolOnTopOfPressedKey):
        predictedWord = self.modelMain.edit_text(entry)
        
        text = self.viewKeypad.make_word_prediction(predictedWord, boolOnTopOfPressedKey)
        self.viewMain.textBox.set(text)

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