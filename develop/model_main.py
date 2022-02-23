import threading
from os import system
from model_fill_word import Fill_Word
from model_bm25 import Model_Bm25
from model_gpt2 import Model_Gpt2
from model_roberta import Model_Roberta
from model_semantic_sentence_retrieval import Model_Semantic_Sentence_Retrieval


class Model_main:
    wordPredTest = ['hey', 'hello', 'have', 'has', 'happy', 'happen']
    sentencePredTest = ["Jingyi, I miss you", "How is your day?", "When can I see you?", "Let's dance."]

    BOOL_ENTRY_BY_KEYWORDS = False
    WORD_PRED_METHOD = ''
    SENT_PRED_METHOD = ''

    def __init__(self):
        self.previousEntry = ''
        self.entry = ''
        self.prediction = ''
        self.boolBm25 = False
        self.boolRoberta = False
        self.boolGpt2 = False
        self.boolSenRetrieval = True # False -> use sentence generation
        self.boolSemantic = False
        self.wordPredNum = 4
        self.sentencePredNum = 4

        

    """ Textbox below"""

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
            indexOfFirstWordOfCaptionInEntry = self.entry.lower().rfind(captionFirstWord)
            self.entry = self.entry[0:indexOfFirstWordOfCaptionInEntry] + caption
            self.entry = self.entry[0].upper() + self.entry[1:] + " "

        return self.entry

    """ Textbox above"""
    """ Word abd sentence prediction below """

    def set_drag(self, boolDrag):
        return boolDrag

    def set_bool_word_pred(self, bool):
        return bool

    def set_bool_sentence_pred(self, bool):
        return bool
        
    def set_word_pred_num(self, num):
        self.wordPredNum = num
        return num

    def set_sentence_pred_num(self, num):
        self.sentencePredNum = num
        return num

    def set_word_pred_on_last_pressed_key(self, bool):
        return bool
    
    """ Word and sentence prediction above """
    """ Word prediction method below """

    def load_fill_word(self):
        self.fillWord = Fill_Word()

    def load_semantic_sen_retrieval(self):
        self.semanticSenRetri = Model_Semantic_Sentence_Retrieval()
        self.boolSenRetrieval = True
        self.boolSemantic = True
        self.boolBm25 = False
        self.boolRoberta = False
        self.boolGpt2 = False


    def load_bm25(self, option, k1, b, epsilon=None, delta=None):
        self.bm25 = Model_Bm25(option, k1, b, epsilon, delta)
        self.boolBm25 = True
        self.boolRoberta = False
        self.boolGpt2 = False
        # Add loading screen
    
    def load_roberta(self):
        self.roberta = Model_Roberta()
        self.boolBm25 = False
        self.boolRoberta = True
        self.boolGpt2 = False
    
    def load_gpt2(self, option, model=None, seed=None, max_length=None, no_repeat_ngram_size=None, num_of_beams=None, top_k=None, top_p=None):
        self.gpt2 = Model_Gpt2(option, model, seed, max_length, no_repeat_ngram_size, num_of_beams, top_k, top_p)
        self.boolBm25 = False
        self.boolRoberta = False
        self.boolGpt2 = True
        # self.gpt2.set_gpt2_method() # "top-p sampling"

    def make_word_prediction(self, entry):
        """ link to controller_main """
        predWords = []
        if self.boolBm25:
            predWords = self.bm25.predict_words(entry)
        elif self.boolGpt2:
            predWords = self.gpt2.predict_words(entry)
        elif self.boolRoberta:
            predWords = self.roberta.predict_words(entry)

        predWordsInNum = self._get_required_num_of_pred(predWords, self.wordPredNum)
        print(f"predicted words: {predWordsInNum}")

        return predWordsInNum

    def make_initail_word_and_word_fill(self, entry):
        """ link to controller_main """
        filledWords = self.fillWord.predict_current_word(entry)
        predFilledWordsInNum = self._get_required_num_of_pred(filledWords, self.wordPredNum)
        return predFilledWordsInNum
    
    def _get_required_num_of_pred(self, predictions, num):
        predictionsInNum = []
        if len(predictions) > num:
            for i in range(num):
                predictionsInNum.append(predictions[i])
        else:
            for pred in predictions:
                predictionsInNum.append(pred)
        return predictionsInNum


    """ Word prediction method above """

    def make_sentence_prediction(self, entry):
        """ link to controller_main """
        # TODO add sentence generation and sentence retrieval options.
        predSentences = []
        if self.boolSenRetrieval:
            predSentences = self.semanticSenRetri.retrieve_sentences(entry)
        else:
            if self.boolBm25:
                # TODO move to above
                predSentences = self.bm25.retrieve_sentences(entry)
            elif self.boolGpt2:
                predSentences = self.gpt2.generate_sentences(entry)
            elif self.boolRoberta:
                pass

        predSetencesInNum = self._get_required_num_of_pred(predSentences, self.sentencePredNum)
        return predSetencesInNum

    """ Sentence prediction method above """




