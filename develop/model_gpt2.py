from symtable import Symbol
from unittest.util import _MAX_LENGTH
from soupsieve import match
import torch
from transformers import pipelines, set_seed
from transformers import GPT2TokenizerFast, GPT2LMHeadModel
import transformers
import time
import re

class Model_Gpt2:

    MAX_LENGTH = 30
    SEED = 0
    SYMBOLS = "!@#$%^&*()_-+=`~\{\};':\",./<>?\|\n"

    def __init__(self, option, model=None, seed=None, method=None, max_length=None, no_repeat_ngram_size=None, num_of_beams=None, top_k=None, top_p=None):
        print(f"GPT2 option: {option}, model: {model}, seed: {seed}, method: {method}, max_length: {max_length}, no_repeat_ngram_size: {no_repeat_ngram_size}, num_of_beams: {num_of_beams}, top_k: {top_k}, top_p: {top_p}")
        self.OPTION = option
        if "WORD" in option:
            self.MODEL = model
            self.SEED = seed
        elif "SENTENCE" in option:
            self.MODEL = model
            self.MAX_LENGTH = max_length
            self.NO_REPET_NGRAM_SIZE = no_repeat_ngram_size
            self.NUM_OF_BEAMS = num_of_beams
            self.TOP_K = top_k
            self.TOP_P = top_p
        
        self._load_gpt2_using_model_mechanism()

        # Using pipline by default
        # self.generator = pipelines.pipeline(task='text-generation', model='gpt2', framework='pt')
        # set_seed(self.SEED)
        

    # done
    def set_gpt2_method(self, type):
        """ Link the menu """        
        self.OPTION = type
        self._load_gpt2_using_model_mechanism()

    def _load_gpt2_using_model_mechanism(self):
        # Load pre-trained model tokenizer (vocabulary)

        self.tokenizer = GPT2TokenizerFast.from_pretrained(self.MODEL)

        # Load pre-trained model (weights)
        # add the EOS token as PAD token to avoid warnings
        self.MODEL = GPT2LMHeadModel.from_pretrained(self.MODEL, pad_token_id=self.tokenizer.eos_token_id)

        # Load pre-trained model tokenizer (vocabulary)
        # self.tokenizer = GPT2TokenizerFast.from_pretrained('/Users/yangboyin/Code/Cambridge/AAC/Tinkerable-AAC-Keyboard/Playground/GPT2Model', local_files_only=True)

        # # Load pre-trained model (weights)
        # self.model = GPT2LMHeadModel.from_pretrained('/Users/yangboyin/Code/Cambridge/AAC/Tinkerable-AAC-Keyboard/Playground/GPT2Model', local_files_only=True)

        self.MODEL.eval()

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

    def _strip_one_sentence(self, predictions):
        # strip a sentence - end by , or .
        oneSentenceList = []
        for result in predictions:
            index = len(result) 
            indexOfPeriod = result.find(".")
            indexOfComma = result.find(",")
            indexOfQuestionMark = result.find("?")
            indexOfExclamationMark = result.find("!")
            indexOfNewLine = result.find("\n")
            if indexOfPeriod != -1 and indexOfPeriod < index:
                index = indexOfPeriod
            if indexOfComma != -1 and indexOfComma < index:
                index = indexOfComma
            if indexOfQuestionMark != -1 and indexOfQuestionMark < index:
                index = indexOfQuestionMark
            if indexOfExclamationMark != -1 and indexOfExclamationMark < index:
                index = indexOfExclamationMark
            if indexOfNewLine != -1 and indexOfNewLine < index:
                index = indexOfNewLine
            singleSentence = result[0:index]
            oneSentenceList.append(singleSentence)
            # print(singleSentence)
        return oneSentenceList

    def _run_gpt2_method(self, query):
        results = []

        if 'GPT2_GREEDY' in self.OPTION:
            results.append(self._greedy_output(query))
        elif 'GPT2_BEAM' in self.OPTION:
            results = self._beam_output(query)
        elif 'GPT2_TOP_K' in self.OPTION: 
            results = self._top_k_sampling_output(query)
        elif 'GPT2_TOP_P' in self.OPTION:
            results = self._top_p_sampling_output(query)
        # elif self.type == "default":
        #     results = self._default_output(query)
        
        prediction = self._strip_one_sentence(results)
        
        return prediction

    def predict_words(self, query):
        #encode text inputs
        query = query.strip()
        indexed_tokens = self.tokenizer.encode(query)
        
        # Convert indexed tokens in a PyTorch tensor
        tokens_tensor = torch.tensor([indexed_tokens])
        
        # Predict all tokens
        with torch.no_grad():
            outputs = self.MODEL(tokens_tensor)
            predictions = outputs[0]
            
        top_preds = 50
        predWords = []
        
        predicted_indices = torch.argsort(predictions[0, -1, :], descending=True)

        for i in range(top_preds):
            predictedItem = predicted_indices[i].item()
            decodedPredictedText = self.tokenizer.decode([predictedItem]).strip()
            decodedPredictedText = re.sub(r'[^\w]', '', decodedPredictedText)
            if decodedPredictedText != '':
                predWords.append(decodedPredictedText)
            
        return predWords

    # def predict_words(self, query):
    #     query = query.strip()
    #     print(f"In gpt2 words, current entry is: '{query}'")
    #     predWords = []
    #     prediction = self._run_gpt2_method(query)
        
    #     predWords = self._pred_next_word(query, prediction)

    #     return predWords
    
    def generate_sentences(self, query):
        query = query.strip()
        print(f"In gpt2 generate_sentences, current entry is: '{query}'")

        predSentences = []
        
        if query != "":
            predSentences = self._run_gpt2_method(query)

        return predSentences


    def _greedy_output(self, query):
        
        # encode context the generation is conditioned on
        input_ids = self.tokenizer.encode(query, return_tensors='pt')

        # generate text until the output length (which includes the context length) reaches 50
        greedy_result = self.MODEL.generate(
            input_ids, 
            max_length=self.MAX_LENGTH, 
            no_repeat_ngram_size=2)
        decodedGreedyResult = self.tokenizer.decode(greedy_result[0], skip_special_tokens=True)

        return decodedGreedyResult

    def _beam_output(self, query):
        # encode context the generation is conditioned on
        input_ids = self.tokenizer.encode(query, return_tensors='pt')

        # activate beam search and early_stopping
        beam_output = self.MODEL.generate(
            input_ids, 
            max_length=self.MAX_LENGTH, 
            num_beams=5, 
            no_repeat_ngram_size=2, 
            early_stopping=True
        )
        decodedBeamResult = []
        decodedBeamResult.append(self.tokenizer.decode(beam_output[0], skip_special_tokens=True))

        return decodedBeamResult

    def _sampling_output(self, query):
        # encode context the generation is conditioned on
        input_ids = self.tokenizer.encode(query, return_tensors='pt')

        # set seed to reproduce results. Feel free to change the seed though to get different results
        set_seed(self.SEED)

        # activate sampling and deactivate top_k by setting top_k sampling to 0
        sampling_output = self.MODEL.generate(
            input_ids, 
            do_sample=True, 
            max_length=self.MAX_LENGTH, 
            top_k=0
        )

        decodedSamplingResult = []
        decodedSamplingResult.append(self.tokenizer.decode(sampling_output[0], skip_special_tokens=True))

        return decodedSamplingResult

    def _top_k_sampling_output(self, query):
        # encode context the generation is conditioned on
        startEncode = time.time()
        input_ids = self.tokenizer.encode(query, return_tensors='pt')
        endEncode = time.time()
        print(f"top-k encode time: {endEncode - startEncode}")

        # set seed to reproduce results. Feel free to change the seed though to get different results
        startSeed = time.time()
        set_seed(self.SEED)
        endSeed = time.time()
        print(f"top-k seed time: {endSeed - startSeed}")


        # set top_k to 50
        startGenerate = time.time()
        top_k_sampling_output = self.MODEL.generate(
            input_ids, 
            do_sample=True, 
            max_length=self.MAX_LENGTH, 
            top_k=50
        )
        endGenerate = time.time()
        print(f"top-k generate time: {endGenerate - startGenerate}")

        decodedTopKSamplingResult = []
        startDecode = time.time()
        decodedTopKSamplingResult.append(self.tokenizer.decode(top_k_sampling_output[0], skip_special_tokens=True))
        endDecode = time.time()
        print(f"top-k decode time: {endDecode - startDecode}")

        return decodedTopKSamplingResult

    def _top_p_sampling_output(self, query):
        # encode context the generation is conditioned on
        input_ids = self.tokenizer.encode(query, return_tensors='pt')

        # set seed to reproduce results. Feel free to change the seed though to get different results
        set_seed(self.SEED)

        # deactivate top_k sampling and sample only from 92% most likely words
        top_p_sampling_outputs = self.MODEL.generate(
            input_ids,
            do_sample=True, 
            max_length=self.MAX_LENGTH, 
            top_k=50, 
            top_p=0.92, 
            num_return_sequences=4
        )

        decodedTopPSamplingResult = []
        for output in top_p_sampling_outputs:
            decodedTopPSamplingResult.append(self.tokenizer.decode(output, skip_special_tokens=True))

        return decodedTopPSamplingResult


    
    
if __name__ == '__main__':
    gpt2 = Model_Gpt2()
    # gpt2.load_gpt2_using_model_mechanism()
    query1 = 'You '
    query2 = 'you'
    # prediction1 = gpt2.set_gpt2_method("top-p sampling", query1)
    # prediction2 = gpt2.set_gpt2_method("top-p sampling", query2)
    gpt2.set_gpt2_method("top-p sampling")
    predSentences = gpt2.generate_sentences(query2)
    print(f"predSentences = {predSentences}")

    predWords = gpt2.predict_words(query2)
    print(f"predWords = {predWords}")
    
    while True:
        query = input("Your query: ")
        predWords = gpt2.predict_words(query)
        for word in predWords:
            print(f"Pred word: {word}")
        predSentences = gpt2.generate_sentences(query)
        for sen in predSentences:
            print(f"Pred sen: {sen}")



