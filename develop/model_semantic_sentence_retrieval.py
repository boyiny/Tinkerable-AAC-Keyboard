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
            self.corpus1 = [line.rstrip() for line in f]
            self.corpus1 = list(set(self.corpus1))
            self.corpus_embeddings1= self.model.encode(self.corpus1, convert_to_tensor=True)
            
        with open(os.path.join(rootDir, 'Dataset', 'MechTurkDataset.txt')) as f:
            self.corpus2 = [line.rstrip() for line in f]
            self.corpus2 = list(set(self.corpus2))
            self.corpus_embeddings2 = self.model.encode(self.corpus2, convert_to_tensor=True)

        self.corpus_embeddings = self.corpus_embeddings1
        self.corpus = self.corpus1
    
    
    def change_corpus(self, corpus_num, filepath):
        # global corpus
        # global corpus_embeddings
        
        if corpus_num == 1:
            self.corpus = self.corpus1
            self.corpus_embeddings = self.corpus_embeddings1
        elif corpus_num == 2:
            self.corpus = self.corpus2
            self.corpus_embeddings = self.corpus_embeddings2
        elif corpus_num == 3:
            with open(filepath) as f:
                self.corpus3 = [line.rstrip() for line in f]
                self.corpus3 = list(set(self.corpus3))
                self.corpus_embeddings3 = self.model.encode(self.corpus3, convert_to_tensor=True)
                self.corpus = self.corpus3
                self.corpus_embeddings = self.corpus_embeddings3
        elif corpus_num == 4:
            corpus4 = []
            corpus_embeddings4 = torch.tensor(self.corpus_embeddings3[0].shape[0],self.corpus_embeddings3[0].shape[1])
            self.corpus = corpus4
            self.corpus_embeddings = corpus_embeddings4

    def _filter(self, sentences, query):
        # to remove the results that do not start with the query - make it as an option for keywords input and conventional left to right input
        results = []
        for sen in sentences:
            if sen.startswith(query):
                results.append(sen)
        return results
        
    # query is the text used as an input to predict what sentence in the corpus the user is aiming to type
    # num_sentences controls how many sentences are predicted

    def retrieve_sentences(self, query):
        num_sentences = 100

        query_embedding = self.model.encode(query, convert_to_tensor=True)
        cos_scores = util.pytorch_cos_sim(query_embedding, self.corpus_embeddings)[0]
        cos_scores = cos_scores.cpu()

        #We use np.argpartition, to only partially sort the num_sentences results
        top_results = np.argpartition(-cos_scores, range(num_sentences))[0:min(num_sentences,len(self.corpus))]
        top_sentences = [self.corpus[idx].strip() for idx in top_results[0:min(num_sentences,len(self.corpus))]]

        results = None
        if self.BOOL_ENTRY_BY_KEYWORDS:
            results = top_sentences
        else:
            results = self._filter(top_sentences, query)
        
        return results

    def add_to_corpus(self, new_sentences):
        # global corpus
        # global corpus_embeddings
        
        # Check if the entered sentences are already present in the corpus
        new_sentences = [sentence for sentence in new_sentences if sentence not in self.corpus]
        
        if len(new_sentences)>0:
            # adding the new sentences to the corpus
            corpus = self.corpus + new_sentences 
            # getting the embeddings of new sentences
            new_sentences_embedding = self.model.encode(new_sentences, convert_to_tensor=True)
            corpus_embeddings = torch.cat([self.corpus_embeddings, new_sentences_embedding.reshape(new_sentences_embedding.shape[0],new_sentences_embedding.shape[1])], dim=0)

if __name__ == '__main__':
    modelSenPred = Model_Semantic_Sentence_Retrieval()

    while True:
        query = input("Your query: ")
        predSentences = modelSenPred.retrieve_sentences(query)
        for sen in predSentences:
            print(sen)
