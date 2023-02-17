import threading
from os import system
from model_fill_word import Model_Fill_Word
from model_bm25 import Model_Bm25
from model_gpt2 import Model_Gpt2
from model_roberta import Model_Roberta
from model_semantic_sentence_retrieval import Model_Semantic_Sentence_Retrieval
from model_kwickchat.model_kwickchat import Model_Kwickchat
from model_speech_recognition import Model_speech_recognition
from model_trace_analysis import Model_Trace_Analysis


class Model_main:
    
    sentence_pred_PREDICTION_TASK = ''
    prediction_approach_SENTENCE_PREDICTION = ''
    BOOL_ENTRY_BY_KEYWORDS = False
    WORD_PRED_METHOD = '' # exact task option
    SENT_PRED_METHOD = '' # exact task option

    SENT_ENTRY_APPROACH = 'Left to right' 
    
    historyKwickchat = []    

    # Don't change
    wordPredNum = 4 
    sentencePredNum = 4
    
    
    

    def __init__(self):
        self.previousEntry = ''
        self.entry = ''
        self.prediction = ''
        
       

 

    """ Word abd sentence prediction below """

    def set_drag(self, boolDrag):
        return boolDrag
    
    # def set_trace(self, boolTrace):
    #     self.trace_analysis = Model_Trace_Analysis(boolTrace)
    #     return boolTrace

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
        self.fillWord = Model_Fill_Word()


    def load_bm25_word(self, option, k1, b, epsilon=None, delta=None):
        self.bm25Word = Model_Bm25(option, k1, b, epsilon, delta)

    def load_gpt2_word(self, option, model=None, seed=None, method=None, max_length=None, no_repeat_ngram_size=None, num_of_beams=None, top_k=None, top_p=None):
        self.gpt2Word = Model_Gpt2(option, model, seed, method, max_length, no_repeat_ngram_size, num_of_beams, top_k, top_p)

    def load_roberta_word(self, option, model):
        self.roberta = Model_Roberta(option, model)


    def load_bm25_sentence(self, option, k1, b, epsilon=None, delta=None):
        self.bm25Sentence = Model_Bm25(option, k1, b, epsilon, delta, boolEntryByKeywords=self.BOOL_ENTRY_BY_KEYWORDS)

    def load_semantic_sen_retrieval_sentence(self, model):
        self.semanticSenRetriSentence = Model_Semantic_Sentence_Retrieval(model, boolEntryByKeywords=self.BOOL_ENTRY_BY_KEYWORDS)
    
    def load_gpt2_sentence(self, option, model=None, seed=None, method=None, max_length=None, no_repeat_ngram_size=None, num_of_beams=None, top_k=None, top_p=None):
        self.gpt2Sentence = Model_Gpt2(option, model, seed, method, max_length, no_repeat_ngram_size, num_of_beams, top_k, top_p)

    def load_kwickchat_sentence(self, option, max_length, min_length, seed, temperature, top_k, top_p, num_of_history_exchanges, persona):
        self.kwickchatSentence = Model_Kwickchat(option, max_length, min_length, seed, temperature, top_k, top_p, num_of_history_exchanges, persona)
        self.partnerSpeech = Model_speech_recognition()

    def conv_partner_speech_recognition_kwickchat(self):
        partnerInput = self.partnerSpeech.partnerSpeechInputRecognition()
        return partnerInput

    def add_conv_partner_input_to_history(self, partnerInput):
        self.historyKwickchat.append(partnerInput)
    
    def add_user_input_to_history(self, userInput):
        # when "Speak" button is clicked in KwickChat mode
        self.historyKwickchat.append(userInput)


    def make_word_prediction(self, entry):
        """ link to controller_main """
        predWords = []
        if 'WORD_BM25' in self.WORD_PRED_METHOD:
            predWords = self.bm25Word.predict_words(entry)
        elif 'WORD_GPT2' in self.WORD_PRED_METHOD:
            predWords = self.gpt2Word.predict_words(entry)
        elif 'WORD_ROBERTA' in self.WORD_PRED_METHOD:
            predWords = self.roberta.predict_words(entry)

        predWordsInNum = self._get_required_num_of_pred(predWords, self.wordPredNum)
        print(f"pred method: {self.WORD_PRED_METHOD}, pred words: {predWordsInNum}")

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
        predSentences = []
        if self.prediction_approach_SENTENCE_PREDICTION == 'Retrieval':
            # retrieve sentence every time the entry is updated. 
            if self.SENT_PRED_METHOD == 'SENTENCE_BM25OKAPI':
                predSentences = self.bm25Sentence.retrieve_sentences(entry)
            elif self.SENT_PRED_METHOD == 'SENTENCE_BM25L':
                predSentences = self.bm25Sentence.retrieve_sentences(entry)
            elif self.SENT_PRED_METHOD == 'SENTENCE_BM25PLUS':
                predSentences = self.bm25Sentence.retrieve_sentences(entry)
            elif self.SENT_PRED_METHOD == 'SENTENCE_SEMANTIC_SIMILARITY':
                predSentences = self.semanticSenRetriSentence.retrieve_sentences(entry)
        elif self.prediction_approach_SENTENCE_PREDICTION == 'Generation':
            # generate sentence every time a word is typed. 
            if entry != '':
                if entry[-1] == ' ':
                    if 'SENTENCE_GPT2' in self.SENT_PRED_METHOD: # multiple GPT2 methods
                        predSentences = self.gpt2Sentence.generate_sentences(entry)
                    elif self.SENT_PRED_METHOD == 'SENTENCE_KWICKCHAT':
                        self.historyKwickchat = self.kwickchatSentence.adjust_history_size(self.historyKwickchat)
                        predSentences = self.kwickchatSentence.generate_sentences(self.historyKwickchat, entry)
        


        predSetencesInNum = self._get_required_num_of_pred(predSentences, self.sentencePredNum)
        
        print(f"pred method: {self.SENT_PRED_METHOD}, pred sentence: {predSetencesInNum}")
        
        return predSetencesInNum

    """ Sentence prediction method above """




