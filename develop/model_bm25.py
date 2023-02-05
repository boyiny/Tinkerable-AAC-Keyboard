from rank_bm25 import BM25Okapi, BM25L, BM25Plus
from data_types import Word_importance
import os
import re

class Model_Bm25:
    BM25_OPTION = "BM25Okapi"
    BOOL_ENTRY_BY_KEYWORDS = False
    k1_BM25OKAPI = 1.5
    b_BM25OKAPI = 0.75
    epsilon_BM25OKAPI = 0.25

    k1_BM25L = 1.5
    b_BM25L = 0.75
    delta_BM25L = 0.5

    k1_BM25PLUS = 1.5
    b_BM25PLUS = 0.75
    delta_BM25PLUS = 1.0

    def __init__(self, option, k1, b, epsilon=None, delta=None, boolEntryByKeywords=None):
        # print(f"In model_bm25, option = {option}, boolEntryByKeywords = {boolEntryByKeywords} k1 = {k1}, b = {b}, epsilon = {epsilon}, delta = {delta}.")
        if option != None:
            self.BM25_OPTION = option
            self.BOOL_ENTRY_BY_KEYWORDS = boolEntryByKeywords

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

            """ set all words to lower case """
            sen = sen.lower()

            self.corpus.append(sen)

        self.tokenized_corpus = [doc.split(" ") for doc in self.corpus]
        if self.BM25_OPTION == "BM25OKAPI":
            if k1 > 0 and b > 0 and epsilon > 0:
                self.k1_BM25OKAPI = k1
                self.b_BM25OKAPI = b
                self.epsilon_BM25OKAPI = epsilon
            self.bm25 = BM25Okapi(self.tokenized_corpus, k1=self.k1_BM25OKAPI, b=self.b_BM25OKAPI, epsilon=self.epsilon_BM25OKAPI)
        elif self.BM25_OPTION == "BM25L":
            if k1 > 0 and b > 0 and delta > 0:
                self.k1_BM25L = k1
                self.b_BM25L = b
                self.delta_BM25L = delta
            self.bm25 = BM25L(self.tokenized_corpus, k1=self.k1_BM25L, b=self.b_BM25L, delta=self.delta_BM25L)
        elif self.BM25_OPTION == "BM25PLUS":
            if k1 > 0 and b > 0 and delta > 0:
                self.k1_BM25PLUS = k1
                self.b_BM25PLUS = b
                self.b_BM25PLUS = delta
            self.bm25 = BM25Plus(self.tokenized_corpus, k1=self.k1_BM25PLUS, b=self.k1_BM25PLUS, delta=self.delta_BM25PLUS)
        else:
            print(f"Unknown BM25 selection, using BM25Okapi...")
            self.bm25 = BM25Okapi(self.tokenized_corpus)
        
        allWords = []
        for sentence in self.tokenized_corpus:
            for word in sentence:
                allWords.append(word)

        self.wordsImportance = self._cal_words_importance(allWords)


    def predict_words(self, query):
        # print(f"In bm25, word, current entry is: '{query}'")
        predSentences = []
        query = query.lower()
        # print(f"query is: \'{self.query}\'")

        tokenized_query = query.split()
        # print(f"Tokenized query: {tokenized_query}")

        # doc_scores = self.bm25.get_scores(tokenized_query)
        # print(f"score: {doc_scores}")

        topNSen = self.bm25.get_top_n(tokenized_query, self.corpus, n=20)
        # print(f"topNSen: {topNSen}")

        for sen in topNSen:
            sentence = sen.rstrip("\n")
            if sen.startswith(query):
                predSentences.append(sentence)
            # print(f'sentence: {sentence}')
        predSentences = list(dict.fromkeys(predSentences))

        # self.predWords = self._get_pred_words(wordPredNum)

        predWords = []
        predWords = self._pred_next_word(query, predSentences)

        return predWords

    def retrieve_sentences(self, query):
        # print(f"In bm25, sentence, current entry is: '{query}'")
        query = query.lower()
        predSentences = []

        tokenized_query = query.split()

        topNSen = self.bm25.get_top_n(tokenized_query, self.corpus, n=20)

        for sen in topNSen:
            sentence = sen.rstrip("\n")
            if self.BOOL_ENTRY_BY_KEYWORDS:
                predSentences.append(sentence)
            else:
                if sentence.startswith(query):
                    predSentences.append(sentence)
        predSentences = list(dict.fromkeys(predSentences))
        
        return predSentences


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
    
    def _pred_next_word(self, query, predSentences):
        queryListOfWords = query.split()
        currentWord = queryListOfWords[-1]
        # print(f"current word: {currentWord}")

        predWords = []
        if predSentences != []:
            for sen in predSentences:
                listOfWords = sen.split()
                if currentWord in listOfWords and listOfWords.index(currentWord) + 1 < len(listOfWords):
                    nextWord = listOfWords[listOfWords.index(currentWord)+1]
                    predWords.append(nextWord)
        
        predWords = list(dict.fromkeys(predWords))     

        return predWords



if __name__ == '__main__':
    model = Model_Bm25()
    query1 = "You are a"
    query2 = "You are "
    nextWords = model.predict_words(query1)
    sentences = model.retrieve_sentences(query2)
    print(f"Next words: {nextWords}")
    print(f"Sentences: {sentences}")


    