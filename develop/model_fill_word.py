from data_types import Word_importance
import os
import re


class Model_Fill_Word:
    WORD_PRED_NUM = 10

    def __init__(self):
        txt_path = './Dataset/sent_train_aac.txt'
        # print(f"{os.path.dirname(__file__)}")
        txt_path = os.path.join(os.path.dirname(__file__), txt_path)
        with open(txt_path, 'r') as file:
            self.lines = file.readlines()
        self.corpus = []
        
        for sentence in self.lines:
            """ remove "\n" at the end of a sentence """
            sen = sentence.rstrip("\n") 

            """ remove punctuations in a sentence """
            sen = re.sub(r'[^\w\s]','', sen) 

            self.corpus.append(sen)

        self.tokenized_corpus = [doc.split(" ") for doc in self.corpus]
        self.filledWords = []
        
        allWords = []
        for sentence in self.tokenized_corpus:
            for word in sentence:
                allWords.append(word)

        self.wordsImportance = self._cal_words_importance(allWords)

    def _cal_words_importance(self, allWords):
        wordImp = []
        wordsNum = len(allWords)
        dictionary = {}

        for word in allWords:
            if word in dictionary:
                dictionary[word] += 1
            else:
                dictionary.update({word: 1})

        for word in dictionary:
            wordImp.append(Word_importance(word, float(dictionary[word])/float(wordsNum)))

        def takeImportance(wi): 
            """ For each wi in wordImp, take importance for ordering """
            return wi.importance

        """ Ensure the pred current words are taken from the high freq to low freq """
        wordImp.sort(reverse=True, key=takeImportance)

        return wordImp

    def _pred_initial_word(self):
        predInitWords = []
        if self.wordsImportance != []:
            for i in range(self.WORD_PRED_NUM):
                predInitWords.append(self.wordsImportance[i].word)
            
        
        predInitWords = list(dict.fromkeys(predInitWords))

        return predInitWords        

    def _pred_current_word(self):
        
        queryListOfWords = self.query.split()
        currentUnfinishedWord = queryListOfWords[-1]
        print(f"current unfinished word: {currentUnfinishedWord}")

        predCurrentWords = []
        if self.wordsImportance != []:
            for wordImp in self.wordsImportance:
                if wordImp.word.startswith(currentUnfinishedWord):
                    predCurrentWords.append(wordImp.word)

        return predCurrentWords


    # def _get_pred_words(self, numOfPredWords):

    #     if numOfPredWords > self.WORD_PRED_NUM:
    #         numOfPredWords = self.WORD_PRED_NUM

    #     self.predWords = []
    #     predWordsInNum = []

        
    #     if self.query != "": 
    #         """ having entry (unfinished word) in textbox """
    #         self.predWords = self._pred_current_word()

    #     else: 
    #         self.predWords = self._pred_initial_word()
        
    #     # print(f"Predicted Words: {self.predWords}")

    #     if len(self.predWords) > numOfPredWords:
    #         for i in range(numOfPredWords):
    #             predWordsInNum.append(self.predWords[i])
    #     else:
    #         for word in self.predWords:
    #             predWordsInNum.append(word)

    #     # print(f"Pred words in num: {predWordsInNum}")

    #     return predWordsInNum


    def predict_current_word(self, query):
        self.query = query

        self.predWords = []

        if self.query != "": 
            """ having entry (unfinished word) in textbox """
            self.predWords = self._pred_current_word()

        else: 
            self.predWords = self._pred_initial_word()        

        # self.predWords = self._get_pred_words(wordPredNum)

        return self.predWords

if __name__ == '__main__':
    model = Fill_Word()
    query = ""
    words = model.predict_current_word(query)
    print(f"Words: {words}")
