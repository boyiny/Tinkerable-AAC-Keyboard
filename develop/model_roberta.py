from transformers import pipelines
from transformers import RobertaTokenizer, RobertaForMaskedLM
import torch


class Model_Roberta:
    def __init__(self):
        self.unmasker = pipelines.pipeline('fill-mask', model='roberta-base')

        self.tokenizer = RobertaTokenizer.from_pretrained('roberta-base')
        self.model = RobertaForMaskedLM.from_pretrained('roberta-base')
        

    def predict_next_few_words (self, sent, num):

        for i in range(num):
            sent = sent + "<mask>"
    
        token_ids = self.tokenizer.encode(sent, return_tensors='pt')
        masked_position = (token_ids.squeeze() == self.tokenizer.mask_token_id).nonzero()
        masked_pos = [mask.item() for mask in masked_position ]

        with torch.no_grad():
            output = self.model(token_ids)

        last_hidden_state = output[0].squeeze()

        list_of_list =[]
        for index, mask_index in enumerate(masked_pos):
            mask_hidden_state = last_hidden_state[mask_index]
            idx = torch.topk(mask_hidden_state, k=5, dim=0)[1]
            words = [self.tokenizer.decode(i.item()).strip() for i in idx]
            list_of_list.append(words)
            print ("Mask ",index+1,"Guesses : ",words)
        
        best_guess = ""
        for j in list_of_list:
            best_guess = best_guess+" "+j[0]
            
        return best_guess

    def predict_next_word(self, query):
        text = query + "<mask>"
        result = self.unmasker(text)
        return result


if __name__ == '__main__':
    roberta = Model_Roberta()
    query = "windy London"
    result = roberta.predict_next_word(query)
    for res in result:
        print(f"First pred: {res}")

    query = "merry christmas"
    result = roberta.predict(query)
    for res in result:
        print(f"Second pred: {res}")

    
    sentence = "windy London"
    numOfPredWords = 3

    predicedSentence = roberta.get_prediction(sentence, numOfPredWords)
    print ("\nBest guess for fill in the blank :::", predicedSentence)

















