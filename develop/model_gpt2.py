import torch
from transformers import pipelines, set_seed
from transformers import TFGPT2LMHeadModel, GPT2Tokenizer
from transformers import GPT2TokenizerFast, GPT2LMHeadModel


class Model_Gpt2:

    WORD_PRED_NUM = 5

    def __init__(self):
        # self.generator = pipelines.pipeline('text-generation', model='gpt2')
        # set_seed(32)

        # Load pre-trained model tokenizer (vocabulary)
        self.tokenizer = GPT2Tokenizer.from_pretrained('gpt2')

        # Load pre-trained model (weights)
        # add the EOS token as PAD token to avoid warnings
        self.model = GPT2LMHeadModel.from_pretrained('gpt2', pad_token_id=self.tokenizer.eos_token_id)

               

    def get_next_word(self, text):
        next_word = text

    def greedy_output(self, query):
        
        # encode context the generation is conditioned on
        input_ids = self.tokenizer.encode(query, return_tensors='pt')

        # generate text until the output length (which includes the context length) reaches 50
        greedy_result = self.model.generate(input_ids, max_length=50, no_repeat_ngram_size=2)
        decodedGreedyResult = self.tokenizer.decode(greedy_result[0], skip_special_tokens=True)

        return decodedGreedyResult

    def beam_output(self, query):
        # encode context the generation is conditioned on
        input_ids = self.tokenizer.encode(query, return_tensors='pt')

        # activate beam search and early_stopping
        beam_output = self.model.generate(
            input_ids, 
            max_length=50, 
            num_beams=5, 
            no_repeat_ngram_size=2, 
            early_stopping=True
        )
        decodedBeamResult = self.tokenizer.decode(beam_output[0], skip_special_tokens=True)

        return decodedBeamResult

    def sampling_output(self, query):
        # encode context the generation is conditioned on
        input_ids = self.tokenizer.encode(query, return_tensors='pt')

        # set seed to reproduce results. Feel free to change the seed though to get different results
        set_seed(0)

        # activate sampling and deactivate top_k by setting top_k sampling to 0
        sampling_output = self.model.generate(
            input_ids, 
            do_sample=True, 
            max_length=50, 
            top_k=0
        )

        decodedSamplingResult = self.tokenizer.decode(sampling_output[0], skip_special_tokens=True)

        return decodedSamplingResult

    def top_k_sampling_output(self, query):
        # encode context the generation is conditioned on
        input_ids = self.tokenizer.encode(query, return_tensors='pt')

        # set seed to reproduce results. Feel free to change the seed though to get different results
        set_seed(0)

        # set top_k to 50
        top_k_sampling_output = self.model.generate(
            input_ids, 
            do_sample=True, 
            max_length=50, 
            top_k=50
        )

        decodedTopKSamplingResult = self.tokenizer.decode(top_k_sampling_output[0], skip_special_tokens=True)

        return decodedTopKSamplingResult

    def top_p_sampling_output(self, query):
        # encode context the generation is conditioned on
        input_ids = self.tokenizer.encode(query, return_tensors='pt')

        # set seed to reproduce results. Feel free to change the seed though to get different results
        set_seed(0)

        # deactivate top_k sampling and sample only from 92% most likely words
        top_p_sampling_outputs = self.model.generate(
            input_ids,
            do_sample=True, 
            max_length=50, 
            top_k=50, 
            top_p=0.95, 
            num_return_sequences=3
        )

        decodedTopPSamplingResult = []
        for output in top_p_sampling_outputs:
            decodedTopPSamplingResult.append(self.tokenizer.decode(output, skip_special_tokens=True))

        return decodedTopPSamplingResult

    def predict_words(self, entry):
        predWords = []
        return predWords
    
    def predict_sentences(self, entry):
        predSentences = []
        return predSentences
    
if __name__ == '__main__':
    gpt2 = Model_Gpt2()
    query = 'I enjoy'
    greedyPred = gpt2.greedy_output(query)
    print(f"Greedy Result:\n{greedyPred}\n-------")

    beamPred = gpt2.beam_output(query)
    print(f"Beam Result:\n{beamPred}\n-------")

    samplingPred = gpt2.sampling_output(query)
    print(f"Sampling Result:\n{samplingPred}\n-------")

    topKSamplingPred = gpt2.top_k_sampling_output(query)
    print(f"Top-k Sampling Result:\n{topKSamplingPred}\n-------")

    topPSamplingPred = gpt2.top_p_sampling_output(query)
    print(f"Top-p Sampling Result:\n{topPSamplingPred}\n-------")



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
