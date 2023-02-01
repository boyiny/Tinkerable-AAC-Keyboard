
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
        self.base_prompt = (
            os.environ.get("CUSTOM_BASE_PROMPT")
            or "You are ChatGPT, a large language model trained by OpenAI. You try to answer concisely for each response (e.g. Don't be overly verbose).\n"
        )
        # Track chat history

        self.chat_history: list = []

    def add_to_chat_history(self, chat: str) -> None:
        """
        Add chat to chat history for next prompt
        """
        self.chat_history.append(chat)

    def history(self) -> str:
        """
        Return chat history
        """
        return "\n\n\n\n".join(self.chat_history)

    def construct_prompt(self, new_prompt: str) -> str:
        """
        Construct prompt based on chat history and request
        """
        # prompt = (
            # self.base_prompt + self.history() + "User: " + new_prompt + "\nChatGPT:"
        # )
        prompt = (
                self.base_prompt + "User: " + new_prompt + "\nChatGPT:"
        )
        # Check if prompt over 4000*4 characters
        if len(prompt) > 4000 * 4:
            # Remove oldest chat
            self.chat_history.pop(0)
            # Construct prompt again
            prompt = self.construct_prompt(new_prompt)
        return prompt



    def prompt_geneator(self, query,history):
        combo_prompt = f"A user is having conversation with ones speaking partner. Given the user's input: {query}, Given a conversation history between the user and the user's speaking partner: {history}. You need to predict the user's reply based on user's inputs so that the reply has to be contain the keywords and the conversation history. Please predict this reply (only output one sentence):"
        # combo_prompt = f"You are a text prediction robot for a user. Given the user's input: {query}. You need to generate a sentence based on user's inputs. Please predict this sentence (only output one sentence):"

        return self.construct_prompt(combo_prompt)





class Model_Gpt:

    SYMBOLS = "!@#$%^&*()_-+=`~\{\};':\",./<>?\|\n"

    def __init__(self, option):
        self.OPTION = option
        self.api_key = "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"
        self.engine = "text-chat-davinci-002-20230126"
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

        completion = openai.Completion.create(
            engine=self.engine,
            prompt=prompt,
            temperature=0.2,
            max_tokens=64,
            stop=["\n\n\n"],
        )
        if completion.get("choices") is None:
            raise Exception("ChatGPT API returned no choices")
        if len(completion["choices"]) == 0:
            raise Exception("ChatGPT API returned no choices")
        if completion["choices"][0].get("text") is None:
            raise Exception("ChatGPT API returned no text")
        completion["choices"][0]["text"] = completion["choices"][0]["text"].replace(
            "<|im_end|>",
            "",
        )
        # Add to chat history
        self.prompt.add_to_chat_history(
            "User: "
            + prompt
            + "\n\n\n"
            + "ChatGPT: "
            + completion["choices"][0]["text"]
            + "\n\n\n",
        )
        return completion

    def _run_gpt_method(self, prompt):
        prediction = []
        for i in range(1):
            response = self._ask(prompt)
            prediction.append(response["choices"][0]["text"])
        # completion = self._ask(prompt)
        # response = completion["choices"][0]["text"]

        return prediction

    def predict_words(self, query):
        #encode text inputs
        query = query.strip()
        history = ""
        prompt = self.prompt.prompt_geneator(query,history)

        predWords = self._run_gpt_method(prompt)
            
        return predWords

    
    def generate_sentences(self, history,query):
        query = query.strip()

        predSentences = []
        
        if query != "":
            prompt = self.prompt.prompt_geneator(query,history)
            predSentences = self._run_gpt_method(prompt)

        return predSentences

    def adjust_history_size(self, history):
        self.max_history = self.NUM_OF_HISTORY_EXCHANGES
        newHistory = history[-(2*self.NUM_OF_HISTORY_EXCHANGES+1):]

        return newHistory



    
    
if __name__ == '__main__':
    gpt = Model_Gpt(option="GPT")
    query1 = 'b u r '
    query2 = 'great burger'
    history = ""
    predWords = gpt.predict_words(history,query1)
    print(f"predWords = {predWords}")

    predSentences = gpt.generate_sentences(history,query2)
    print(f"predSentences = {predSentences}")


    
    # while True:
    #     query = input("Your query: ")
    #     predWords = gpt.predict_words(query)
    #     for word in predWords:
    #         print(f"Pred word: {word}")
    #     predSentences = gpt.generate_sentences(query)
    #     for sen in predSentences:
    #         print(f"Pred sen: {sen}")



