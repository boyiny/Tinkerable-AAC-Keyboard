import logging
import random
from argparse import ArgumentParser
from itertools import chain
from pprint import pformat
import warnings
import os

import torch
import torch.nn.functional as F

from transformers import OpenAIGPTLMHeadModel, OpenAIGPTTokenizer, GPT2LMHeadModel, GPT2Tokenizer
from model_kwickchat.model_utils import SPECIAL_TOKENS, build_input_from_segments, add_special_tokens_
from model_kwickchat.model_utils import download_pretrained_model
# from model_utils import SPECIAL_TOKENS, build_input_from_segments, add_special_tokens_
# from model_utils import download_pretrained_model

class Model_Kwickchat:
    PERSONA_NUM = 3

    OPTION = ''
    MAX_LENGTH = 20
    MIN_LENGTH = 1
    SEED = 0
    TEMPERATURE = 0.7
    TOP_K = 0
    TOP_P = 0.9
    NUM_OF_HISTORY_EXCHANGES = 3
    PERSONA = ''

    def __init__(self, option, max_length, min_length, seed, temperature, top_k, top_p, num_of_history_exchanges, persona):
        self.OPTION = option
        self.MAX_LENGTH = max_length
        self.MIN_LENGTH = min_length
        self.SEED = seed
        self.TEMPERATURE = temperature
        self.TOP_K = top_k
        self.TOP_P = top_p
        self.NUM_OF_HISTORY_EXCHANGES = num_of_history_exchanges
        self.PERSONA = persona

        self._setup_kwickchat()
        self._set_personas()

    def _top_filtering(self, logits, top_k=0., top_p=0.9, threshold=-float('Inf'), filter_value=-float('Inf')):
        """ Filter a distribution of logits using top-k, top-p (nucleus) and/or threshold filtering
            Args:
                logits: logits distribution shape (vocabulary size)
                top_k: <=0: no filtering, >0: keep only top k tokens with highest probability.
                top_p: <=0.0: no filtering, >0.0: keep only a subset S of candidates, where S is the smallest subset
                    whose total probability mass is greater than or equal to the threshold top_p.
                    In practice, we select the highest probability tokens whose cumulative probability mass exceeds
                    the threshold top_p.
                threshold: a minimal threshold to keep logits
        """
        assert logits.dim() == 1  # Only work for batch size 1 for now - could update but it would obfuscate a bit the code
        top_k = min(top_k, logits.size(-1))
        if top_k > 0:
            # Remove all tokens with a probability less than the last token in the top-k tokens
            indices_to_remove = logits < torch.topk(logits, top_k)[0][..., -1, None]
            logits[indices_to_remove] = filter_value

        if top_p > 0.0:
            # Compute cumulative probabilities of sorted tokens
            sorted_logits, sorted_indices = torch.sort(logits, descending=True)
            cumulative_probabilities = torch.cumsum(F.softmax(sorted_logits, dim=-1), dim=-1)

            # Remove tokens with cumulative probability above the threshold
            sorted_indices_to_remove = cumulative_probabilities > top_p
            # Shift the indices to the right to keep also the first token above the threshold
            sorted_indices_to_remove[..., 1:] = sorted_indices_to_remove[..., :-1].clone()
            sorted_indices_to_remove[..., 0] = 0

            # Back to unsorted indices and set them to -infinity
            indices_to_remove = sorted_indices[sorted_indices_to_remove]
            logits[indices_to_remove] = filter_value

        indices_to_remove = logits < threshold
        logits[indices_to_remove] = filter_value

        return logits


    def _sample_sequence(self, personality, history, tokenizer,key_phrase,model, args, current_output=None):
        special_tokens_ids = tokenizer.convert_tokens_to_ids(SPECIAL_TOKENS)
        if current_output is None:
            current_output = []

        for i in range(args.max_length):
            instance = build_input_from_segments(personality, history, current_output, tokenizer, key_phrase, with_eos=False)

            input_ids = torch.tensor(instance["input_ids"], device=args.device).unsqueeze(0)
            token_type_ids = torch.tensor(instance["token_type_ids"], device=args.device).unsqueeze(0)

            logits = model(input_ids, token_type_ids=token_type_ids)
            # if isinstance(logits, tuple):  # for gpt2 and maybe others
            logits = logits[0]
            logits = logits[0, -1, :] / args.temperature
            logits = self._top_filtering(logits, top_k=args.top_k, top_p=args.top_p)
            probs = F.softmax(logits, dim=-1)

            prev = torch.topk(probs, 1)[1] if args.no_sample else torch.multinomial(probs, 1)
            if i < args.min_length and prev.item() in special_tokens_ids:
                while prev.item() in special_tokens_ids:
                    if probs.max().item() == 1:
                        warnings.warn("Warning: model generating special token with probability 1.")
                        break  # avoid infinitely looping over special token
                    prev = torch.multinomial(probs, num_samples=1)

            if prev.item() in special_tokens_ids:
                break
            current_output.append(prev.item())

        return current_output

    def _run(self):
        rootDir = os.path.realpath(os.path.join(os.path.dirname(__file__), '../Model/KwickChat'))
        parser = ArgumentParser()
        parser.add_argument("--dataset_path", type=str, default="", help="Path or url of the dataset. If empty download from S3.")
        parser.add_argument("--dataset_cache", type=str, default='./dataset_cache', help="Path or url of the dataset cache")
        parser.add_argument("--model", type=str, default="openai-gpt", help="Model type (openai-gpt or gpt2)", choices=['openai-gpt', 'gpt2'])
        parser.add_argument("--model_checkpoint", type=str,
                            default=rootDir,
                            help="Path, url or short name of the model")
        #train a larger one
        parser.add_argument("--max_history", type=int, default=2, help="Number of previous utterances to keep in history")
        parser.add_argument("--device", type=str, default="cpu" if torch.cuda.is_available() else "cpu", help="Device (cuda or cpu)")

        parser.add_argument("--no_sample", action='store_true', help="Set to use greedy decoding instead of sampling")
        parser.add_argument("--max_length", type=int, default=20, help="Maximum length of the output utterances")
        parser.add_argument("--min_length", type=int, default=1, help="Minimum length of the output utterances")
        parser.add_argument("--seed", type=int, default=0, help="Seed")
        parser.add_argument("--temperature", type=float, default=0.7, help="Sampling softmax temperature")
        parser.add_argument("--top_k", type=int, default=0, help="Filter top-k tokens before sampling (<=0: no filtering)")
        parser.add_argument("--top_p", type=float, default=0.9, help="Nucleus filtering (top-p) before sampling (<=0.0: no filtering)")
        parser.add_argument("--num_suggestions", type=int, default=4,
                            help="Number of sentence suggestions")
        args = parser.parse_args()

        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__file__)
        logger.info(pformat(args))

        if args.model_checkpoint == "":
            if args.model == 'gpt2':
                raise ValueError("Interacting with GPT2 requires passing a finetuned model_checkpoint")
            else:
                args.model_checkpoint = download_pretrained_model()
        
        
        if args.seed != 0:
            random.seed(args.seed)
            torch.random.manual_seed(args.seed)
            torch.cuda.manual_seed(args.seed)


        logger.info("Get pretrained model and tokenizer")
        tokenizer_class, model_class = (GPT2Tokenizer, GPT2LMHeadModel) if args.model == 'gpt2' else (OpenAIGPTTokenizer, OpenAIGPTLMHeadModel)
        tokenizer = tokenizer_class.from_pretrained(args.model_checkpoint)
        model = model_class.from_pretrained(args.model_checkpoint)
        model.to(args.device)
        add_special_tokens_(model, tokenizer)

        # logger.info("Sample a personality")
        # dataset = get_dataset(tokenizer, args.dataset_path, args.dataset_cache)
        # personalities = [dialog["personality"] for dataset in dataset.values() for dialog in dataset]
        # personality = random.choice(personalities)


        history = []

        personality = []
        num_personas = input('please enter the number of personas (at least 1): >>>')
        for i in range(int(num_personas)):
            persona = input('enter persona {}: >>>'.format(i))
            personality.append(tokenizer.encode(persona))

        while True:

            raw_text = input("Speaking Partner >>> ")
            raw_text_key = input("Your Key Words >>> ")
            while not raw_text:
                print('Prompt should not be empty!')
                raw_text = input("Alan >>> ")
            while not raw_text_key:
                print('Prompt should not be empty!')
                raw_text_key = input("Key Words >>> ")

            history.append(tokenizer.encode(raw_text))
            key_phrase=[tokenizer.encode(raw_text_key)]
            # print(history)
            # print(key_phrase)
            # break

            out_idx_list = []
            out_text_list = []
            for seed in range(args.num_suggestions):
                random.seed(seed)
                torch.random.manual_seed(seed)
                torch.cuda.manual_seed(seed)

                with torch.no_grad():
                    out_ids = self._sample_sequence(personality, history, tokenizer, key_phrase, model, args)

                out_text = tokenizer.decode(out_ids, skip_special_tokens=True)
                print("Suggested Reply {} >>> {}".format(seed,out_text))
                out_idx_list.append(out_ids)
                out_text_list.append(out_text)

            select_idx = int(input("Your Selection >>> "))
            print("Your Reply >>> {}".format(out_text_list[select_idx]))

            history.append(out_idx_list[select_idx])
            history = history[-(2*args.max_history+1):]


    def _setup_kwickchat(self):
        rootDir = os.path.realpath(os.path.join(os.path.dirname(__file__), '../Model/KwickChat'))
        print(f"KwickChat model path: {rootDir}")
        parser = ArgumentParser()
        parser.add_argument("--dataset_path", type=str, default="", help="Path or url of the dataset. If empty download from S3.")
        parser.add_argument("--dataset_cache", type=str, default='./dataset_cache', help="Path or url of the dataset cache")
        parser.add_argument("--model", type=str, default="openai-gpt", help="Model type (openai-gpt or gpt2)", choices=['openai-gpt', 'gpt2'])
        parser.add_argument("--model_checkpoint", type=str,
                            default=rootDir,
                            help="Path, url or short name of the model")
        #train a larger one
        parser.add_argument("--max_history", type=int, default=2, help="Number of previous utterances to keep in history")
        parser.add_argument("--device", type=str, default="cpu" if torch.cuda.is_available() else "cpu", help="Device (cuda or cpu)")

        parser.add_argument("--no_sample", action='store_true', help="Set to use greedy decoding instead of sampling")
        parser.add_argument("--max_length", type=int, default=self.MAX_LENGTH, help="Maximum length of the output utterances")
        parser.add_argument("--min_length", type=int, default=self.MIN_LENGTH, help="Minimum length of the output utterances")
        parser.add_argument("--seed", type=int, default=self.SEED, help="Seed")
        parser.add_argument("--temperature", type=float, default=self.TEMPERATURE, help="Sampling softmax temperature")
        parser.add_argument("--top_k", type=int, default=self.TOP_K, help="Filter top-k tokens before sampling (<=0: no filtering)")
        parser.add_argument("--top_p", type=float, default=self.TOP_P, help="Nucleus filtering (top-p) before sampling (<=0.0: no filtering)")
        parser.add_argument("--num_suggestions", type=int, default=4,
                            help="Number of sentence suggestions")
        self.args = parser.parse_args()

        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__file__)
        logger.info(pformat(self.args))

        if self.args.model_checkpoint == "":
            if self.args.model == 'gpt2':
                raise ValueError("Interacting with GPT2 requires passing a finetuned model_checkpoint")
            else:
                self.args.model_checkpoint = download_pretrained_model()
        
        if self.args.seed != 0:
            random.seed(self.args.seed)
            torch.random.manual_seed(self.args.seed)
            torch.cuda.manual_seed(self.args.seed)


        logger.info("Get pretrained model and tokenizer")
        tokenizer_class, model_class = (GPT2Tokenizer, GPT2LMHeadModel) if self.args.model == 'gpt2' else (OpenAIGPTTokenizer, OpenAIGPTLMHeadModel)
        self.tokenizer = tokenizer_class.from_pretrained(self.args.model_checkpoint)
        self.model = model_class.from_pretrained(self.args.model_checkpoint)
        self.model.to(self.args.device)
        add_special_tokens_(self.model, self.tokenizer)

    def _set_personas(self):
        self.personality = []
        for persona in self.PERSONA:
            self.personality.append(self.tokenizer.encode(persona))


    def generate_sentences(self, history, keyWords):
        encodedHistory = []

        for his in history:
            encodedHistory.append(self.tokenizer.encode(his))

        
        key_phrase=[self.tokenizer.encode(keyWords)]
        # print(encodedHistory)
        # print(key_phrase)
        # break

        out_idx_list = []
        out_text_list = []
        for seed in range(self.args.num_suggestions):
            random.seed(seed)
            torch.random.manual_seed(seed)
            torch.cuda.manual_seed(seed)

            with torch.no_grad():
                out_ids = self._sample_sequence(self.personality, encodedHistory, self.tokenizer, key_phrase, self.model, self.args)

            out_text = self.tokenizer.decode(out_ids, skip_special_tokens=True)
            out_idx_list.append(out_ids)
            out_text_list.append(out_text)


        return out_text_list

    def adjust_history_size(self, history):
        self.args.max_history = self.NUM_OF_HISTORY_EXCHANGES
        newHistory = history[-(2*self.NUM_OF_HISTORY_EXCHANGES+1):]

        return newHistory

    

if __name__ == "__main__":
    max_length = 21
    min_length = 1
    seed = 0
    temperature = 0.7
    top_k = 0
    top_p = 0.9
    num_of_history_exchanges = 3
    persona = ['student', 'phd', 'hci']
    option = 'SENTENCE_KWICKCHAT'
    kwickChat = Model_Kwickchat(option, max_length, min_length, seed, temperature, top_k, top_p, num_of_history_exchanges, persona)
    # kwickChat.run()
    # kwickChat._setup_kwickchat()
    
    # personas = []
    # for i in range(kwickChat.PERSONA_NUM):
    #     persona = input(f"Input your persona {i}: ")
    #     personas.append(persona)

    # kwickChat._set_personas(persona)
    
    predSentences = []
    history = []
    while True:
        partnerInput = input("Conversation partener: ")
        keywords = input("Input your keywords: ")
        history.append(partnerInput)
        senPred = kwickChat.generate_sentences(history, keywords)
        for sen in senPred:
            print(sen)
        # edit_sentence()
        userInput = input("Edit your input: ")
        history.append(userInput)

        history = kwickChat.adjust_history_size(history)
        print(f"History size: {len(history)}")


        