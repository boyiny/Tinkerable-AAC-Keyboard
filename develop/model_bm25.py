from rank_bm25 import BM25Okapi
from data_types import Word_importance
import os

class Model_Bm25:
    WORD_PRED_NUM = 10
    SENT_PRED_NUM = 10

    def __init__(self):

        txt_path = './Dataset/sent_dev_aac.txt'
        print(f"{os.path.dirname(__file__)}")
        txt_path = os.path.join(os.path.dirname(__file__), txt_path)
        with open(txt_path, 'r') as file:
            self.lines = file.readlines()
        self.corpus = []
        
        for sentence in self.lines:
            """ remove "\n" at the end of a sentence """
            sen = sentence.rstrip("\n") 

            """ remove marks at the end of a sentence """
            sen = sen[0:-1] 

            self.corpus.append(sen)

        self.tokenized_corpus = [doc.split(" ") for doc in self.corpus]
        self.bm25 = BM25Okapi(self.tokenized_corpus)
        self.predSentences = []
        self.predWords = []
        
        allWords = []
        for sentence in self.tokenized_corpus:
            for word in sentence:
                allWords.append(word)

        self.wordsImportance = self._cal_words_importance(allWords)


    def predict(self, query, wordPredNum):
        self.query = query
        tokenized_query = query.split(" ")

        # doc_scores = self.bm25.get_scores(tokenized_query)
        # print(f"score: {doc_scores}")

        topNSen = self.bm25.get_top_n(tokenized_query, self.corpus, n=10)
        # print(f"topNSen: {topNSen}")

        for i in range(len(topNSen)):
            sentence = topNSen[i].rstrip("\n")
            self.predSentences.append(sentence)
            # print(f'sentence: {sentence}')
        self.predSentences = list(dict.fromkeys(self.predSentences))

        self.predWords = self._get_pred_words(wordPredNum)

        return self.predWords, self.predSentences


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
        if self.predSentences != []:
            for sen in self.predSentences:
                listOfWords = sen.split()
                initWord = listOfWords[0]
                predInitWords.append(initWord)
        
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
    
    def _pred_next_word(self):
        queryListOfWords = self.query.split()
        currentWord = queryListOfWords[-1]
        print(f"current word: {currentWord}")

        predWords = []
        if self.predSentences != []:
            for i in range(self.WORD_PRED_NUM):
                listOfWords = self.predSentences[i].split()
                if currentWord in listOfWords:
                    nextWord = listOfWords[listOfWords.index(currentWord)+1]
                    predWords.append(nextWord)
        
        predWords = list(dict.fromkeys(predWords))     

        return predWords


    def _get_pred_words(self, numOfPredWords):

        if numOfPredWords > self.WORD_PRED_NUM:
            numOfPredWords = self.WORD_PRED_NUM

        self.predWords = []
        predWordsInNum = []

        
        if self.query != "": 
            """ having entry in textbox """
            if self.query[-1] == " ":
                self.predWords = self._pred_next_word()
            else:
                self.predWords = self._pred_current_word()

        else: 
            self.predWords = self._pred_initial_word()
        
        # print(f"Predicted Words: {self.predWords}")

        if len(self.predWords) > numOfPredWords:
            for i in range(numOfPredWords):
                predWordsInNum.append(self.predWords[i])
        else:
            for word in self.predWords:
                predWordsInNum.append(word)

        # print(f"Pred words in num: {predWordsInNum}")

        return predWordsInNum
        
    
    def _get_sentence_pred(self, numOfPredSentences):
        if numOfPredSentences > self.SENT_PRED_NUM:
            numOfPredSentences = self.SENT_PRED_NUM
        predSentences = []
        if self.results != []:
            for i in range(numOfPredSentences):
                predSentences.append(self.results[i])
        return predSentences



if __name__ == '__main__':
    model = Model_Bm25()
    query = "te"
    words, sentences = model.predict(query, 4)
    print(f"Words: {words}")
    print(f"Sentences: {sentences}")


    