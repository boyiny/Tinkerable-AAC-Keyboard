from os import pread
from unittest.util import _MAX_LENGTH
from soupsieve import match
import torch
from transformers import pipelines, set_seed
from transformers import TFGPT2LMHeadModel, GPT2Tokenizer
from transformers import GPT2TokenizerFast, GPT2LMHeadModel
import transformers


class Model_Gpt2:

    WORD_PRED_NUM = 5
    MAX_LENGTH = 30

    def __init__(self):
        self.type = "default"

        # Using pipline by default
        self.generator = pipelines.pipeline(task='text-generation', model='gpt2', framework='pt')
        set_seed(32)

    def set_gpt2_method(self, type):
        """ Link the menu """        
        self.type = type
        self._load_gpt2_using_model_mechanism()

    def _load_gpt2_using_model_mechanism(self):
        # Load pre-trained model tokenizer (vocabulary)
        self.tokenizer = GPT2Tokenizer.from_pretrained('gpt2')

        # Load pre-trained model (weights)
        # add the EOS token as PAD token to avoid warnings
        self.model = GPT2LMHeadModel.from_pretrained('gpt2', pad_token_id=self.tokenizer.eos_token_id)

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
            if indexOfPeriod != -1 and indexOfPeriod < index:
                index = indexOfPeriod
            if indexOfComma != -1 and indexOfComma < index:
                index = indexOfComma
            if indexOfQuestionMark != -1 and indexOfQuestionMark < index:
                index = indexOfQuestionMark
            if indexOfExclamationMark != -1 and indexOfExclamationMark < index:
                index = indexOfExclamationMark
            singleSentence = result[0:index]
            oneSentenceList.append(singleSentence)
            # print(singleSentence)
        return oneSentenceList

    def _run_gpt2_method(self, query):
        results = []

        if self.type == "greedy":
            results = self._greedy_output(query)
        elif self.type == "beam":
            results = self._beam_output(query)
        elif self.type == "sampling":
            results = self._sampling_output(query)
        elif self.type == "top-k sampling": 
            results = self._top_k_sampling_output(query)
        elif self.type == "top-p sampling":
            results = self._top_p_sampling_output(query)
        elif self.type == "default":
            results = self._default_output(query)
        
        prediction = self._strip_one_sentence(results)
        
        return prediction


    def predict_words(self, query):
        query = query.strip()
        print(f"In gpt2 words, current entry is: '{query}'")
        predWords = []
        prediction = self._run_gpt2_method(query)
        
        predWords = self._pred_next_word(query, prediction)

        return predWords
    
    def predict_sentences(self, query):
        query = query.strip()
        print(f"In gpt2 sentences, current entry is: '{query}'")
        predSentences = []

        predSentences = self._run_gpt2_method(query)

        return predSentences


    def _greedy_output(self, query):
        
        # encode context the generation is conditioned on
        input_ids = self.tokenizer.encode(query, return_tensors='pt')

        # generate text until the output length (which includes the context length) reaches 50
        greedy_result = self.model.generate(input_ids, max_length=self.MAX_LENGTH, no_repeat_ngram_size=2)
        decodedGreedyResult = self.tokenizer.decode(greedy_result[0], skip_special_tokens=True)

        return decodedGreedyResult

    def _beam_output(self, query):
        # encode context the generation is conditioned on
        input_ids = self.tokenizer.encode(query, return_tensors='pt')

        # activate beam search and early_stopping
        beam_output = self.model.generate(
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
        set_seed(0)

        # activate sampling and deactivate top_k by setting top_k sampling to 0
        sampling_output = self.model.generate(
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
        input_ids = self.tokenizer.encode(query, return_tensors='pt')

        # set seed to reproduce results. Feel free to change the seed though to get different results
        set_seed(0)

        # set top_k to 50
        top_k_sampling_output = self.model.generate(
            input_ids, 
            do_sample=True, 
            max_length=self.MAX_LENGTH, 
            top_k=50
        )

        decodedTopKSamplingResult = []
        decodedTopKSamplingResult.append(self.tokenizer.decode(top_k_sampling_output[0], skip_special_tokens=True))

        return decodedTopKSamplingResult

    def _top_p_sampling_output(self, query):
        # encode context the generation is conditioned on
        input_ids = self.tokenizer.encode(query, return_tensors='pt')

        # set seed to reproduce results. Feel free to change the seed though to get different results
        set_seed(0)

        # deactivate top_k sampling and sample only from 92% most likely words
        top_p_sampling_outputs = self.model.generate(
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

    def _default_output(self, query):
        results = self.generator(query, max_length=30, num_return_sequence=5)
        defaultPredResult = []
        for res in results:
            sen = res.get('generated_text')
            defaultPredResult.append(sen) 

        return defaultPredResult

    
    
if __name__ == '__main__':
    gpt2 = Model_Gpt2()
    # gpt2.load_gpt2_using_model_mechanism()
    query1 = 'You '
    query2 = 'you'
    # prediction1 = gpt2.set_gpt2_method("top-p sampling", query1)
    # prediction2 = gpt2.set_gpt2_method("top-p sampling", query2)
    gpt2.set_gpt2_method("top-p sampling")
    predWords = gpt2.predict_words(query1)
    print(f"predWords = {predWords}")
    predSentences = gpt2.predict_sentences(query1)
    print(f"predSentences = {predSentences}")



    # gpt2.predict_words(query)

    # gpt2.predict_words(query2)
    
    # greedyPred = gpt2.greedy_output(query)
    # print(f"Greedy Result:\n{greedyPred}\n-------")

    # beamPred = gpt2.beam_output(query)
    # print(f"Beam Result:\n{beamPred}\n-------")

    # samplingPred = gpt2.sampling_output(query)
    # print(f"Sampling Result:\n{samplingPred}\n-------")

    # topKSamplingPred = gpt2.top_k_sampling_output(query)
    # print(f"Top-k Sampling Result:\n{topKSamplingPred}\n-------")

    # topPSamplingPred = gpt2.top_p_sampling_output(query)
    # print(f"Top-p Sampling Result:\n{topPSamplingPred}\n-------")



    # query = "You are a"
    # result = gpt2.predict(query)
    
    # query2 = "You are "
    # result2 = gpt2.predict(query2)

    
    # print(f"Result: {result2}")




# import torch
# from transformers import GPT2TokenizerFast, GPT2LMHeadModel

# # Load pre-trained model tokenizer (vocabulary)
# tokenizer = GPT2TokenizerFast.from_pretrained('./GPT2/GPT2Model')

# # Load pre-trained model (weights)
# model = GPT2LMHeadModel.from_pretrained('./GPT2/GPT2Model')

# # Set the model in evaluation mode to deactivate the DropOut modules
# # This is IMPORTANT to have reproducible results during evaluation!
# model.eval()

# # define a function to predict next word
# def PredNext(text):
#     #encode text inputs
#     indexed_tokens = tokenizer.encode(text)
    
#     # Convert indexed tokens in a PyTorch tensor
#     tokens_tensor = torch.tensor([indexed_tokens])
    
#     # Predict all tokens
#     with torch.no_grad():
#         outputs = model(tokens_tensor)
#         predictions = outputs[0]
        
#     top_preds = 1000
#     preds = []
    
#     predicted_indices = torch.argsort(predictions[0, -1, :], descending=True)

#     for i in range(top_preds):
#         predicted_index2 = predicted_indices[i].item()
#         predicted_text2 = tokenizer.decode([predicted_index2])
#         preds.append(predicted_text2)
        
#     return preds
