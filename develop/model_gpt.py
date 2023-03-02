
import os
import openai

class Prompt:
    """
    Prompt class with methods to construct prompt
    """

    def __init__(self) -> None:
        """
        Initialize prompt with base prompt
        """
        # self.base_prompt = (
        #     os.environ.get("CUSTOM_BASE_PROMPT")
        #     or "You are ChatGPT, a large language model trained by OpenAI. You try to answer concisely for each response (e.g. Don't be overly verbose).\n"
        # )
        # Track chat history

        self.chat_history = [
            {"role": "system", "content": "Your goal is to predict the response for a given user query based on the previous conversational history and the previous question. Please read the following user query and history carefully, and generate a response that is relevant and coherent. Your response should be in natural language and aim to provide value to the user. We appreciate your help in improving our language model's ability to assist users in various contexts. Below are the examples:"},
            {"role": "user", "content": "Given question: I'm having trouble with my account. Can you help me reset my password? Given the user's input: email address, predict the response."},
            {"role": "assistant", "content": "Sure, I can help you reset your password. First, please provide me with your email address and any other relevant information."}
        ]

        # self.chat_history = []

    def add_to_chat_history(self, chat):
        """
        Add chat to chat history for next prompt
        """
        self.chat_history.append(chat)

    # def history(self) -> str:
    #     """
    #     Return chat history
    #     """
    #     return "\n\n\n\n".join(self.chat_history)

    def construct_prompt(self, new_prompt: str):
        """
        Construct prompt based on chat history and request
        """
        # prompt = (
            # self.base_prompt + self.history() + "User: " + new_prompt + "\nChatGPT:"
        # )
        # prompt = (
        #         self.base_prompt + "User: " + new_prompt + "\nChatGPT:"
        # )

        self.chat_history.append(
            {"role": "user", "content": new_prompt},
        )
        print(f"prompt is {self.chat_history}")


        # Check if prompt over 4000*4 characters
        # if len(self.chat_history) > 4000 * 4:
        #     # Remove oldest chat
        #     self.chat_history.pop(0)
        #     # Construct prompt again
        #     self.construct_prompt(new_prompt)
        return self.chat_history



    def prompt_geneator(self, question, query):
        combo_prompt = f"Given question: {question}, Given the user's input: {query}, predict the response."
        # combo_prompt = f"You are a text prediction robot for a user. Given the user's input: {query}. You need to generate a sentence based on user's inputs. Please predict this sentence (only output one sentence):"

        return self.construct_prompt(combo_prompt)





class Model_Gpt:

    SYMBOLS = "!@#$%^&*()_-+=`~\{\};':\",./<>?\|\n"

    def __init__(self, option):
        self.OPTION = option
        self.api_key = "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"
        self.engine = "gpt-3.5-turbo"
        # self.engine = "text-chat-davinci-002-20221122"
        # if "WORD" in option:

        #     self.engine = engine
        # elif "SENTENCE" in option:

        # self.engine = "text-chat-davinci-002-20230126"

        
        self.prompt = Prompt()
        openai.api_key = self.api_key or os.environ.get("OPENAI_API_KEY")
        self.NUM_OF_HISTORY_EXCHANGES = 4



    def _ask(self, prompt):
        """
        Send a request to ChatGPT and return the response
        Response: {
            "id": "...",
            "object": "text_completion",
            "created": <time>,
            "model": "text-chat-davinci-002-20230126",
            "choices": [
                {
                "text": "<Response here>",
                "index": 0,
                "logprobs": null,
                "finish_details": { "type": "stop", "stop": "<|endoftext|>" }
                }
            ],
            "usage": { "prompt_tokens": x, "completion_tokens": y, "total_tokens": z }
        }
        """



        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=prompt
        )
        reply = chat.choices[0].message.content


        # completion = openai.Completion.create(
        #     engine=self.engine,
        #     prompt=prompt,
        #     temperature=0.2,
        #     max_tokens=64,
        #     stop=["\n\n\n"],
        # )
        # if completion.get("choices") is None:
        #     raise Exception("ChatGPT API returned no choices")
        # if len(completion["choices"]) == 0:
        #     raise Exception("ChatGPT API returned no choices")
        # if completion["choices"][0].get("text") is None:
        #     raise Exception("ChatGPT API returned no text")
        # completion["choices"][0]["message"]["content"] = completion["choices"][0]["text"].replace(
        #     "<|im_end|>",
        #     "",
        # )
        # Add to chat history
        self.prompt.add_to_chat_history(
            {"role": "assistant", "content": reply}
        )
        return chat

    def _run_gpt_method(self, prompt):
        prediction = []
        for i in range(1):
            response = self._ask(prompt)
            prediction.append(response.choices[0].message.content)
        # completion = self._ask(prompt)
        # response = completion["choices"][0]["text"]

        return prediction

    def predict_words(self,question, query):
        #encode text inputs
        query = query.strip()
        # question = ""
        prompt = self.prompt.prompt_geneator(question,query)

        predWords = self._run_gpt_method(prompt)
            
        return predWords

    
    def generate_sentences(self, question,query):
        query = query.strip()

        predSentences = []
        
        if query != "":
            prompt = self.prompt.prompt_geneator(question,query)
            predSentences = self._run_gpt_method(prompt)

        return predSentences

    def adjust_history_size(self, history):
        self.max_history = self.NUM_OF_HISTORY_EXCHANGES
        newHistory = history[-(2*self.NUM_OF_HISTORY_EXCHANGES+1):]

        return newHistory



    
    
if __name__ == '__main__':
    gpt = Model_Gpt(option="GPT")
    query1 = 'b u r '
    query2 = 'order number and photo'
    question = "I received a damaged product. What should I do?"
    # predWords = gpt.predict_words(question,query1)
    # print(f"predWords = {predWords}")

    predSentences = gpt.generate_sentences(question,query2)
    print(f"predSentences = {predSentences}")


    
    # while True:
    #     query = input("Your query: ")
    #     predWords = gpt.predict_words(query)
    #     for word in predWords:
    #         print(f"Pred word: {word}")
    #     predSentences = gpt.generate_sentences(query)
    #     for sen in predSentences:
    #         print(f"Pred sen: {sen}")



