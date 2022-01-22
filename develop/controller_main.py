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

        self.boolWordPredDisplay = False
        self.boolWordPredOnPressedKey = False
        self.boolSentencePredDisplay = False

        self.currentFilledWords = []
        
        
    def main(self):
        self.viewMain.mainloop()

    """ Menu response below """
    def set_word_pred_display(self, boolWordPredDisplay, boolWordPredOnPressedKey):
        self.boolWordPredDisplay = boolWordPredDisplay
        if boolWordPredDisplay:
            self._set_word_pred_place(boolWordPredOnPressedKey)
        else:
            # turn off word display
            self.viewKeypad.clear_placed_words()

    def set_sentence_pred_display(self, boolSentencePredDisplay):
        self.boolSentencePredDisplay = boolSentencePredDisplay
        if boolSentencePredDisplay:
            self._set_sentence_pred_place()
        else:
            self.viewKeypad.clear_placed_sentences()


    """ Menu response above """


    """ On button click below """


    def on_key_button_click(self, caption): # , boolWordPred, boolSenPred
        self.currentPressedKey = caption
        text = self.modelMain.edit_text_letter(caption) 
        self.viewMain.textBox.set(text)

        predWords = []

        entry = self.viewEntry.entry.get()
        if entry == "":
            """ Initial input """   
            if self.boolWordPredDisplay:      
                # set fill initial word  
                predWords = self._make_word_fill(entry)
            else:
                self.viewKeypad.clear_placed_words()
            if self.boolSentencePredDisplay:
                # set sentence pred display

                # TODO set different cases, get predicted word
                self._make_sentence_prediction_with_pred_words(entry, predWords)
            else:
                self.viewKeypad.clear_placed_sentences()

        elif entry[-1] == " ":
            """ Finished a word """
            if self.boolWordPredDisplay:      
                # set fill initial word  
                # self._make_word_fill(entry)
                predWords = self._make_word_prediction(entry)
            else:
                self.viewKeypad.clear_placed_words()
            if self.boolSentencePredDisplay:
                # set sentence pred display
                self._make_sentence_prediction(entry)
            else:
                self.viewKeypad.clear_placed_sentences()

        else:
            """ Typing a word """
            if self.boolWordPredDisplay:      
                # set fill initial word  
                predWords = self._make_word_fill(entry)
            else:
                self.viewKeypad.clear_placed_words()

            if self.boolSentencePredDisplay:
                # set sentence pred display

                self._make_sentence_prediction_with_pred_words(entry, predWords)

            else:
                self.viewKeypad.clear_placed_sentences()
        
            
    def on_predicted_word_button_click(self, entry):
        """ Present selected pred word on textbox """
        predictedWord = self.modelMain.edit_text_word(entry)
        self.viewMain.textBox.set(predictedWord)

        """ Update the word prediction when operate the menu during the usage """
        # word pred control
        if self.viewKeypad.BOOL_WORD_PRED_DISPLAY:
            self._set_word_pred_place(self.boolWordPredOnPressedKey)
        else:
            self.viewKeypad.clear_placed_words()

        # sentence pred control
        if self.viewKeypad.BOOL_SENT_PRED_DISPLAY:

            self._make_sentence_prediction(entry)
        else:
            self.viewKeypad.clear_placed_sentences()
        

    def on_predicted_sentence_button_click(self, entry):
        predictedSentence = self.modelMain.edit_text_sentence(entry)
        print(f"In controller_main: on_predicted_sentence_button_click()")
        self._set_sentence_pred_place()
        self.viewMain.textBox.set(predictedSentence)
        

    """ On button click above """

    """ Word and Sentence Prediction Below """

    def set_word_pred_num(self, num):
        self.viewKeypad.WORD_PRED_NUM = self.modelMain.set_word_pred_num(num)

    def set_sentence_pred_num(self, num):
        self.viewKeypad.SENT_PRED_NUM = self.modelMain.set_sentence_pred_num(num)

    
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

    def _make_word_fill(self, entry): 
        currentWord = self.modelMain.make_initail_word_and_word_fill(entry)
        self.currentFilledWords = currentWord
        self.viewKeypad.clear_placed_words()
        self.viewKeypad.place_predicted_words(self.currentPressedKey, predWords=currentWord)
        return currentWord

    def _make_word_prediction(self, entry):
        predictedWords = self.modelMain.make_word_prediction(entry)
        self.viewKeypad.clear_placed_words()
        self.viewKeypad.place_predicted_words(self.currentPressedKey, predWords=predictedWords)
        return predictedWords


    def _make_sentence_prediction(self, entry):
        predictedSentences = self.modelMain.make_sentence_prediction(entry)
        self.viewKeypad.clear_placed_sentences()
        self.viewKeypad.place_predicted_sentences(predSentence=predictedSentences)
        return predictedSentences
        # show word pred


    def _make_sentence_prediction_with_pred_words(self, entry, predWords):
        """ Show 2 sentence predictions for [the entry + first word], 1 sentence prediction for [the entry + second word] and [the entry + third word] """
        predictedSentences = []
        predSenTemp1 = []
        predSenTemp2 = []
        predSenTemp3 = []
        predSenTemp4 = []

        i = 0
        for word in predWords:
            if entry == "":
                entryWithPredWord = entry + word
            elif entry[-1] == " ":
                entryWithPredWord = entry + word
            else: 
                listOfWords = entry.split()
                lastWord = listOfWords[-1]
                indexOfLastWord = entry.rfind(lastWord)
                entryWithPredWord = entry[0:indexOfLastWord] + word
            print(f"entryWithPredWord is {entryWithPredWord}.")
            predSen = self.modelMain.make_sentence_prediction(entryWithPredWord)
            
            if len(predSen) > 0:
                if i == 0:
                    predSenTemp1 = predSen
                elif i == 1:
                    predSenTemp2 = predSen
                elif i == 2: 
                    predSenTemp3 = predSen
                else:
                    predSenTemp4 = predSen
            i += 1

        if len(predSenTemp1) >= 2:
            for n in range(2):
                predictedSentences.append(predSenTemp1[n])
            if len(predSenTemp2) >= 1:
                predictedSentences.append(predSenTemp2[0]) 
                if len(predSenTemp3) >= 1:
                    """ ideal, all have pred -> 1,1,2,3 """
                    predictedSentences.append(predSenTemp3[0])
                else:
                    """ temp3 == 0 -> 1,1,2,4 """
                    predictedSentences.append(predSenTemp4[0])
            else:
                """ temp2 == 0 """
                if len(predSenTemp3) >= 1:
                    predictedSentences.append(predSenTemp3[0])
                    if len(predSenTemp4) >= 1:
                        """ -> 1,1,3,4 """
                        predictedSentences.append(predSenTemp4[0])
                    else:
                        """ temp4 == 0 """
                        if len(predSenTemp3) >= 2:
                            """ -> 1,1,3,3 """
                            predictedSentences.append(predSenTemp3[1])
                        else:
                            if len(predSenTemp1) >= 3: 
                                """ -> 1,1,1,3 """
                                predictedSentences[2] = predSenTemp1[2]
                                predictedSentences.append(predSenTemp3[0])
        
        if len(predictedSentences) < 4 and predSenTemp1 == 4:
            """ -> 1,1,1,1 """
            predictedSentences = []
            for sen in predSenTemp1:
                predictedSentences.append(sen)


        predictedSentencesWithoutNone = []
        for sen in predictedSentences:
            if sen != "":
                predictedSentencesWithoutNone.append(sen)
        self.viewKeypad.clear_placed_sentences()
        self.viewKeypad.place_predicted_sentences(predSentence=predictedSentencesWithoutNone)

        return predictedSentences


    def _set_word_pred_place(self, boolWordPlaceOnLastPressedKey):
        """ Link to view_main menu """
        """ self.boolWordPredDisplay is True """
        self.modelMain.load_fill_word()

        self.boolWordPredOnPressedKey = boolWordPlaceOnLastPressedKey
        
        self.viewKeypad.BOOL_WORD_PRED_PRESSED_KEY = self.modelMain.set_word_pred_on_last_pressed_key(self.boolWordPredOnPressedKey)
        
        entry = self.viewEntry.entry.get()
        if entry == "":
            """ First word """
            self._make_word_fill(entry)
        elif entry[-1] == " ":
            """ Finished a word """
            self._make_word_prediction(entry)
        else:
            """ Typing a word """
            self._make_word_fill(entry)
    


    # def _set_word_pred_place(self):
    #     entry = self.viewEntry.entry.get()
    #     predictedWord = self._make_word_prediction(entry)
    #     self.viewKeypad.BOOL_WORD_PRED_PRESSED_KEY = self.modelMain.set_word_pred_on_last_pressed_key(self.boolWordPredOnPressedKey)
    #     self.viewKeypad.clear_placed_words()
        
    #     if self.boolWordPredDisplay:
    #         self.viewKeypad.place_predicted_words(self.currentPressedKey, predWords=predictedWord)





    def _set_sentence_pred_place(self):
        """ For menu setting """
        
        entry = self.viewEntry.entry.get()
        print(f"Current entry is: {entry}.")
        predictedSentence = self._make_sentence_prediction(entry)
        # set button place method
        self.viewKeypad.BOOL_WORD_PRED_PRESSED_KEY = self.modelMain.set_word_pred_on_last_pressed_key(self.boolWordPredOnPressedKey)
        self.viewKeypad.clear_placed_sentences()
        
        if self.boolSentencePredDisplay:
            self.viewKeypad.place_predicted_sentences(predSentence=predictedSentence)

       

    
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