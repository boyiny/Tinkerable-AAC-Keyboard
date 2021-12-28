from transformers import pipelines, set_seed

class Model_Gpt2:

    WORD_PRED_NUM = 5

    def __init__(self):
        self.generator = pipelines.pipeline('text-generation', model='gpt2')
        set_seed(32)
        

    def get_next_word(self, text):
        next_word = text

    def predict(self, query):
        result = self.generator(query, max_length=30, num_return_sequence=5)
        return result
    
if __name__ == '__main__':
    gpt2 = Model_Gpt2()
    query = "It is a "
    result = gpt2.predict(query)
    
    query2 = "That "
    result2 = gpt2.predict(query2)

    print(f"Result: {result}")
    print(f"Result: {result2}")




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
