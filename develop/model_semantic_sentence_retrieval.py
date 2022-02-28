from sentence_transformers import SentenceTransformer, util
import numpy as np
import torch
import os

class Model_Semantic_Sentence_Retrieval:
    MODEL = 'all-mpnet-base-v2'
    BOOL_ENTRY_BY_KEYWORDS = False

    def __init__(self, model, boolEntryByKeywords=None):
        self.BOOL_ENTRY_BY_KEYWORDS = boolEntryByKeywords

        self.MODEL = model
        print(f"In SBERT, using model: {self.MODEL}")
        rootDir = os.path.dirname(__file__)

        # self.model = SentenceTransformer(os.path.join(rootDir, 'Model','DistilbertBase')) # './' + path_change +'DistilbertBase' 
        self.model = SentenceTransformer(self.MODEL)

        with open(os.path.join(rootDir, 'Dataset', 'sent_train_aac.txt')) as f: #  + path_change
            self.corpus = [line.rstrip() for line in f]
            self.corpus = list(set(self.corpus))
            self.corpusEmbeddings= self.model.encode(self.corpus, convert_to_tensor=True)
            
        self.corpus = self.corpus
    
    def _filter(self, sentences, query):
        # to remove the results that do not start with the query - make it as an option for keywords input and conventional left to right input
        results = []
        for sen in sentences:
            if sen.startswith(query):
                results.append(sen)
        return results

    def retrieve_sentences(self, query):
        numSentences = 100

        queryEmbedding = self.model.encode(query, convert_to_tensor=True)
        cosScores = util.pytorch_cos_sim(queryEmbedding, self.corpusEmbeddings)[0]
        cosScores = cosScores.cpu()

        #We use np.argpartition, to only partially sort the num_sentences results
        topResults = np.argpartition(-cosScores, range(numSentences))[0:min(numSentences,len(self.corpus))]
        topSentences = [self.corpus[idx].strip() for idx in topResults[0:min(numSentences,len(self.corpus))]]

        results = None
        if self.BOOL_ENTRY_BY_KEYWORDS:
            results = topSentences
        else:
            results = self._filter(topSentences, query)
        
        return results

    # def add_to_corpus(self, newSentences):
    #     # global corpus
    #     # global corpus_embeddings
        
    #     # Check if the entered sentences are already present in the corpus
    #     newSentences = [sentence for sentence in newSentences if sentence not in self.corpus]
        
    #     if len(newSentences)>0:
    #         # adding the new sentences to the corpus
    #         corpus = self.corpus + newSentences 
    #         # getting the embeddings of new sentences
    #         newSentencesEmbedding = self.model.encode(newSentences, convert_to_tensor=True)
    #         corpusEmbeddings = torch.cat([self.corpusEmbeddings, newSentencesEmbedding.reshape(newSentencesEmbedding.shape[0],newSentencesEmbedding.shape[1])], dim=0)

if __name__ == '__main__':
    modelSenPred = Model_Semantic_Sentence_Retrieval()

    while True:
        query = input("Your query: ")
        predSentences = modelSenPred.retrieve_sentences(query)
        for sen in predSentences:
            print(sen)
