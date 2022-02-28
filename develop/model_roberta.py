from transformers import pipelines
from transformers import RobertaTokenizer, RobertaForMaskedLM
import torch
import re


class Model_Roberta:
    

    def __init__(self, option, model):
        self.OPTION = option
        print(f"Word pred with {self.OPTION}, model: {model}")
        if "WORD" in self.OPTION:
            self.MODEL = model #'roberta-base'
            self.load_roberta()
        

        # self.tokenizer = RobertaTokenizer.from_pretrained('roberta-base')
        # self.model = RobertaForMaskedLM.from_pretrained('roberta-base')
        # ,, , , , "Please input..."
        
    def load_roberta(self):
        if self.MODEL == 'distilroberta-base' or self.MODEL == 'roberta-base' or self.MODEL == 'roberta-large' or self.MODEL == 'xlm-roberta-base' or self.MODEL == 'xlm-roberta-large':
            self.unmasker = pipelines.pipeline('fill-mask', model=self.MODEL)
        else: 
            # TODO check input model is valid
            self.unmasker = pipelines.pipeline('fill-mask', model='roberta-base')


        # if self.MODEL == 'roberta-base':
        #     self.unmasker = pipelines.pipeline('fill-mask', model='roberta-base')
        # elif self.MODEL == 'roberta-large':
        #     self.unmasker = pipelines.pipeline('fill-mask', model='roberta-large')
        # elif self.MODEL == 'xlm-roberta-base':
        #     self.unmasker = pipelines.pipeline('fill-mask', model='xlm-roberta-base')
        # elif self.MODEL == 'distilroberta-base':
        #     self.unmasker = pipelines.pipeline('fill-mask', model='roberta-base')

        # else: 
        #     self.unmasker = pipelines.pipeline('fill-mask', model='roberta-base')

    # def predict_next_few_words(self, sent, num):

    #     for i in range(num):
    #         sent = sent + "<mask>"
    
    #     token_ids = self.tokenizer.encode(sent, return_tensors='pt')
    #     masked_position = (token_ids.squeeze() == self.tokenizer.mask_token_id).nonzero()
    #     masked_pos = [mask.item() for mask in masked_position ]

    #     with torch.no_grad():
    #         output = self.model(token_ids)

    #     last_hidden_state = output[0].squeeze()

    #     list_of_list =[]
    #     for index, mask_index in enumerate(masked_pos):
    #         mask_hidden_state = last_hidden_state[mask_index]
    #         idx = torch.topk(mask_hidden_state, k=100, dim=0)[1]
    #         words = [self.tokenizer.decode(i.item()).strip() for i in idx]
    #         list_of_list.append(words)
    #         # print ("Mask ",index+1,"Guesses : ",words)
        
    #     best_guess = ""
    #     for j in list_of_list:
    #         best_guess = best_guess+" "+j[0]
            
    #     return best_guess

    def predict_words(self, query):
        text = query + "<mask>"
        # inputs = self.tokenizer(text, return_tensors="pt")
        # results = self.model(**inputs)
        results = self.unmasker(text)
        wordsPred = []
        for element in results:
            elementWithoutSymbol = re.sub(r'[^\w]', '', element['token_str'])
            if elementWithoutSymbol != '':
                wordsPred.append(elementWithoutSymbol)
        return wordsPred


if __name__ == '__main__':
    roberta = Model_Roberta()
    query = "windy London"
    result = roberta.predict_words(query)
    for res in result:
        print(f"First pred: {res}")

    query = "merry christmas"
    result = roberta.predict_words(query)
    for res in result:
        print(f"Second pred: {res}")

    
    sentence = "windy London"
    numOfPredWords = 3

    # predicedSentence = roberta.predict_next_few_words(sentence, numOfPredWords)
    # print ("\nBest guess for fill in the blank :::", predicedSentence)

    while(True):
        query = input("Input your query: ")
        wordsPred = roberta.predict_words(query)
        print(f"Result: {wordsPred}")















