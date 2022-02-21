from cProfile import label
from os import stat
import tkinter as tk
from tkinter import BOTTOM, ttk

from click import command
from gevent import config
from sympy import per

import configparser 
import os


class View_tinker:
    WORD_PRED_NUM = [1,2,3,4]
    WORD_DISP_LOC = ["Fixed", "Above last pressed key"]
    WORD_PRED_METHOD = ["BM25Okpi", "BM25L", "BM25Plus", "GPT-2", "RoBERTa"]
    
    K1_BM25OKPI = 1.5
    B_BM25OKPI = 0.75
    EPSILON_BM25OKPI = 0.25

    K1_BM25L = 1.5
    B_BM25L = 0.75
    DELTA_BM25L = 0.5
    
    K1_BM25PLUS = 1.5
    B_BM25PLUS = 0.75
    DELTA_BM25PLUS = 1.0

    MODEL_GPT2 = ["distilgpt2", "gpt2", "gpt2-medium", "gpt2-large", "gpt2-xl", "Please input..."]

    MODEL_ROBERTA = ["distilroberta-base","roberta-base", "roberta-large", "xlm-roberta-base", "xlm-roberta-large", "Please input..."]
    

    SEN_PRED_NUM = [1,2,3,4]
    SEN_ENTRY_APPROACH = ["Left to right", "Keywords"]
    SEN_PRED_APPROACH = ["Retrieval", "Generation"]
    SEN_SIMILARITY = ["Text", "Semantics"]
    SEN_RETRI_TEXT_METHOD = ["BM25Okpi", "BM25L", "BM25Plus"]
    SEN_RETRI_SEMAN_MODEL = ["all-mpnet-base-v2", "multi-qa-mpnet-base-dot-v1", "all-distilroberta-v1", "all-MiniLM-L12-v2", "multi-qa-distilbert-cos-v1", "all-MiniLM-L6-v2", "multi-qa-MiniLM-L6-cos-v1", "paraphrase-multilingual-mpnet-base-v2", "paraphrase-albert-small-v2", "paraphrase-multilingual-MiniLM-L12-v2", "paraphrase-MiniLM-L3-v2", "distiluse-base-multilingual-cased-v1", "distiluse-base-multilingual-cased-v2", "Please input..."]
    SEN_GEN_METHOD = ["KWickChat", "GPT-2"]
    SEN_KW_HISTORY_NUM = 3
    SEN_KW_PERSONA_NUM = 3
    SEN_GPT2_APPROACH = ["Greedy search", "Beam search", "Top-k sampling", "Top-p sampling"]
    GPT2_MAX_LENGTH = 30
    GPT2_NO_REPEAT_NGRAM_SIZE = 2
    GPT2_NUM_BEAMS = 5
    GPT2_SEED = 0
    GPT2_TOP_K = 50
    GPT2_TOP_P = 0.92

    lastPersonaNum = 1

    WORD_PRED_TASK = ""
    SENTENCE_PRED_TASK = ""

    def __init__(self):
        self.file = os.path.realpath(os.path.join(os.path.dirname(__file__), 'tinker.ini'))
        self.config = configparser.ConfigParser()
        self.config.read(self.file)
        self.config.sections()
        print(self.config.sections())
        print(f"init - Word pred: {self.config['PREDICTION_TASK']['WORD_PRED']}")
        print(f"init - Sentence pred: {self.config['PREDICTION_TASK']['SENTENCE_PRED']}")

        
    def _close(self):
        self.root.destroy()

    def _save(self):
        self.config.set('PREDICTION_TASK', 'WORD_PRED', self.WORD_PRED_TASK)
        self.config.set('PREDICTION_TASK', 'SENTENCE_PRED', self.SENTENCE_PRED_TASK)
        self.config.write(open(self.file,'w'))
        # self.root.destroy()
        print(f"Word pred: {self.WORD_PRED_TASK}")
        print(f"Sentence pred: {self.SENTENCE_PRED_TASK}")
        

    def run(self):
        
        self.root = tk.Tk()
        self.root.title("Tinker Panel")

        baseFrame = ttk.Frame(self.root)
        baseFrame.pack(padx=5, pady=5)

        tabControl = ttk.Notebook(baseFrame)
        
        tabWordPredFrame = ttk.Frame(tabControl)
        tabSenPredFrame = ttk.Frame(tabControl)
        
        tabControl.add(tabWordPredFrame, text ='Word Prediction')
        tabControl.add(tabSenPredFrame, text ='Sentence Prediction')
        tabControl.pack(expand = 1, fill ="both")


        cancelBtn = ttk.Button(baseFrame, text="Cancel", command=self._close)
        cancelBtn.pack(padx=5, pady=5, side=tk.RIGHT)

        confirmBtn = ttk.Button(baseFrame, text="Confirm", command=self._save)
        confirmBtn.pack(padx=5, pady=5, side=tk.RIGHT)

        

        self._word_pred_panel(tabWordPredFrame)
        self._sentence_prediction_panel(tabSenPredFrame)
         
        
                    
        # ttk.Button(buttonFrame, text="Confirm").

        self.root.mainloop() 

    def _word_pred_method_combobox(self, event, frame):
        # TODO when "Confirm" button is clicked -> record data via .get()


        # row 4 - 6
        if self.wordPredMethod.get() == "BM25Okpi":
            # row 4
            ttk.Label(frame, text="      k1").grid(sticky="E", column=0, row=4)
            k1Bm25OkpiString = tk.StringVar(frame, self.K1_BM25OKPI) 
            k1BM25Okpi = tk.Entry(frame, width=21, textvariable = k1Bm25OkpiString)
            k1BM25Okpi.grid(sticky="W", column=1, row=4)
            # row 5
            ttk.Label(frame, text="      b").grid(sticky="E", column=0, row=5)
            bBm25OkpiString = tk.StringVar(frame, self.B_BM25OKPI)
            bBm25Okpi = tk.Entry(frame, width=21, textvariable=bBm25OkpiString)
            bBm25Okpi.grid(sticky="W", column=1, row=5)
            # row 6
            ttk.Label(frame, text='      \u03B5').grid(sticky="E", column=0, row=6) # epsilon
            epsilonBm25OkpiString = tk.StringVar(frame, self.EPSILON_BM25OKPI)
            epsilonBm25Okpi = tk.Entry(frame, width=21, textvariable=epsilonBm25OkpiString)
            epsilonBm25Okpi.grid(sticky="W", column=1, row=6)
            # Assign task
            self.WORD_PRED_TASK = "WORD_BM25OKPI"
        elif self.wordPredMethod.get() == "BM25L":
            # row 4
            ttk.Label(frame, text="      k1").grid(sticky="E", column=0, row=4)
            k1Bm25LString = tk.StringVar(frame, self.K1_BM25L)
            k1Bm25L = tk.Entry(frame, width=21, textvariable=k1Bm25LString)
            k1Bm25L.grid(sticky="W", column=1, row=4)
            # row 5
            ttk.Label(frame, text="      b").grid(sticky="E", column=0, row=5)
            bBm25LString = tk.StringVar(frame, self.B_BM25L)
            bBm25L = tk.Entry(frame, width=21, textvariable=bBm25LString)
            bBm25L.grid(sticky="W", column=1, row=5)
            # row 6
            ttk.Label(frame, text='      \u03B4').grid(sticky="E", column=0, row=6) # delta
            deltaBm25LString = tk.StringVar(frame, self.DELTA_BM25L)
            deltaBm25L = tk.Entry(frame, width=21, textvariable=deltaBm25LString)
            deltaBm25L.grid(sticky="W", column=1, row=6)
            # Assign task
            self.WORD_PRED_TASK = "WORD_BM25OL"
        elif self.wordPredMethod.get() == "BM25Plus":
            # row 4
            ttk.Label(frame, text="      k1").grid(sticky="E", column=0, row=4)
            k1Bm25PlusString = tk.StringVar(frame, self.K1_BM25PLUS)
            k1Bm25Plus = tk.Entry(frame, width=21, textvariable=k1Bm25PlusString)
            k1Bm25Plus.grid(sticky="W", column=1, row=4)
            # row 5
            ttk.Label(frame, text="      b").grid(sticky="E", column=0, row=5)
            bBm25PlusString = tk.StringVar(frame, self.B_BM25PLUS)
            bBm25Plus = tk.Entry(frame, width=21, textvariable=bBm25PlusString)
            bBm25Plus.grid(sticky="W", column=1, row=5)
            # row 6
            ttk.Label(frame, text='      \u03B4').grid(sticky="E", column=0, row=6) # delta
            deltaBm25PlusString = tk.StringVar(frame, self.DELTA_BM25PLUS)
            deltaBm25Plus = tk.Entry(frame, width=21, textvariable=deltaBm25PlusString)
            deltaBm25Plus.grid(sticky="W", column=1, row=6)
            # Assign task
            self.WORD_PRED_TASK = "WORD_BM25PLUS"
        elif self.wordPredMethod.get() == "GPT-2":
            # row 4
            ttk.Label(frame, text="Model").grid(sticky="E", column=0, row=4)
            modelGpt2 = ttk.Combobox(frame, values=self.MODEL_GPT2)
            modelGpt2.current(1)
            modelGpt2.grid(sticky="W", column=1, row=4)
            # row 5
            ttk.Label(frame, text="Seed").grid(sticky="E", column=0, row=5)
            seedGpt2String = tk.StringVar(frame, self.GPT2_SEED)
            seedGpt2 = tk.Entry(frame, width=21, textvariable=seedGpt2String)
            seedGpt2.grid(sticky="W", column=1, row=5)
            #  row 6
            ttk.Label(frame, text="", width=8, padding=5).grid(sticky="E", column=0, row=6)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1,row=6)
            # Assign task
            self.WORD_PRED_TASK = "WORD_GPT2"
        elif self.wordPredMethod.get() == "RoBERTa":
            # row 4
            ttk.Label(frame, text="Model").grid(sticky="E", column=0, row=4)
            modelRoberta = ttk.Combobox(frame, values=self.MODEL_ROBERTA)
            modelRoberta.current(1)
            modelRoberta.grid(sticky="W", column=1, row=4)
            # row 5
            ttk.Label(frame, text="", width=8, padding=5).grid(sticky="E", column=0, row=5)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1,row=5)
            #  row 6
            ttk.Label(frame, text="", width=8, padding=5).grid(sticky="E", column=0, row=6)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1,row=6)
            # Assign task
            self.WORD_PRED_TASK = "WORD_ROBERTA"

    def _word_pred_panel(self, frame):
        # row 0
        ttk.Label(frame, text ="Word Prediction", font=('Helvetica',13,'bold')).grid(sticky="E", column=0, row=0)

        # row 1
        ttk.Label(frame, text ="Max Prediction Number").grid(sticky="E", column=0, row=1)
        maxWordPredNum = ttk.Combobox(frame, values=self.WORD_PRED_NUM, state="readonly")
        # maxWordPredNumStringVar = tk.StringVar(frame, value=4)
        # maxWordPredNum = ttk.Spinbox(frame, from_=1, to=4, textvariable=maxWordPredNumStringVar, wrap=False)
        maxWordPredNum.grid(sticky="W", column=1, row=1)
        maxWordPredNum.current(3)

        # row 2
        ttk.Label(frame, text ="Display Location").grid(sticky="E", column=0, row=2)
        wordDisplayLocation = ttk.Combobox(frame, values=self.WORD_DISP_LOC, state="readonly")
        wordDisplayLocation.grid(sticky="W", column=1, row=2)
        wordDisplayLocation.current(1)

        # row 3
        ttk.Label(frame, text ="Method").grid(sticky="E", column=0, row=3)
        self.wordPredMethod = ttk.Combobox(frame, values=self.WORD_PRED_METHOD, state="readonly")
        self.wordPredMethod.grid(sticky="W", column=1, row=3)
        # self.wordPredMethod.current(0)
        self.wordPredMethod.bind("<<ComboboxSelected>>", lambda event: self._word_pred_method_combobox(event, frame))

        

    """ Sentence Prediction Below """
    def _sen_retrieval_text_method_combobox(self, event, frame):
        if self.senRetriTextMethod.get() == "BM25Okpi":
            # row 6
            ttk.Label(frame, text="      k1").grid(sticky="E", column=0, row=6)
            k1Bm25OkpiString_senRetri = tk.StringVar(frame, self.K1_BM25OKPI) 
            k1BM25Okpi_senRetri = tk.Entry(frame, width=21, textvariable = k1Bm25OkpiString_senRetri)
            k1BM25Okpi_senRetri.grid(sticky="W", column=1, row=6)
            ttk.Label(frame, text="", width=5, padding=5).grid(sticky="W", column=2,row=6)
            # row 7
            ttk.Label(frame, text="      b").grid(sticky="E", column=0, row=7)
            bBm25OkpiString_senRetri = tk.StringVar(frame, self.B_BM25OKPI)
            bBm25Okpi_senRetri = tk.Entry(frame, width=21, textvariable=bBm25OkpiString_senRetri)
            bBm25Okpi_senRetri.grid(sticky="W", column=1, row=7)
            # row 8
            ttk.Label(frame, text='      \u03B5').grid(sticky="E", column=0, row=8) # epsilon
            epsilonBm25OkpiString_senRetri = tk.StringVar(frame, self.EPSILON_BM25OKPI)
            epsilonBm25Okpi_senRetri = tk.Entry(frame, width=21, textvariable=epsilonBm25OkpiString_senRetri)
            epsilonBm25Okpi_senRetri.grid(sticky="W", column=1, row=8)
            # row 9
            ttk.Label(frame, text="", width=15, padding=5).grid(sticky="E", column=0, row=9)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1,row=9)
            # Assign task
            self.SENTENCE_PRED_TASK = "SENTENCE_BM25OKPI"
        elif self.senRetriTextMethod.get() == "BM25L":
            # row 6
            ttk.Label(frame, text="      k1").grid(sticky="E", column=0, row=6)
            k1Bm25LString_senRetri = tk.StringVar(frame, self.K1_BM25L)
            k1Bm25L_senRetri = tk.Entry(frame, width=21, textvariable=k1Bm25LString_senRetri)
            k1Bm25L_senRetri.grid(sticky="W", column=1, row=6)
            ttk.Label(frame, text="", width=5, padding=5).grid(sticky="W", column=2,row=6)
            # row 7
            ttk.Label(frame, text="      b").grid(sticky="E", column=0, row=7)
            bBm25LString_senRetri = tk.StringVar(frame, self.B_BM25L)
            bBm25L_senRetri = tk.Entry(frame, width=21, textvariable=bBm25LString_senRetri)
            bBm25L_senRetri.grid(sticky="W", column=1, row=7)
            # row 8
            ttk.Label(frame, text='      \u03B4').grid(sticky="E", column=0, row=8) # delta
            deltaBm25LString_senRetri = tk.StringVar(frame, self.DELTA_BM25L)
            deltaBm25L_senRetri = tk.Entry(frame, width=21, textvariable=deltaBm25LString_senRetri)
            deltaBm25L_senRetri.grid(sticky="W", column=1, row=8)
            # row 9
            ttk.Label(frame, text="", width=15, padding=5).grid(sticky="E", column=0, row=9)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1,row=9)
            # Assign task
            self.SENTENCE_PRED_TASK = "SENTENCE_BM25L"
        elif self.senRetriTextMethod.get() == "BM25Plus":
            # row 6
            ttk.Label(frame, text="      k1").grid(sticky="E", column=0, row=6)
            k1Bm25PlusString_senRetri = tk.StringVar(frame, self.K1_BM25PLUS)
            k1Bm25Plus_senRetri = tk.Entry(frame, width=21, textvariable=k1Bm25PlusString_senRetri)
            k1Bm25Plus_senRetri.grid(sticky="W", column=1, row=6)
            ttk.Label(frame, text="", width=5, padding=5).grid(sticky="W", column=2,row=6)
            # row 7
            ttk.Label(frame, text="      b").grid(sticky="E", column=0, row=7)
            bBm25PlusString_senRetri = tk.StringVar(frame, self.B_BM25PLUS)
            bBm25Plus_senRetri = tk.Entry(frame, width=21, textvariable=bBm25PlusString_senRetri)
            bBm25Plus_senRetri.grid(sticky="W", column=1, row=7)
            # row 8
            ttk.Label(frame, text='      \u03B4').grid(sticky="E", column=0, row=8) # delta
            deltaBm25PlusString_senRetri = tk.StringVar(frame, self.DELTA_BM25PLUS)
            deltaBm25Plus_senRetri = tk.Entry(frame, width=21, textvariable=deltaBm25PlusString_senRetri)
            deltaBm25Plus_senRetri.grid(sticky="W", column=1, row=8)
            # row 9
            ttk.Label(frame, text="", width=15, padding=5).grid(sticky="E", column=0, row=9)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1,row=9)
            # Assign task
            self.SENTENCE_PRED_TASK = "SENTENCE_BM25PLUS"

    def _sen_similarity_combobox(self, event, frame):
        
        if self.senSimilarity.get() == "Text":
            # row 5
            ttk.Label(frame, text="Select Retrieval Method").grid(sticky="E", column=0, row=5)
            self.senRetriTextMethod = ttk.Combobox(frame, values=self.SEN_RETRI_TEXT_METHOD, state="readonly")
            self.senRetriTextMethod.grid(sticky="W", column=1, row=5)
            # self.senRetriTextMethod.current(0)
            self.senRetriTextMethod.bind("<<ComboboxSelected>>", lambda event: self._sen_retrieval_text_method_combobox(event, frame))
            # row 6
            ttk.Label(frame, text="", width=15, padding=5).grid(sticky="E", column=0, row=6)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1,row=6)
            ttk.Label(frame, text="", width=5, padding=5).grid(sticky="W", column=2,row=6)
            # row 7
            ttk.Label(frame, text="", width=15, padding=5).grid(sticky="E", column=0, row=7)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1,row=7)
            # row 8
            ttk.Label(frame, text="", width=15, padding=5).grid(sticky="E", column=0, row=8)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1,row=8)
             # row 9
            ttk.Label(frame, text="", width=15, padding=5).grid(sticky="E", column=0, row=9)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1,row=9)
        elif self.senSimilarity.get() == "Semantics":
            # row 5
            ttk.Label(frame, text="Select Language Model").grid(sticky="E", column=0, row=5)
            self.senRetriSemanticsModel = ttk.Combobox(frame, values=self.SEN_RETRI_SEMAN_MODEL)
            self.senRetriSemanticsModel.grid(sticky="E", column=1, row=5)
            # self.senRetriSemanticsModel.current(0)
            # row 6
            ttk.Label(frame, text="", width=15, padding=5).grid(sticky="E", column=0, row=6)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1,row=6)
            ttk.Label(frame, text="", width=5, padding=5).grid(sticky="W", column=2,row=6)
            # row 7
            ttk.Label(frame, text="", width=15, padding=5).grid(sticky="E", column=0, row=7)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1,row=7)
            # row 8
            ttk.Label(frame, text="", width=15, padding=5).grid(sticky="E", column=0, row=8)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1,row=8)
            # row 9
            ttk.Label(frame, text="", width=15, padding=5).grid(sticky="E", column=0, row=9)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1,row=9)

    def _sen_gpt2_approach_combobox(self, event, frame):

        if self.senGpt2Approach.get() == "Greedy search":
            # row 6
            ttk.Label(frame, text="max length").grid(sticky="E", column=0, row=6)
            maxLengthString_senGpt2Greedy = tk.StringVar(frame, value=self.GPT2_MAX_LENGTH)
            maxLength_senGpt2Greedy = tk.Entry(frame, width=21, textvariable=maxLengthString_senGpt2Greedy)
            maxLength_senGpt2Greedy.grid(sticky="W", column=1, row=6)
            ttk.Label(frame, text="", width=5, padding=5).grid(sticky="W", column=2,row=6)
            # row 7
            ttk.Label(frame, text="no repeat n-gram size").grid(sticky="E", column=0, row=7)
            noRepeatNGramSizeString_senGpt2Greedy = tk.StringVar(frame, value=self.GPT2_NO_REPEAT_NGRAM_SIZE)
            noRepeatNGramSize_senGpt2Greedy = tk.Entry(frame, width=21, textvariable=noRepeatNGramSizeString_senGpt2Greedy)
            noRepeatNGramSize_senGpt2Greedy.grid(sticky="W", column=1, row=7)
            # row 8
            ttk.Label(frame, text="", width=15, padding=5).grid(sticky="E", column=0, row=8)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1,row=8)
            # row 9
            ttk.Label(frame, text="", width=15, padding=5).grid(sticky="E", column=0, row=9)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1,row=9)
            # Assign task
            self.SENTENCE_PRED_TASK = "SENTENCE_GPT2_GREEDY"

        elif self.senGpt2Approach.get() == "Beam search":
            # row 6
            ttk.Label(frame, text="max length").grid(sticky="E", column=0, row=6)
            maxLengthString_senGpt2Beam = tk.StringVar(frame, value=self.GPT2_MAX_LENGTH)
            maxLength_senGpt2Beam = tk.Entry(frame, width=21, textvariable=maxLengthString_senGpt2Beam)
            maxLength_senGpt2Beam.grid(sticky="W", column=1, row=6)
            ttk.Label(frame, text="", width=5, padding=5).grid(sticky="W", column=2,row=6)
            # row 7
            ttk.Label(frame, text="no repeat n-gram size").grid(sticky="E", column=0, row=7)
            noRepeatNGramSizeString_senGpt2Beam = tk.StringVar(frame, value=self.GPT2_NO_REPEAT_NGRAM_SIZE)
            noRepeatNGramSize_senGpt2Beam = tk.Entry(frame, width=21, textvariable=noRepeatNGramSizeString_senGpt2Beam)
            noRepeatNGramSize_senGpt2Beam.grid(sticky="W", column=1, row=7)
            # row 8
            ttk.Label(frame, text="number of beams").grid(sticky="E", column=0, row=8)
            numOfBeamsString_senGpt2Beam = tk.StringVar(frame, value=self.GPT2_NUM_BEAMS)
            numOfBeams_senGpt2Beam = tk.Entry(frame, width=21, textvariable=numOfBeamsString_senGpt2Beam)
            numOfBeams_senGpt2Beam.grid(sticky="W", column=1, row=8)
             # row 9
            ttk.Label(frame, text="", width=15, padding=5).grid(sticky="E", column=0, row=9)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1,row=9)
            # Assign task
            self.SENTENCE_PRED_TASK = "SENTENCE_GPT2_BEAM"

        elif self.senGpt2Approach.get() == "Top-k sampling":
            # row 6
            ttk.Label(frame, text="max length").grid(sticky="E", column=0, row=6)
            maxLengthString_senGpt2TopK = tk.StringVar(frame, value=self.GPT2_MAX_LENGTH)
            maxLength_senGpt2TopK = tk.Entry(frame, width=21, textvariable=maxLengthString_senGpt2TopK)
            maxLength_senGpt2TopK.grid(sticky="W", column=1, row=6)
            ttk.Label(frame, text="", width=5, padding=5).grid(sticky="W", column=2,row=6)
            # row 7
            ttk.Label(frame, text="                                seed").grid(sticky="E", column=0, row=7)
            seedString_senGpt2TopK = tk.StringVar(frame, value=self.GPT2_SEED)
            seed_senGpt2TopK = tk.Entry(frame, width=21, textvariable=seedString_senGpt2TopK)
            seed_senGpt2TopK.grid(sticky="W", column=1, row=7)
            # row 8
            ttk.Label(frame, text="                                top k").grid(sticky="E", column=0, row=8)
            topKString_senGpt2TopK = tk.StringVar(frame, value=self.GPT2_TOP_K)
            topK_senGpt2TopK = tk.Entry(frame, width=21, textvariable=topKString_senGpt2TopK)
            topK_senGpt2TopK.grid(sticky="W", column=1, row=8)
            # row 9
            ttk.Label(frame, text="", width=15, padding=5).grid(sticky="E", column=0, row=9)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1,row=9)
            # Assign task
            self.SENTENCE_PRED_TASK = "SENTENCE_GPT2_TOP_K"

        elif self.senGpt2Approach.get() == "Top-p sampling":
            # row 6
            ttk.Label(frame, text="max length").grid(sticky="E", column=0, row=6)
            maxLengthString_senGpt2TopP = tk.StringVar(frame, value=self.GPT2_MAX_LENGTH)
            maxLength_senGpt2TopP = tk.Entry(frame, width=21, textvariable=maxLengthString_senGpt2TopP)
            maxLength_senGpt2TopP.grid(sticky="W", column=1, row=6)
            ttk.Label(frame, text="", width=5, padding=5).grid(sticky="W", column=2,row=6)
            # row 7
            ttk.Label(frame, text="                                seed").grid(sticky="E", column=0, row=7)
            seedString_senGpt2TopP = tk.StringVar(frame, value=self.GPT2_SEED)
            seed_senGpt2TopP = tk.Entry(frame, width=21, textvariable=seedString_senGpt2TopP)
            seed_senGpt2TopP.grid(sticky="W", column=1, row=7)
            # row 8
            ttk.Label(frame, text="                                top k").grid(sticky="E", column=0, row=8)
            topKString_senGpt2TopP = tk.StringVar(frame, value=self.GPT2_TOP_K)
            topK_senGpt2TopP = tk.Entry(frame, width=21, textvariable=topKString_senGpt2TopP)
            topK_senGpt2TopP.grid(sticky="W", column=1, row=8)
            # row 9
            ttk.Label(frame, text="                                top p").grid(sticky="E", column=0, row=9)
            topPString_senGpt2TopP = tk.StringVar(frame, value=self.GPT2_TOP_P)
            topP_senGpt2TopP = tk.Entry(frame, width=21, textvariable=topPString_senGpt2TopP)
            topP_senGpt2TopP.grid(sticky="W", column=1, row=9)
            # Assign task
            self.SENTENCE_PRED_TASK = "SENTENCE_GPT2_TOP_P"

    def _sen_gen_method_combobox(self, event, frame):
        
        if self.senGenMethod.get() == "GPT-2":
            # row 5
            ttk.Label(frame, text="      Select Method").grid(sticky="E", column=0, row=5)
            self.senGpt2Approach = ttk.Combobox(frame, values=self.SEN_GPT2_APPROACH, state="readonly")
            self.senGpt2Approach.grid(sticky="W", column=1, row=5)
            # self.senGpt2Approach.current(0)
            self.senGpt2Approach.bind("<<ComboboxSelected>>", lambda event: self._sen_gpt2_approach_combobox(event, frame))
            # row 6
            ttk.Label(frame, text="", width=15, padding=5).grid(sticky="E", column=0, row=6)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1,row=6)
            ttk.Label(frame, text="", width=5, padding=5).grid(sticky="W", column=2,row=6)
            # row 7
            ttk.Label(frame, text="", width=15, padding=5).grid(sticky="E", column=0, row=7)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1,row=7)
            # row 8
            ttk.Label(frame, text="", width=15, padding=5).grid(sticky="E", column=0, row=8)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1,row=8)
             # row 9
            ttk.Label(frame, text="", width=15, padding=5).grid(sticky="E", column=0, row=9)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1,row=9)
        elif self.senGenMethod.get() == "KWickChat":
            # row 5
            ttk.Label(frame, text="Number of History").grid(sticky="E", column=0, row=5)
            senKWHistoryNumString = tk.StringVar(frame, value=self.SEN_KW_HISTORY_NUM)
            senKWHistoryNum = tk.Entry(frame, width=21, textvariable=senKWHistoryNumString)
            senKWHistoryNum.grid(sticky="W", column=1, row=5)
            # row 6
            ttk.Label(frame, text="      Persona").grid(sticky="E", column=0, row=6)
            senKWPersonaNumString = tk.StringVar(frame, value=self.SEN_KW_PERSONA_NUM)
            senKWPersonaNum = tk.Entry(frame, width=21, textvariable=senKWPersonaNumString)
            senKWPersonaNum.grid(sticky="W", column=1, row=6)
            senKWPersonaNumBtn = tk.Button(frame, text="ok", command=lambda: self._create_persona(frame, int(senKWPersonaNum.get())))
            senKWPersonaNumBtn.grid(sticky="W", column=2,row=6)
            # row 7
            ttk.Label(frame, text="", width=15, padding=5).grid(sticky="E", column=0, row=7)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1,row=7)
            # row 8
            ttk.Label(frame, text="", width=15, padding=5).grid(sticky="E", column=0, row=8)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1,row=8)
             # row 9
            ttk.Label(frame, text="", width=15, padding=5).grid(sticky="E", column=0, row=9)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1,row=9)
            
            

    def _create_persona(self, frame, personaNum):
        # row 7 - X
        rowNum = 7
        self.senKWPersonaList = []
        if personaNum >= self.lastPersonaNum:
            for i in range(personaNum):
                ttk.Label(frame, text="Input persona").grid(sticky="E", column=0, row=rowNum+i)
                senKWPersona = ttk.Entry(frame, width=21)
                senKWPersona.grid(sticky="W", column=1,row=rowNum+i)
                self.senKWPersonaList.append(senKWPersona.get())
        else:
            for i in range(personaNum):
                ttk.Label(frame, text="Input persona").grid(sticky="E", column=0, row=rowNum+i)
                senKWPersona = ttk.Entry(frame, width=21)
                senKWPersona.grid(sticky="W", column=1,row=rowNum+i)
                self.senKWPersonaList.append(senKWPersona.get())
            for i in range(self.lastPersonaNum - personaNum):
                ttk.Label(frame, text="", width=15, padding=5).grid(sticky="E", column=0, row=rowNum+personaNum+i)
                ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1,row=rowNum+personaNum+i)
        self.lastPersonaNum = personaNum
        # Assign task
        self.SENTENCE_PRED_TASK = "SENTENCE_KWICKCHAT"

    def _sen_pred_approach_combobox(self, event, frame):
        
        if self.senPredApproach.get() == "Retrieval":
            # row 4
            ttk.Label(frame, text="        Similarity").grid(sticky="E", column=0, row=4)
            self.senSimilarity = ttk.Combobox(frame, values=self.SEN_SIMILARITY, state="readonly")
            self.senSimilarity.grid(sticky="W", column=1, row=4)
            # self.senSimilarity.current(0)
            self.senSimilarity.bind("<<ComboboxSelected>>", lambda event: self._sen_similarity_combobox(event, frame))
            # row 5
            ttk.Label(frame, text="", width=15, padding=5).grid(sticky="E", column=0, row=5)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1,row=5)
            # row 6
            ttk.Label(frame, text="", width=15, padding=5).grid(sticky="E", column=0, row=6)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1,row=6)
            ttk.Label(frame, text="", width=5, padding=5).grid(sticky="W", column=2,row=6)
            # row 7
            ttk.Label(frame, text="", width=15, padding=5).grid(sticky="E", column=0, row=7)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1,row=7)
            # row 8
            ttk.Label(frame, text="", width=15, padding=5).grid(sticky="E", column=0, row=8)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1,row=8)
             # row 9
            ttk.Label(frame, text="", width=15, padding=5).grid(sticky="E", column=0, row=9)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1,row=9)
        elif self.senPredApproach.get() == "Generation":
            # row 4
            ttk.Label(frame, text="Select Method").grid(sticky="E", column=0, row=4)
            self.senGenMethod = ttk.Combobox(frame, values=self.SEN_GEN_METHOD, state="readonly")
            self.senGenMethod.grid(sticky="W", column=1, row=4)
            # self.senGenMethod.current(1)
            self.senGenMethod.bind("<<ComboboxSelected>>", lambda event: self._sen_gen_method_combobox(event, frame))
            # row 5
            ttk.Label(frame, text="", width=15, padding=5).grid(sticky="E", column=0, row=5)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1,row=5)
            # row 6
            ttk.Label(frame, text="", width=15, padding=5).grid(sticky="E", column=0, row=6)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1,row=6)
            ttk.Label(frame, text="", width=5, padding=5).grid(sticky="W", column=2,row=6)
            # row 7
            ttk.Label(frame, text="", width=15, padding=5).grid(sticky="E", column=0, row=7)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1,row=7)
            # row 8
            ttk.Label(frame, text="", width=15, padding=5).grid(sticky="E", column=0, row=8)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1,row=8)
             # row 9
            ttk.Label(frame, text="", width=15, padding=5).grid(sticky="E", column=0, row=9)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1,row=9)

    def _sentence_prediction_panel(self, frame):
        # row 0
        ttk.Label(frame, text ="Sentence Prediction", font=('Helvetica',13,'bold')).grid(sticky="E", column = 0, row = 0)

        # row 1
        ttk.Label(frame, text ="Max Prediction Number").grid(sticky="E", column=0, row=1)
        maxSenPredNum = ttk.Combobox(frame, values=self.SEN_PRED_NUM, state="readonly")
        maxSenPredNum.grid(sticky="W", column=1, row=1)
        maxSenPredNum.current(3)
        

        # row 2
        ttk.Label(frame, text ="Sentence Entry Approach").grid(sticky="E", column=0, row=2)
        senEntryApproach = ttk.Combobox(frame, values=self.SEN_ENTRY_APPROACH, state="readonly")
        senEntryApproach.grid(sticky="W", column=1, row=2)
        senEntryApproach.current(0)

        # row 3
        ttk.Label(frame, text="Prediction Approach").grid(sticky="E", column=0, row=3)
        self.senPredApproach = ttk.Combobox(frame, values=self.SEN_PRED_APPROACH, state="readonly")
        self.senPredApproach.grid(sticky="W", column=1, row=3)
        # self.senPredApproach.current(0)
        self.senPredApproach.bind("<<ComboboxSelected>>", lambda event: self._sen_pred_approach_combobox(event, frame))

        
if __name__ == '__main__':
    panel = View_tinker()
    panel.run()
