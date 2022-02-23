from model_main import Model_main
from view_main import View_main, View_menu, View_entry, View_keypad
from view_tinker_panel import View_tinker
import configparser 
import os


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
        self.boolSenRetrieval = True
        self.boolSemantic = True

        self.boolWordPredDisplay = False
        self.boolWordPredOnPressedKey = False
        self.boolSentencePredDisplay = False

        self.currentFilledWords = []

        self.file = os.path.realpath(os.path.join(os.path.dirname(__file__), 'tinker.ini'))
        self.config = configparser.ConfigParser()
        self.config.read(self.file)
        self.config.sections()
        
        
    def main(self):
        self.viewMain.mainloop()

    def get_tinker_data(self):
        self.file = os.path.realpath(os.path.join(os.path.dirname(__file__), 'tinker.ini'))
        self.config = configparser.ConfigParser()
        self.config.read(self.file)
        self.config.sections()

        self.word_pred_PREDICTION_TASK          = self.config['PREDICTION_TASK']['word_pred']
        if self.word_pred_PREDICTION_TASK == '':
            self.boolWordPredDisplay = False
            print(f"word pred task is empty")
        else:
            self.boolWordPredDisplay = True
            print(f"word pred task: {self.word_pred_PREDICTION_TASK}")
        self.sentence_pred_PREDICTION_TASK      = self.config['PREDICTION_TASK']['sentence_pred']
        if self.sentence_pred_PREDICTION_TASK == '':
            self.boolSentencePredDisplay = False
            print(f"sen pred task is empty")
        else:
            self.boolSentencePredDisplay = True
            print(f"sen pred task: {self.sentence_pred_PREDICTION_TASK}")

        self.max_pred_num_WORD_PREDICTION       = int(self.config['WORD_PREDICTION']['max_pred_num'])
        self.display_location_WORD_PREDICTION   = str(self.config['WORD_PREDICTION']['display_location'])
        self.method_WORD_PREDICTION             = str(self.config['WORD_PREDICTION']['method'])
        
        self.k1_WORD_BM25OKAPI           = float(self.config['WORD_BM25OKAPI']['k1'])
        self.b_WORD_BM25OKAPI            = float(self.config['WORD_BM25OKAPI']['b'])
        self.epsilon_WORD_BM25OKAPI      = float(self.config['WORD_BM25OKAPI']['epsilon'])

        self.k1_WORD_BM25L              = float(self.config['WORD_BM25L']['k1'])
        self.b_WORD_BM25L               = float(self.config['WORD_BM25L']['b'])
        self.delta_WORD_BM25L           = float(self.config['WORD_BM25L']['delta'])

        self.k1_WORD_BM25PLUS           = float(self.config['WORD_BM25PLUS']['k1'])
        self.b_WORD_BM25PLUS            = float(self.config['WORD_BM25PLUS']['b'])
        self.delta_WORD_BM25PLUS        = float(self.config['WORD_BM25PLUS']['delta'])

        self.model_WORD_GPT2            = str(self.config['WORD_GPT2']['model'])
        self.seed_WORD_GPT2             = int(self.config['WORD_GPT2']['seed'])

        self.model_WORD_ROBERTA         = str(self.config['WORD_ROBERTA']['model'])

        self.max_pred_num_SENTENCE_PREDICTION               = int(self.config['SENTENCE_PREDICTION']['max_pred_num'])
        self.sentence_entry_approach_SENTENCE_PREDICTION    = str(self.config['SENTENCE_PREDICTION']['sentence_entry_approach'])
        self.prediction_approach_SENTENCE_PREDICTION        = str(self.config['SENTENCE_PREDICTION']['prediction_approach'])

        self.similarity_SENTENCE_RETRIEVAL                  = str(self.config['SENTENCE_RETRIEVAL']['similarity'])

        self.retri_method_SENTENCE_TEXT_SIMILARITY          = str(self.config['SENTENCE_TEXT_SIMILARITY']['retri_method'])

        self.k1_SENTENCE_BM25OKAPI       = float(self.config['SENTENCE_BM25OKAPI']['k1'])
        self.b_SENTENCE_BM25OKAPI        = float(self.config['SENTENCE_BM25OKAPI']['b'])
        self.epsilon_SENTENCE_BM25OKAPI  = float(self.config['SENTENCE_BM25OKAPI']['epsilon'])

        self.k1_SENTENCE_BM25L          = float(self.config['SENTENCE_BM25L']['k1'])
        self.b_SENTENCE_BM25L           = float(self.config['SENTENCE_BM25L']['b'])
        self.delta_SENTENCE_BM25L       = float(self.config['SENTENCE_BM25L']['delta'])

        self.k1_SENTENCE_BM25PLUS       = float(self.config['SENTENCE_BM25PLUS']['k1'])
        self.b_SENTENCE_BM25PLUS        = float(self.config['SENTENCE_BM25PLUS']['b'])
        self.delta_SENTENCE_BM25PLUS    = float(self.config['SENTENCE_BM25PLUS']['delta'])

        self.sen_retri_seman_model_SENTENCE_SEMANTIC_SIMILARITY = str(self.config['SENTENCE_SEMANTIC_SIMILARITY']['sen_retri_seman_model'])

        self.method_SENTENCE_GENERATION                         = str(self.config['SENTENCE_GENERATION']['method'])

        self.method_SENTENCE_GPT2                               = str(self.config['SENTENCE_GPT2']['method'])

        self.max_length_SENTENCE_GPT2_GREEDY                = int(self.config['SENTENCE_GPT2_GREEDY']['max_length'])
        self.no_repeat_n_gram_size_SENTENCE_GPT2_GREEDY     = int(self.config['SENTENCE_GPT2_GREEDY']['no_repeat_n_gram_size'])

        self.max_length_SENTENCE_GPT2_BEAM                  = int(self.config['SENTENCE_GPT2_BEAM']['max_length'])
        self.no_repeat_n_gram_size_SENTENCE_GPT2_BEAM       = int(self.config['SENTENCE_GPT2_BEAM']['no_repeat_n_gram_size'])
        self.num_of_beams_SENTENCE_GPT2_BEAM                = int(self.config['SENTENCE_GPT2_BEAM']['num_of_beams'])

        self.max_length_SENTENCE_GPT2_TOP_K                 = int(self.config['SENTENCE_GPT2_TOP_K']['max_length'])
        self.seed_SENTENCE_GPT2_TOP_K                       = int(self.config['SENTENCE_GPT2_TOP_K']['seed'])
        self.top_k_SENTENCE_GPT2_TOP_K                      = int(self.config['SENTENCE_GPT2_TOP_K']['top_k'])

        self.max_length_SENTENCE_GPT2_TOP_P                 = int(self.config['SENTENCE_GPT2_TOP_P']['max_length'])
        self.seed_SENTENCE_GPT2_TOP_P                       = int(self.config['SENTENCE_GPT2_TOP_P']['seed'])
        self.top_k_SENTENCE_GPT2_TOP_P                      = int(self.config['SENTENCE_GPT2_TOP_P']['top_k'])
        self.top_p_SENTENCE_GPT2_TOP_P                      = float(self.config['SENTENCE_GPT2_TOP_P']['top_p'])

        self.max_length_SENTENCE_KWICKCHAT          = int(self.config['SENTENCE_KWICKCHAT']['max_length'])
        self.min_length_SENTENCE_KWICKCHAT          = int(self.config['SENTENCE_KWICKCHAT']['min_length'])
        self.seed_SENTENCE_KWICKCHAT                = int(self.config['SENTENCE_KWICKCHAT']['seed'])
        self.temperature_SENTENCE_KWICKCHAT         = float(self.config['SENTENCE_KWICKCHAT']['temperature'])
        self.top_k_SENTENCE_KWICKCHAT               = int(self.config['SENTENCE_KWICKCHAT']['top_k'])
        self.top_p_SENTENCE_KWICKCHAT               = float(self.config['SENTENCE_KWICKCHAT']['top_p'])
        self.num_of_history_SENTENCE_KWICKCHAT      = int(self.config['SENTENCE_KWICKCHAT']['num_of_history'])
        self.num_of_persona_SENTENCE_KWICKCHAT      = int(self.config['SENTENCE_KWICKCHAT']['num_of_persona'])
        self.persona_SENTENCE_KWICKCHAT             = str(self.config['SENTENCE_KWICKCHAT']['persona']).split('|')
        print(f"Persona list: {self.persona_SENTENCE_KWICKCHAT}")

        self.assign_task()


    """ Tinker Panel responses below """

    def _word_prediction_settings(self):
        # link to view: show pred
        if self.word_pred_PREDICTION_TASK == '':
            self.viewKeypad.clear_placed_words()
        else:
            # make the first prediction based on current input
            self.modelMain.load_fill_word()
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

        # link to view: show pred loaction
        if self.display_location_WORD_PREDICTION == 'Above last pressed key':
            self.viewKeypad.BOOL_WORD_PRED_PRESSED_KEY = True
        elif self.display_location_WORD_PREDICTION == 'Fixed':
            self.viewKeypad.BOOL_WORD_PRED_PRESSED_KEY = False

        # link to view: word pred num
        self.viewKeypad.WORD_PRED_NUM = self.max_pred_num_WORD_PREDICTION

        # link to model: word pred method
        self.modelMain.WORD_PRED_METHOD = self.word_pred_PREDICTION_TASK
        if self.word_pred_PREDICTION_TASK == "WORD_BM25OKAPI": # "BM25L", "BM25Plus", "GPT-2", "RoBERTa"
            option = "BM25Okapi"
            self.modelMain.load_bm25(option, self.k1_WORD_BM25OKAPI, self.b_WORD_BM25OKAPI, epsilon=self.epsilon_WORD_BM25OKAPI)
        elif self.word_pred_PREDICTION_TASK == "WORD_BM25L":
            option = "BM25L"
            self.modelMain.load_bm25(option, self.k1_WORD_BM25L, self.b_WORD_BM25L, delta=self.delta_WORD_BM25L)
        elif self.word_pred_PREDICTION_TASK == "WORD_BM25PLUS":
            option = "BM25Plus"
            self.modelMain.load_bm25(option, self.k1_WORD_BM25PLUS, self.b_WORD_BM25PLUS, delta=self.delta_WORD_BM25PLUS)
        elif self.word_pred_PREDICTION_TASK == "WORD_GPT2":
            pass
        elif self.word_pred_PREDICTION_TASK == "WORD_ROBERTA":
            pass


    def _sentence_prediction_settings(self):
        # link to view: show pred
        if self.sentence_pred_PREDICTION_TASK == '':
            self.viewKeypad.clear_placed_sentences()
        else:
            entry = self.viewEntry.entry.get()
            predictedSentence = self._make_sentence_prediction(entry)
            self.viewKeypad.clear_placed_sentences()
            self.viewKeypad.place_predicted_sentences(predSentence=predictedSentence) # TODO set different for KWickChat
            # self.viewMain.textBox.set(predictedSentence)

        # link to view: sentence pred num
        self.viewKeypad.SENT_PRED_NUM = self.max_pred_num_SENTENCE_PREDICTION

        # link to view and model: entry approach
        # TODO add the actual features for view and model
        if self.sentence_entry_approach_SENTENCE_PREDICTION == 'Keywords':
            self.viewKeypad.BOOL_ENTRY_BY_KEYWORDS = True
            self.modelMain.BOOL_ENTRY_BY_KEYWORDS = True
        elif self.sentence_entry_approach_SENTENCE_PREDICTION == 'Left to right':
            self.viewKeypad.BOOL_ENTRY_BY_KEYWORDS = False
            self.modelMain.BOOL_ENTRY_BY_KEYWORDS = False

        # link to model: sentence pred method
        self.modelMain.SENT_PRED_METHOD = self.sentence_pred_PREDICTION_TASK

    def assign_task(self):
        self._word_prediction_settings()
        # self._sentence_prediction_settings()
    

    """ Tinker Panel responses above """

        

    """ Menu response below """
    
    # done
    def set_word_pred_display(self, boolWordPredDisplay, boolWordPredOnPressedKey):
        # self.boolWordPredDisplay = boolWordPredDisplay
        if boolWordPredDisplay:
            self._set_word_pred_place(boolWordPredOnPressedKey)
        else:
            # turn off word display
            self.viewKeypad.clear_placed_words()

        
    # done
    def set_sentence_pred_display(self, boolSentencePredDisplay):
        # self.boolSentencePredDisplay = boolSentencePredDisplay
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
            if  self.boolSentencePredDisplay:
                # set sentence pred display
                print(f"In controller_main, key_button_click, current entry is: '{entry}'")
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

            if  self.boolSentencePredDisplay:
                # set sentence pred display

                self._make_sentence_prediction_with_pred_words(entry, predWords)

            else:
                self.viewKeypad.clear_placed_sentences()
        
            
    def on_predicted_word_button_click(self, entry):
        """ Present selected pred word on textbox """
        predictedWord = self.modelMain.edit_text_word(entry)
        self.viewMain.textBox.set(predictedWord)

        # """ Update the word prediction when operate the menu during the usage """
        # word pred control
        if self.boolWordPredDisplay:
            self._set_word_pred_place(self.boolWordPredOnPressedKey)
        else:
            self.viewKeypad.clear_placed_words()

        # sentence pred control
        if self.boolSentencePredDisplay:

            self._make_sentence_prediction(self.viewEntry.entry.get())
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
        # TODO add sentence generation and sentence retrieval options
        subType = ""
        if method == "BM25":
            self.modelMain.load_bm25()
        elif method == "RoBERTa":
            self.boolBm25 = False
            self.boolRoberta = True
            self.boolGpt2 = False
            self.modelMain.load_roberta()
        elif "GPT-2" in method:
            index = method.find(":")
            subType = method[index+2:]
            print(f"In set prediction method, subType is '{subType}'")
            self.boolBm25 = False
            self.boolRoberta = False
            self.boolGpt2 = True

            self.modelMain.load_gpt2(subType)
        elif method == "Default":
            self.boolBm25 = False
            self.boolRoberta = False
            self.boolGpt2 = False
            self.boolSenRetrieval = True
            self.boolSemantic = True
            self.modelMain.load_semantic_sen_retrieval()
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



    def _set_sentence_pred_place(self):
        """ For menu setting """
        
        entry = self.viewEntry.entry.get()
        print(f"In controller_main, current entry is: '{entry}'")
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

    # tinkerPanel = View_tinker(keyboard)
    # tinkerPanel.run()
