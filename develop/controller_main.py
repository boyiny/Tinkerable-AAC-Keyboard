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

        self.boolWordPredOnPressedKey = False
        self.boolSentencePredShow = True

    def main(self):
        self.viewMain.mainloop()

    """ On button click below """

    def on_key_button_click(self, caption): # , boolWordPred, boolSenPred

        self.currentPressedKey = caption
        text = self.modelMain.edit_text_letter(caption) 
        self.viewMain.textBox.set(text)
        self._set_word_sentence_pred_display()

    
    def on_predicted_word_button_click(self, entry):
        """ Present selected pred word on textbox """
        predictedWord = self.modelMain.edit_text_word(entry)
        self._set_word_sentence_pred_display()
        self.viewMain.textBox.set(predictedWord)
        """ Update the word prediction """
        self._set_word_sentence_pred_display()


    def on_predicted_sentence_button_click(self, entry):
        predictedSentence = self.modelMain.edit_text_sentence(entry)
        print(f"In controller_main: on_predicted_sentence_button_click()")
        self._set_word_sentence_pred_display()
        self.viewMain.textBox.set(predictedSentence)
        

    """ On button click above """

    """ Word and Sentence Prediction Below """

    def set_word_pred_num(self, num):
        self.viewKeypad.WORD_PRED_NUM = self.modelMain.set_word_pred_num(num)

    def set_sentence_pred_num(self, num):
        self.viewKeypad.SENT_PRED_NUM = self.modelMain.set_sentence_pred_num(num)


    def _set_word_sentence_pred_display(self):

        if self.viewKeypad.BOOL_WORD_PRED_DISPLAY and self.viewKeypad.BOOL_SENT_PRED_DISPLAY:
            self._set_word_sentence_pred_place()
        elif not(self.viewKeypad.BOOL_WORD_PRED_DISPLAY) and self.viewKeypad.BOOL_SENT_PRED_DISPLAY:
            self._set_word_sentence_pred_place()
            self.viewKeypad.clear_placed_words()
        elif self.viewKeypad.BOOL_WORD_PRED_DISPLAY and not(self.viewKeypad.BOOL_SENT_PRED_DISPLAY):
            self._set_word_sentence_pred_place()
            self.viewKeypad.clear_placed_sentence()
        else:
            # turn off word and sentence display
            self.viewKeypad.clear_placed_words()

    
    def set_prediction_method(self, method):
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


    def _make_word_sentence_prediction(self, entry):
        predictedWord, predictedSentence = self.modelMain.make_word_sentence_prediction(entry)
        return predictedWord, predictedSentence
        # show word pred


    def set_word_pred_place(self, boolWordPlaceOnLastPressedKey):
        self.boolWordPredOnPressedKey = boolWordPlaceOnLastPressedKey
        self._set_word_sentence_pred_place()
    
    def set_sentence_pred_place(self, boolSentencePredShow):
        self.boolSentencePredShow = boolSentencePredShow
        self._set_word_sentence_pred_place()


    def _set_word_sentence_pred_place(self):
        """ Called in viewMenu """
        entry = self.viewEntry.entry.get()
        predictedWord, predictedSentence = self._make_word_sentence_prediction(entry)
        # set button place method
        self.viewKeypad.BOOL_WORD_PRED_PRESSED_KEY = self.modelMain.set_word_pred_on_last_pressed_key(self.boolWordPredOnPressedKey)
        self.viewKeypad.clear_placed_words()

        

        if self.boolWordPredOnPressedKey:
            # on_last_pressed_key
            self.viewKeypad.place_predicted_words(self.currentPressedKey, predWords=predictedWord)
        else:
            # on fixed location
            self.viewKeypad.place_predicted_words(self.currentPressedKey, predWords=predictedWord)
        
        self.viewKeypad.place_predicted_sentences(predictedSentence)
        # TODO: set sentence display flag
        # if self.viewKeypad.BOOL_SENT_PRED_DISPLAY:
        #     self.viewKeypad.place_predicted_sentences(predictedSentence)
       

    
    """ Word and Sentence Prediction Above """


    """ Set dragable keys below """
    
    def set_drag(self, boolDrag):
        self.viewKeypad.KEY_DRAGABLE = self.modelMain.set_drag(boolDrag)
        self.viewKeypad.record_button_position()
        self.viewKeypad.refresh(self, self.viewMain, self.viewEntry)

    """ Set dragable keys above """


if __name__ == '__main__':
    keyboard = Controller_main()
    keyboard.main()