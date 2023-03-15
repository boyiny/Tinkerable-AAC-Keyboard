from cProfile import label
from os import stat
import tkinter as tk
from tkinter import BOTTOM, ttk
from tkinter import filedialog
import tkinter.font as tkFont

from click import command
from gevent import config
from sympy import per

import configparser 
import os
import time
import shutil
import ctypes
import glob




class View_tinker:
    WORD_PRED_NUM = [1,2,3,4]
    WORD_DISP_LOC = ["Fixed", "Above last pressed key"]
    WORD_PRED_METHOD = ["BM25Okapi", "BM25L", "BM25Plus", "GPT-2", "RoBERTa"]
    
    K1_BM25OKAPI = 1.5
    B_BM25OKAPI = 0.75
    EPSILON_BM25OKAPI = 0.25

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
    SEN_RETRI_TEXT_METHOD = ["BM25Okapi", "BM25L", "BM25Plus"]
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

    KW_MAX_LENGTH = 20
    KW_MIN_LENGTH = 1
    KW_SEED = 0
    KW_TEMPERATURE = 0.7
    KW_TOP_K = 0
    KW_TOP_P = 0.9

    lastPersonaNum = 1

    WORD_PRED_TASK = ""
    SENTENCE_PRED_TASK = ""

    BOOL_WORD_TINKERED = False
    BOOL_SENTENCE_TINKERED = False

    def __init__(self, controller):
        # self.comboboxStyle = ttk.Style()
        # self.comboboxStyle.configure('W.TCombobox', arrowsize = 20)


        self.controller = controller
        self.file = os.path.realpath(os.path.join(os.path.dirname(__file__), 'tinker.ini'))
        self.config = configparser.ConfigParser()
        self.config.read(self.file)
        self.config.sections()

        
        
    def _close(self):
        self.root.destroy()

    def _save_word_pred_settings(self):
        self.config.set('PREDICTION_TASK', 'word_pred', self.WORD_PRED_TASK)
        self.config.set('PREDICTION_TASK', 'sentence_pred', self.SENTENCE_PRED_TASK)
        self.config.set('WORD_PREDICTION', 'max_pred_num', self.maxWordPredNum.get())
        self.config.set('WORD_PREDICTION', 'display_location', self.wordDisplayLocation.get())
        self.config.set('WORD_PREDICTION', 'method', self.wordPredMethod.get())
        
        if self.WORD_PRED_TASK == "WORD_BM25OKAPI":
            self.config.set('WORD_BM25OKAPI', 'k1', self.k1BM25Okapi_wordPred.get())
            self.config.set('WORD_BM25OKAPI', 'b', self.bBM25Okapi_wordPred.get())
            self.config.set('WORD_BM25OKAPI', 'epsilon', self.epsilonBM25Okapi_wordPred.get())
        elif self.WORD_PRED_TASK == "WORD_BM25L":
            self.config.set('WORD_BM25L', 'k1', self.k1Bm25L_wordPred.get())
            self.config.set('WORD_BM25L', 'b', self.bBm25L_wordPred.get())
            self.config.set('WORD_BM25L', 'delta', self.deltaBm25L_wordPred.get())
        elif self.WORD_PRED_TASK == "BM25Plus":
            self.config.set('WORD_BM25PLUS', 'k1', self.k1Bm25Plus_wordPred.get())
            self.config.set('WORD_BM25PLUS', 'b', self.bBm25Plus_wordPred.get())
            self.config.set('WORD_BM25PLUS', 'delta', self.deltaBm25Plus_wordPred.get())
        elif self.WORD_PRED_TASK == "WORD_GPT2":
            self.config.set('WORD_GPT2', 'model', self.modelGpt2_wordPred.get())
            self.config.set('WORD_GPT2', 'seed', self.seedGpt2_wordPred.get())
        elif self.WORD_PRED_TASK == "WORD_ROBERTA":
            self.config.set('WORD_ROBERTA', 'model', self.modelRoberta_wordPred.get())

    def _save_sentence_pred_settings(self):
        self.config.set('SENTENCE_PREDICTION', 'max_pred_num', self.maxSenPredNum.get())
        self.config.set('SENTENCE_PREDICTION', 'sentence_entry_approach', self.senEntryApproach.get())
        self.config.set('SENTENCE_PREDICTION', 'prediction_approach', self.senPredApproach.get())

        if self.senPredApproach.get() == "Retrieval":
            self.config.set('SENTENCE_RETRIEVAL', 'similarity', self.senSimilarity.get())
            if self.senSimilarity.get() == "Text":
                self.config.set('SENTENCE_TEXT_SIMILARITY', 'retri_method', self.senRetriTextMethod.get())
                if self.SENTENCE_PRED_TASK == "SENTENCE_BM25OKAPI":
                    self.config.set('SENTENCE_BM25OKAPI', 'k1', self.k1BM25Okapi_senRetri.get())
                    self.config.set('SENTENCE_BM25OKAPI', 'b', self.bBM25Okapi_senRetri.get())
                    self.config.set('SENTENCE_BM25OKAPI', 'epsilon', self.epsilonBM25Okapi_senRetri.get())
                elif self.SENTENCE_PRED_TASK == "SENTENCE_BM25L":
                    self.config.set('SENTENCE_BM25L', 'k1', self.k1Bm25L_senRetri.get())
                    self.config.set('SENTENCE_BM25L', 'b', self.bBm25L_senRetri.get())
                    self.config.set('SENTENCE_BM25L', 'delta', self.deltaBm25L_senRetri.get())
                elif self.SENTENCE_PRED_TASK == "SENTENCE_BM25PLUS":
                    self.config.set('SENTENCE_BM25PLUS', 'k1', self.k1Bm25Plus_senRetri.get())
                    self.config.set('SENTENCE_BM25PLUS', 'b', self.bBm25Plus_senRetri.get())
                    self.config.set('SENTENCE_BM25PLUS', 'delta', self.deltaBm25Plus_senRetri.get())
            elif self.senSimilarity.get() == "Semantics":
                self.config.set('SENTENCE_SEMANTIC_SIMILARITY', 'sen_retri_seman_model', self.senRetriSemanticsModel.get())
        elif self.senPredApproach.get() == "Generation":
            self.config.set('SENTENCE_GENERATION', 'method', self.senGenMethod.get())
            if self.senGenMethod.get() == "GPT-2":
                self.config.set('SENTENCE_GPT2', 'model', self.senGpt2Model.get())
                self.config.set('SENTENCE_GPT2', 'method', self.senGpt2Approach.get())
                if self.SENTENCE_PRED_TASK == "SENTENCE_GPT2_GREEDY":
                    self.config.set('SENTENCE_GPT2_GREEDY', 'max_length', self.maxLength_senGpt2Greedy.get())
                    self.config.set('SENTENCE_GPT2_GREEDY', 'no_repeat_n_gram_size', self.noRepeatNGramSize_senGpt2Greedy.get())
                elif self.SENTENCE_PRED_TASK == "SENTENCE_GPT2_BEAM":
                    self.config.set('SENTENCE_GPT2_BEAM', 'max_length', self.maxLength_senGpt2Beam.get())
                    self.config.set('SENTENCE_GPT2_BEAM', 'no_repeat_n_gram_size', self.noRepeatNGramSize_senGpt2Beam.get())
                    self.config.set('SENTENCE_GPT2_BEAM', 'num_of_beams', self.numOfBeams_senGpt2Beam.get())
                elif self.SENTENCE_PRED_TASK == "SENTENCE_GPT2_TOP_K":
                    self.config.set('SENTENCE_GPT2_TOP_K', 'max_length', self.maxLength_senGpt2TopK.get())
                    self.config.set('SENTENCE_GPT2_TOP_K', 'seed', self.seed_senGpt2TopK.get())
                    self.config.set('SENTENCE_GPT2_TOP_K', 'top_k', self.seed_senGpt2TopK.get())
                elif self.SENTENCE_PRED_TASK == "SENTENCE_GPT2_TOP_P":
                    self.config.set('SENTENCE_GPT2_TOP_P', 'max_length', self.maxLength_senGpt2TopP.get())
                    self.config.set('SENTENCE_GPT2_TOP_P', 'seed', self.seed_senGpt2TopP.get())
                    self.config.set('SENTENCE_GPT2_TOP_P', 'top_k', self.topK_senGpt2TopP.get())
                    self.config.set('SENTENCE_GPT2_TOP_P', 'top_p', self.topP_senGpt2TopP.get())
            elif self.senGenMethod.get() == "KWickChat":
                self.config.set('SENTENCE_KWICKCHAT', 'max_length', self.senKWMaxLength.get())
                self.config.set('SENTENCE_KWICKCHAT', 'min_length', self.senKWMinLength.get())
                self.config.set('SENTENCE_KWICKCHAT', 'seed', self.senKWSeed.get())
                self.config.set('SENTENCE_KWICKCHAT', 'temperature', self.senKWTemperature.get())
                self.config.set('SENTENCE_KWICKCHAT', 'top_k', self.senKWTopK.get())
                self.config.set('SENTENCE_KWICKCHAT', 'top_p', self.senKWTopP.get())
                self.config.set('SENTENCE_KWICKCHAT', 'num_of_history', self.senKWHistoryNum.get())
                self.config.set('SENTENCE_KWICKCHAT', 'num_of_persona', self.senKWPersonaNum.get())
                personaList = []
                for p in self.senKWPersonaList:
                    personaList.append(p.get())
                personas = "|".join(personaList)
                self.config.set('SENTENCE_KWICKCHAT', 'persona', personas) # it is a list


    def _save(self):
        if self.BOOL_WORD_TINKERED:
            self._save_word_pred_settings()
        if self.BOOL_SENTENCE_TINKERED:
            self._save_sentence_pred_settings()
        
        if self.BOOL_WORD_TINKERED or self.BOOL_SENTENCE_TINKERED:
            self.config.write(open(self.file,'w'))
            self.controller.get_tinker_data()

        self.root.destroy()
        self.BOOL_WORD_TINKERED = False
        self.BOOL_SENTENCE_TINKERED = False

        if self.SENTENCE_PRED_TASK == 'SENTENCE_KWICKCHAT':
            self.controller.pop_up_conv_partner_window_kwickchat()

    def save_setting(self):
        timestr = time.strftime("%Y%m%d_%H%M%S")
        tinkerFileName = "./analysis/prediction_setting/tinker_"+str(timestr)+".ini"
        # copy current .ini file
        shutil.copyfile('tinker.ini', tinkerFileName)

    def load_setting(self):
        saved_file = filedialog.askopenfilename(initialdir="/",title="Select a File", filetypes=(("Configuration files", "*.ini"),))
        shutil.copyfile(saved_file, 'tinker.ini')
        self.file = os.path.realpath(os.path.join(os.path.dirname(__file__), 'tinker.ini'))
        self.config = configparser.ConfigParser()
        self.config.read(self.file)
        self.config.sections()
        self.controller.get_tinker_data()

        if self.controller.sentence_pred_PREDICTION_TASK == 'SENTENCE_KWICKCHAT':
            self.controller.pop_up_conv_partner_window_kwickchat()
            # self.controller.modelLogData.record_conversation_partner_input()

    def auto_load_the_latest_setting(self):   
        # If no previous setting (i.e. folder is empty), load a basic one
        if not os.listdir('./analysis/prediction_setting/'):
            self.file = os.path.realpath(os.path.join(os.path.dirname(__file__), 'tinker.ini'))
            self.config = configparser.ConfigParser()
            self.config.read(self.file)
            self.config.sections()
            self.controller.get_tinker_data()
        # else, load the last one
        else:
            fileList = glob.glob('./analysis/prediction_setting/*.ini')
            latestFile = max(fileList, key=os.path.getctime)
            self.config = configparser.ConfigParser()
            self.config.read(latestFile)
            self.config.sections()
            self.controller.get_tinker_data()
            

    def pop_up_prediction_settings_saved_notification(self):
        ctypes.windll.user32.MessageBoxW(0, "Current prediction settings have been saved.", "Info", 0)

    def default_setting(self):
        self.config.set('PREDICTION_TASK', 'word_pred', "WORD_BM25OKAPI")
        self.config.set('WORD_PREDICTION', 'max_pred_num', "4")
        self.config.set('WORD_PREDICTION', 'display_location', "Fixed")
        self.config.set('WORD_PREDICTION', 'method', "BM25Okapi")
        self.config.set('WORD_BM25OKAPI', 'k1', str(self.K1_BM25OKAPI))
        self.config.set('WORD_BM25OKAPI', 'b', str(self.B_BM25OKAPI))
        self.config.set('WORD_BM25OKAPI', 'epsilon', str(self.EPSILON_BM25OKAPI))

        self.config.set('PREDICTION_TASK', 'sentence_pred', "SENTENCE_BM25OKAPI")
        self.config.set('SENTENCE_PREDICTION', 'max_pred_num', "4")
        self.config.set('SENTENCE_PREDICTION', 'sentence_entry_approach', "Left to right")
        self.config.set('SENTENCE_PREDICTION', 'prediction_approach', "Retrieval")
        self.config.set('SENTENCE_RETRIEVAL', 'similarity', "Text")
        self.config.set('SENTENCE_TEXT_SIMILARITY', 'retri_method', "SENTENCE_BM25OKAPI")
        self.config.set('SENTENCE_BM25OKAPI', 'k1', str(self.K1_BM25OKAPI))
        self.config.set('SENTENCE_BM25OKAPI', 'b', str(self.B_BM25OKAPI))
        self.config.set('SENTENCE_BM25OKAPI', 'epsilon', str(self.EPSILON_BM25OKAPI))

        self.config.write(open(self.file,'w'))
        self.controller.get_tinker_data()


        
        

    def run(self):
        
        self.root = tk.Tk()
        self.root.title("Tinker Panel")

        bigFont = tkFont.Font(family='Arial', size=20)
        self.root.option_add("*Font", bigFont)

        baseFrame = ttk.Frame(self.root)
        baseFrame.pack(padx=5, pady=5)
        
        # style = ttk.Style()
        # style.configure('TNotebook.Tab', font=("Arial", 50))

        tabControl = ttk.Notebook(baseFrame)
        
        
        tabWordPredFrame = ttk.Frame(tabControl)
        # tabWordPredFrame.option_add("*Font", bigFont)
        tabSenPredFrame = ttk.Frame(tabControl)
        # tabSenPredFrame.option_add("*Font", bigFont)
        
        
        tabControl.add(tabWordPredFrame)
        tabControl.add(tabSenPredFrame)

        tabControl.tab(0, text ='      Word Prediction      ')
        tabControl.tab(1, text ='      Sentence Prediction      ')

        tabControl.pack(expand = True, fill ="both")
        
        # self.tabWordPredFrame = tabWordPredFrame
        # self.tabSenPredFrame = tabSenPredFrame


        
        


        cancelBtn = ttk.Button(baseFrame, text="Cancel", command=self._close)
        cancelBtn.pack(ipadx=10, ipady=10, side=tk.RIGHT)

        confirmBtn = ttk.Button(baseFrame, text="Confirm", command=self._save) # style="Big.TButton",
        confirmBtn.pack(ipadx=10, ipady=10, side=tk.RIGHT)

        # print(style.theme_names())
        # print(style.layout('TButton'))
        # style.configure('big.TButton', font=('Arial', 25))
        

        self._word_pred_panel(self.root, tabWordPredFrame)
        self._sentence_prediction_panel(self.root, tabSenPredFrame)
         
        
                    
        # ttk.Button(buttonFrame, text="Confirm").

        self.root.mainloop() 

    def _word_pred_method_combobox(self, event, frame):
        # bigFont = tkFont.Font(family='Arial', size=20)
        # frame.option_add("*TCombobox*Listbox*Font", bigFont)

        # row 4 - 6
        if self.wordPredMethod.get() == "BM25Okapi":
            # row 4
            ttk.Label(frame, text="      k1").grid(sticky="E", column=0, row=4)
            k1BM25OkapiString_wordPred = tk.StringVar(frame, self.K1_BM25OKAPI) 
            self.k1BM25Okapi_wordPred = tk.Entry(frame, width=21, textvariable = k1BM25OkapiString_wordPred)
            self.k1BM25Okapi_wordPred.grid(sticky="W", column=1, row=4)
            # row 5
            ttk.Label(frame, text="      b").grid(sticky="E", column=0, row=5)
            bBM25OkapiString_wordPred = tk.StringVar(frame, self.B_BM25OKAPI)
            self.bBM25Okapi_wordPred = tk.Entry(frame, width=21, textvariable=bBM25OkapiString_wordPred)
            self.bBM25Okapi_wordPred.grid(sticky="W", column=1, row=5)
            # row 6
            ttk.Label(frame, text='      \u03B5').grid(sticky="E", column=0, row=6) # epsilon
            epsilonBM25OkapiString_wordPred = tk.StringVar(frame, self.EPSILON_BM25OKAPI)
            self.epsilonBM25Okapi_wordPred = tk.Entry(frame, width=21, textvariable=epsilonBM25OkapiString_wordPred)
            self.epsilonBM25Okapi_wordPred.grid(sticky="W", column=1, row=6)
            # Assign task
            self.WORD_PRED_TASK = "WORD_BM25OKAPI"
            self.BOOL_WORD_TINKERED = True
        elif self.wordPredMethod.get() == "BM25L":
            # row 4
            ttk.Label(frame, text="      k1").grid(sticky="E", column=0, row=4)
            k1Bm25LString_wordPred = tk.StringVar(frame, self.K1_BM25L)
            self.k1Bm25L_wordPred = tk.Entry(frame, width=21, textvariable=k1Bm25LString_wordPred)
            self.k1Bm25L_wordPred.grid(sticky="W", column=1, row=4)
            # row 5
            ttk.Label(frame, text="      b").grid(sticky="E", column=0, row=5)
            bBm25LString_wordPred = tk.StringVar(frame, self.B_BM25L)
            self.bBm25L_wordPred = tk.Entry(frame, width=21, textvariable=bBm25LString_wordPred)
            self.bBm25L_wordPred.grid(sticky="W", column=1, row=5)
            # row 6
            ttk.Label(frame, text='      \u03B4').grid(sticky="E", column=0, row=6) # delta
            deltaBm25LString_wordPred = tk.StringVar(frame, self.DELTA_BM25L)
            self.deltaBm25L_wordPred = tk.Entry(frame, width=21, textvariable=deltaBm25LString_wordPred)
            self.deltaBm25L_wordPred.grid(sticky="W", column=1, row=6)
            # Assign task
            self.WORD_PRED_TASK = "WORD_BM25L"
            self.BOOL_WORD_TINKERED = True
        elif self.wordPredMethod.get() == "BM25Plus":
            # row 4
            ttk.Label(frame, text="      k1").grid(sticky="E", column=0, row=4)
            k1Bm25PlusString_wordPred = tk.StringVar(frame, self.K1_BM25PLUS)
            self.k1Bm25Plus_wordPred = tk.Entry(frame, width=21, textvariable=k1Bm25PlusString_wordPred)
            self.k1Bm25Plus_wordPred.grid(sticky="W", column=1, row=4)
            # row 5
            ttk.Label(frame, text="      b").grid(sticky="E", column=0, row=5)
            bBm25PlusString_wordPred = tk.StringVar(frame, self.B_BM25PLUS)
            self.bBm25Plus_wordPred = tk.Entry(frame, width=21, textvariable=bBm25PlusString_wordPred)
            self.bBm25Plus_wordPred.grid(sticky="W", column=1, row=5)
            # row 6
            ttk.Label(frame, text='      \u03B4').grid(sticky="E", column=0, row=6) # delta
            deltaBm25PlusString_wordPred = tk.StringVar(frame, self.DELTA_BM25PLUS)
            self.deltaBm25Plus_wordPred = tk.Entry(frame, width=21, textvariable=deltaBm25PlusString_wordPred)
            self.deltaBm25Plus_wordPred.grid(sticky="W", column=1, row=6)
            # Assign task
            self.WORD_PRED_TASK = "WORD_BM25PLUS"
            self.BOOL_WORD_TINKERED = True
        elif self.wordPredMethod.get() == "GPT-2":
            # row 4
            ttk.Label(frame, text="Model").grid(sticky="E", column=0, row=4)
            self.modelGpt2_wordPred = ttk.Combobox(frame, values=self.MODEL_GPT2) 
            self.modelGpt2_wordPred.current(1)
            self.modelGpt2_wordPred.grid(sticky="W", column=1, row=4)
            # row 5
            ttk.Label(frame, text="Seed").grid(sticky="E", column=0, row=5)
            seedGpt2String_wordPred = tk.StringVar(frame, self.GPT2_SEED)
            self.seedGpt2_wordPred = tk.Entry(frame, width=21, textvariable=seedGpt2String_wordPred)
            self.seedGpt2_wordPred.grid(sticky="W", column=1, row=5)
            #  row 6
            ttk.Label(frame, text="", width=8, padding=5).grid(sticky="E", column=0, row=6)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=6)
            # Assign task
            self.WORD_PRED_TASK = "WORD_GPT2"
            self.BOOL_WORD_TINKERED = True
        elif self.wordPredMethod.get() == "RoBERTa":
            # row 4
            ttk.Label(frame, text="Model").grid(sticky="E", column=0, row=4)
            self.modelRoberta_wordPred = ttk.Combobox(frame, values=self.MODEL_ROBERTA)
            self.modelRoberta_wordPred.current(1)
            self.modelRoberta_wordPred.grid(sticky="W", column=1, row=4)
            # row 5
            ttk.Label(frame, text="", width=8, padding=5).grid(sticky="E", column=0, row=5)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=5)
            #  row 6
            ttk.Label(frame, text="", width=8, padding=5).grid(sticky="E", column=0, row=6)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=6)
            # Assign task
            self.WORD_PRED_TASK = "WORD_ROBERTA"
            self.BOOL_WORD_TINKERED = True

    def _word_pred_panel(self, root, frame):
        # row 0
        ttk.Label(frame, text ="Word Prediction", font=('bold')).grid(sticky="E", column=0, row=0)

        # row 1
        ttk.Label(frame, text ="Max Prediction Number").grid(sticky="E", column=0, row=1)
        self.maxWordPredNum = ttk.Combobox(frame, values=self.WORD_PRED_NUM, state="readonly")
        # maxWordPredNumStringVar = tk.StringVar(frame, value=4)
        # maxWordPredNum = ttk.Spinbox(frame, from_=1, to=4, textvariable=maxWordPredNumStringVar, wrap=False)
        self.maxWordPredNum.grid(sticky="W", column=1, row=1)
        self.maxWordPredNum.current(3)

        # row 2
        ttk.Label(frame, text ="Display Location").grid(sticky="E", column=0, row=2)
        self.wordDisplayLocation = ttk.Combobox(frame, values=self.WORD_DISP_LOC, state="readonly")
        self.wordDisplayLocation.grid(sticky="W", column=1, row=2)
        self.wordDisplayLocation.current(1)

        # row 3
        ttk.Label(frame, text ="Method").grid(sticky="E", column=0, row=3)
        self.wordPredMethod = ttk.Combobox(frame, values=self.WORD_PRED_METHOD, state="readonly")
        self.wordPredMethod.grid(sticky="W", column=1, row=3)
        # self.wordPredMethod.current(0)
        self.wordPredMethod.bind("<<ComboboxSelected>>", lambda event: self._word_pred_method_combobox(event, frame))

        

    """ Sentence Prediction Below """
    def _sen_retrieval_text_method_combobox(self, event, frame):
        if self.senRetriTextMethod.get() == "BM25Okapi":
            # row 6
            ttk.Label(frame, text="      k1").grid(sticky="E", column=0, row=6)
            k1BM25OkapiString_senRetri = tk.StringVar(frame, self.K1_BM25OKAPI) 
            self.k1BM25Okapi_senRetri = tk.Entry(frame, width=21, textvariable = k1BM25OkapiString_senRetri)
            self.k1BM25Okapi_senRetri.grid(sticky="W", column=1, row=6)
            # row 7
            ttk.Label(frame, text="      b").grid(sticky="E", column=0, row=7)
            bBM25OkapiString_senRetri = tk.StringVar(frame, self.B_BM25OKAPI)
            self.bBM25Okapi_senRetri = tk.Entry(frame, width=21, textvariable=bBM25OkapiString_senRetri)
            self.bBM25Okapi_senRetri.grid(sticky="W", column=1, row=7)
            # row 8
            ttk.Label(frame, text='      \u03B5').grid(sticky="E", column=0, row=8) # epsilon
            epsilonBM25OkapiString_senRetri = tk.StringVar(frame, self.EPSILON_BM25OKAPI)
            self.epsilonBM25Okapi_senRetri = tk.Entry(frame, width=21, textvariable=epsilonBM25OkapiString_senRetri)
            self.epsilonBM25Okapi_senRetri.grid(sticky="W", column=1, row=8)
            # row 9
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=9)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=9)
            # row 10
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=10)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=10)
            # row 11
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=11)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=11)
            # row 12
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=12)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=12)
            ttk.Label(frame, text="", width=5, padding=5).grid(sticky="W", column=2, row=12)
            # row 13
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=13)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=13)
            # row 14
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=14)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=14)
            # row 15
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=15)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=15)
            # row 16
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=16)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=16)
            # Assign task
            self.SENTENCE_PRED_TASK = "SENTENCE_BM25OKAPI"
            self.BOOL_SENTENCE_TINKERED = True


        elif self.senRetriTextMethod.get() == "BM25L":
            # row 6
            ttk.Label(frame, text="      k1").grid(sticky="E", column=0, row=6)
            k1Bm25LString_senRetri = tk.StringVar(frame, self.K1_BM25L)
            self.k1Bm25L_senRetri = tk.Entry(frame, width=21, textvariable=k1Bm25LString_senRetri)
            self.k1Bm25L_senRetri.grid(sticky="W", column=1, row=6)
            # row 7
            ttk.Label(frame, text="      b").grid(sticky="E", column=0, row=7)
            bBm25LString_senRetri = tk.StringVar(frame, self.B_BM25L)
            self.bBm25L_senRetri = tk.Entry(frame, width=21, textvariable=bBm25LString_senRetri)
            self.bBm25L_senRetri.grid(sticky="W", column=1, row=7)
            # row 8
            ttk.Label(frame, text='      \u03B4').grid(sticky="E", column=0, row=8) # delta
            deltaBm25LString_senRetri = tk.StringVar(frame, self.DELTA_BM25L)
            self.deltaBm25L_senRetri = tk.Entry(frame, width=21, textvariable=deltaBm25LString_senRetri)
            self.deltaBm25L_senRetri.grid(sticky="W", column=1, row=8)
            # row 9
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=9)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=9)
            # row 10
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=10)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=10)
            # row 11
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=11)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=11)
            # row 12
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=12)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=12)
            ttk.Label(frame, text="", width=5, padding=5).grid(sticky="W", column=2, row=12)
            # row 13
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=13)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=13)
            # row 14
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=14)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=14)
            # row 15
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=15)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=15)
            # row 16
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=16)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=16)
            # Assign task
            self.SENTENCE_PRED_TASK = "SENTENCE_BM25L"
            self.BOOL_SENTENCE_TINKERED = True
        elif self.senRetriTextMethod.get() == "BM25Plus":
            # row 6
            ttk.Label(frame, text="      k1").grid(sticky="E", column=0, row=6)
            k1Bm25PlusString_senRetri = tk.StringVar(frame, self.K1_BM25PLUS)
            self.k1Bm25Plus_senRetri = tk.Entry(frame, width=21, textvariable=k1Bm25PlusString_senRetri)
            self.k1Bm25Plus_senRetri.grid(sticky="W", column=1, row=6)
            # row 7
            ttk.Label(frame, text="      b").grid(sticky="E", column=0, row=7)
            bBm25PlusString_senRetri = tk.StringVar(frame, self.B_BM25PLUS)
            self.bBm25Plus_senRetri = tk.Entry(frame, width=21, textvariable=bBm25PlusString_senRetri)
            self.bBm25Plus_senRetri.grid(sticky="W", column=1, row=7)
            # row 8
            ttk.Label(frame, text='      \u03B4').grid(sticky="E", column=0, row=8) # delta
            deltaBm25PlusString_senRetri = tk.StringVar(frame, self.DELTA_BM25PLUS)
            self.deltaBm25Plus_senRetri = tk.Entry(frame, width=21, textvariable=deltaBm25PlusString_senRetri)
            self.deltaBm25Plus_senRetri.grid(sticky="W", column=1, row=8)
            # row 9
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=9)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=9)
            # row 10
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=10)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=10)
            # row 11
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=11)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=11)
            # row 12
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=12)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=12)
            ttk.Label(frame, text="", width=5, padding=5).grid(sticky="W", column=2, row=12)
            # row 13
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=13)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=13)
            # row 14
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=14)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=14)
            # row 15
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=15)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=15)
            # row 16
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=16)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=16)
            # Assign task
            self.SENTENCE_PRED_TASK = "SENTENCE_BM25PLUS"
            self.BOOL_SENTENCE_TINKERED = True

    def _sen_similarity_combobox(self, event, frame):
        
        if self.senSimilarity.get() == "Text":
            # row 5
            ttk.Label(frame, text="Select Retrieval Method").grid(sticky="E", column=0, row=5)
            self.senRetriTextMethod = ttk.Combobox(frame, values=self.SEN_RETRI_TEXT_METHOD, state="readonly")
            self.senRetriTextMethod.grid(sticky="W", column=1, row=5)
            # self.senRetriTextMethod.current(0)
            self.senRetriTextMethod.bind("<<ComboboxSelected>>", lambda event: self._sen_retrieval_text_method_combobox(event, frame))
            # row 6
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=6)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=6)
            # row 7
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=7)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=7)
            # row 8
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=8)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=8)
             # row 9
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=9)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=9)
            # row 10
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=10)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=10)
            # row 11
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=11)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=11)
            # row 12
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=12)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=12)
            ttk.Label(frame, text="", width=5, padding=5).grid(sticky="W", column=2, row=12)
            # row 13
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=13)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=13)
            # row 14
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=14)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=14)
            # row 15
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=15)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=15)
            # row 16
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=16)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=16)
        elif self.senSimilarity.get() == "Semantics":
            # row 5
            ttk.Label(frame, text="Select Language Model").grid(sticky="E", column=0, row=5)
            self.senRetriSemanticsModel = ttk.Combobox(frame, values=self.SEN_RETRI_SEMAN_MODEL)
            self.senRetriSemanticsModel.grid(sticky="E", column=1, row=5)
            # self.senRetriSemanticsModel.current(0)
            # row 6
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=6)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=6)
            # row 7
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=7)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=7)
            # row 8
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=8)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=8)
            # row 9
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=9)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=9)
            # row 10
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=10)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=10)
            # row 11
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=11)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=11)
            # row 12
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=12)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=12)
            ttk.Label(frame, text="", width=5, padding=5).grid(sticky="W", column=2, row=12)
            # row 13
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=13)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=13)
            # row 14
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=14)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=14)
            # row 15
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=15)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=15)
            # row 16
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=16)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=16)
            # Assign task
            self.SENTENCE_PRED_TASK = "SENTENCE_SEMANTIC_SIMILARITY"
            self.BOOL_SENTENCE_TINKERED = True

    def _sen_gpt2_approach_combobox(self, event, frame):

        if self.senGpt2Approach.get() == "Greedy search":
            # row 7
            ttk.Label(frame, text="max length").grid(sticky="E", column=0, row=7)
            maxLengthString_senGpt2Greedy = tk.StringVar(frame, value=self.GPT2_MAX_LENGTH)
            self.maxLength_senGpt2Greedy = tk.Entry(frame, width=21, textvariable=maxLengthString_senGpt2Greedy)
            self.maxLength_senGpt2Greedy.grid(sticky="W", column=1, row=7)
            # row 8
            ttk.Label(frame, text="no repeat n-gram size").grid(sticky="E", column=0, row=8)
            noRepeatNGramSizeString_senGpt2Greedy = tk.StringVar(frame, value=self.GPT2_NO_REPEAT_NGRAM_SIZE)
            self.noRepeatNGramSize_senGpt2Greedy = tk.Entry(frame, width=21, textvariable=noRepeatNGramSizeString_senGpt2Greedy)
            self.noRepeatNGramSize_senGpt2Greedy.grid(sticky="W", column=1, row=8)
            # row 9
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=9)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=9)
            # row 10
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=10)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=10)
            # row 11
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=11)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=11)
            # row 12
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=12)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=12)
            ttk.Label(frame, text="", width=5, padding=5).grid(sticky="W", column=2, row=12)
            # row 13
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=13)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=13)
            # row 14
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=14)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=14)
            # row 15
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=15)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=15)
            # row 16
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=16)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=16)

            # Assign task
            self.SENTENCE_PRED_TASK = "SENTENCE_GPT2_GREEDY"
            self.BOOL_SENTENCE_TINKERED = True


        elif self.senGpt2Approach.get() == "Beam search":
            # row 7
            ttk.Label(frame, text="max length").grid(sticky="E", column=0, row=7)
            maxLengthString_senGpt2Beam = tk.StringVar(frame, value=self.GPT2_MAX_LENGTH)
            self.maxLength_senGpt2Beam = tk.Entry(frame, width=21, textvariable=maxLengthString_senGpt2Beam)
            self.maxLength_senGpt2Beam.grid(sticky="W", column=1, row=7)
            # row 8
            ttk.Label(frame, text="no repeat n-gram size").grid(sticky="E", column=0, row=8)
            noRepeatNGramSizeString_senGpt2Beam = tk.StringVar(frame, value=self.GPT2_NO_REPEAT_NGRAM_SIZE)
            self.noRepeatNGramSize_senGpt2Beam = tk.Entry(frame, width=21, textvariable=noRepeatNGramSizeString_senGpt2Beam)
            self.noRepeatNGramSize_senGpt2Beam.grid(sticky="W", column=1, row=8)
            # row 9
            ttk.Label(frame, text="number of beams").grid(sticky="E", column=0, row=9)
            numOfBeamsString_senGpt2Beam = tk.StringVar(frame, value=self.GPT2_NUM_BEAMS)
            self.numOfBeams_senGpt2Beam = tk.Entry(frame, width=21, textvariable=numOfBeamsString_senGpt2Beam)
            self.numOfBeams_senGpt2Beam.grid(sticky="W", column=1, row=9)
             # row 10
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=10)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=10)
            # row 11
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=11)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=11)
            # row 12
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=12)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=12)
            ttk.Label(frame, text="", width=5, padding=5).grid(sticky="W", column=2, row=12)
            # row 13
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=13)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=13)
            # row 14
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=14)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=14)
            # row 15
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=15)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=15)
            # row 16
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=16)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=16)
            
            # Assign task
            self.SENTENCE_PRED_TASK = "SENTENCE_GPT2_BEAM"
            self.BOOL_SENTENCE_TINKERED = True

        elif self.senGpt2Approach.get() == "Top-k sampling":
            # row 7
            ttk.Label(frame, text="max length").grid(sticky="E", column=0, row=7)
            maxLengthString_senGpt2TopK = tk.StringVar(frame, value=self.GPT2_MAX_LENGTH)
            self.maxLength_senGpt2TopK = tk.Entry(frame, width=21, textvariable=maxLengthString_senGpt2TopK)
            self.maxLength_senGpt2TopK.grid(sticky="W", column=1, row=7)
            # row 8
            ttk.Label(frame, text="                                seed").grid(sticky="E", column=0, row=8)
            seedString_senGpt2TopK = tk.StringVar(frame, value=self.GPT2_SEED)
            self.seed_senGpt2TopK = tk.Entry(frame, width=21, textvariable=seedString_senGpt2TopK)
            self.seed_senGpt2TopK.grid(sticky="W", column=1, row=8)
            # row 9
            ttk.Label(frame, text="                                top k").grid(sticky="E", column=0, row=9)
            topKString_senGpt2TopK = tk.StringVar(frame, value=self.GPT2_TOP_K)
            self.topK_senGpt2TopK = tk.Entry(frame, width=21, textvariable=topKString_senGpt2TopK)
            self.topK_senGpt2TopK.grid(sticky="W", column=1, row=9)
            # row 10
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=10)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=10)
            # row 11
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=11)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=11)
            # row 12
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=12)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=12)
            ttk.Label(frame, text="", width=5, padding=5).grid(sticky="W", column=2, row=12)
            # row 13
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=13)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=13)
            # row 14
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=14)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=14)
            # row 15
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=15)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=15)
            # row 16
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=16)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=16)

            # Assign task
            self.SENTENCE_PRED_TASK = "SENTENCE_GPT2_TOP_K"
            self.BOOL_SENTENCE_TINKERED = True

        elif self.senGpt2Approach.get() == "Top-p sampling":
            # row 7
            ttk.Label(frame, text="max length").grid(sticky="E", column=0, row=7)
            maxLengthString_senGpt2TopP = tk.StringVar(frame, value=self.GPT2_MAX_LENGTH)
            self.maxLength_senGpt2TopP = tk.Entry(frame, width=21, textvariable=maxLengthString_senGpt2TopP)
            self.maxLength_senGpt2TopP.grid(sticky="W", column=1, row=7)
            # row 8
            ttk.Label(frame, text="                                seed").grid(sticky="E", column=0, row=8)
            seedString_senGpt2TopP = tk.StringVar(frame, value=self.GPT2_SEED)
            self.seed_senGpt2TopP = tk.Entry(frame, width=21, textvariable=seedString_senGpt2TopP)
            self.seed_senGpt2TopP.grid(sticky="W", column=1, row=8)
            # row 9
            ttk.Label(frame, text="                                top k").grid(sticky="E", column=0, row=9)
            topKString_senGpt2TopP = tk.StringVar(frame, value=self.GPT2_TOP_K)
            self.topK_senGpt2TopP = tk.Entry(frame, width=21, textvariable=topKString_senGpt2TopP)
            self.topK_senGpt2TopP.grid(sticky="W", column=1, row=9)
            # row 10
            ttk.Label(frame, text="                                top p").grid(sticky="E", column=0, row=10)
            topPString_senGpt2TopP = tk.StringVar(frame, value=self.GPT2_TOP_P)
            self.topP_senGpt2TopP = tk.Entry(frame, width=21, textvariable=topPString_senGpt2TopP)
            self.topP_senGpt2TopP.grid(sticky="W", column=1, row=10)
            # row 11
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=11)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=11)
            # row 12
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=12)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=12)
            ttk.Label(frame, text="", width=5, padding=5).grid(sticky="W", column=2, row=12)
            # row 13
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=13)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=13)
            # row 14
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=14)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=14)
            # row 15
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=15)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=15)
            # row 16
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=16)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=16)
            
            # Assign task
            self.SENTENCE_PRED_TASK = "SENTENCE_GPT2_TOP_P"
            self.BOOL_SENTENCE_TINKERED = True

    def _sen_gen_method_combobox(self, event, frame):
        
        if self.senGenMethod.get() == "GPT-2":
            # row 2
            self.senEntryApproach.current(0)
            self.senEntryApproach.state(["disabled"])
            # row 5
            ttk.Label(frame, text="      Select Model").grid(sticky="E", column=0, row=5)
            self.senGpt2Model = ttk.Combobox(frame, values=self.MODEL_GPT2)
            self.senGpt2Model.current(1)
            self.senGpt2Model.grid(sticky="W", column=1, row=5)
            # self.senGpt2Approach.bind("<<ComboboxSelected>>", lambda event: self._sen_gpt2_approach_combobox(event, frame))

            # row 6
            ttk.Label(frame, text="      Select Method").grid(sticky="E", column=0, row=6)
            self.senGpt2Approach = ttk.Combobox(frame, values=self.SEN_GPT2_APPROACH, state="readonly")
            self.senGpt2Approach.grid(sticky="W", column=1, row=6)
            # self.senGpt2Approach.current(0)
            self.senGpt2Approach.bind("<<ComboboxSelected>>", lambda event: self._sen_gpt2_approach_combobox(event, frame))
            
            # ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=6)
            # ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=6)
            # row 7
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=7)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=7)
            # row 8
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=8)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=8)
             # row 9
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=9)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=9)
            # row 10
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=10)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=10)
            # row 11
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=11)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=11)
            # row 12
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=12)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=12)
            ttk.Label(frame, text="", width=5, padding=5).grid(sticky="W", column=2, row=12)
            # row 13
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=13)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=13)
            # row 14
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=14)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=14)
            # row 15
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=15)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=15)
            # row 16
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=16)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=16)
        elif self.senGenMethod.get() == "KWickChat":
            # row 2
            self.senEntryApproach.current(1)
            self.senEntryApproach.state(["disabled"])
            # row 5
            ttk.Label(frame, text="                   max length").grid(sticky="E", column=0, row=5)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=5)
            senKWMaxLenthString = tk.StringVar(frame, value=self.KW_MAX_LENGTH)
            self.senKWMaxLength = tk.Entry(frame, width=21, textvariable=senKWMaxLenthString)
            self.senKWMaxLength.grid(sticky="W", column=1, row=5)
            # row 6
            ttk.Label(frame, text="                   min length").grid(sticky="E", column=0, row=6)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=6)
            senKWMinLenthString = tk.StringVar(frame, value=self.KW_MIN_LENGTH)
            self.senKWMinLength = tk.Entry(frame, width=21, textvariable=senKWMinLenthString)
            self.senKWMinLength.grid(sticky="W", column=1, row=6)
            # row 7
            ttk.Label(frame, text="                   seed").grid(sticky="E", column=0, row=7)
            senKWSeedString = tk.StringVar(frame, value=self.KW_SEED)
            self.senKWSeed = tk.Entry(frame, width=21, textvariable=senKWSeedString)
            self.senKWSeed.grid(sticky="W", column=1, row=7)
            # row 8
            ttk.Label(frame, text="        temperature").grid(sticky="E", column=0, row=8)
            senKWTemperatureString = tk.StringVar(frame, value=self.KW_TEMPERATURE)
            self.senKWTemperature = tk.Entry(frame, width=21, textvariable=senKWTemperatureString)
            self.senKWTemperature.grid(sticky="W", column=1, row=8)
            # row 9
            ttk.Label(frame, text="        top k").grid(sticky="E", column=0, row=9)
            senKWTopKString = tk.StringVar(frame, value=self.KW_TOP_K)
            self.senKWTopK = tk.Entry(frame, width=21, textvariable=senKWTopKString)
            self.senKWTopK.grid(sticky="W", column=1, row=9)
            # row 10
            ttk.Label(frame, text="        top p").grid(sticky="E", column=0, row=10)
            senKWTopPString = tk.StringVar(frame, value=self.KW_TOP_P)
            self.senKWTopP = tk.Entry(frame, width=21, textvariable=senKWTopPString)
            self.senKWTopP.grid(sticky="W", column=1, row=10)
            # row 11
            ttk.Label(frame, text="        Number of History").grid(sticky="E", column=0, row=11)
            senKWHistoryNumString = tk.StringVar(frame, value=self.SEN_KW_HISTORY_NUM)
            self.senKWHistoryNum = tk.Entry(frame, width=21, textvariable=senKWHistoryNumString)
            self.senKWHistoryNum.grid(sticky="W", column=1, row=11)
            # row 12
            ttk.Label(frame, text="        Persona").grid(sticky="E", column=0, row=12)
            senKWPersonaNumString = tk.StringVar(frame, value=self.SEN_KW_PERSONA_NUM)
            self.senKWPersonaNum = tk.Entry(frame, width=21, textvariable=senKWPersonaNumString)
            self.senKWPersonaNum.grid(sticky="W", column=1, row=12)
            senKWPersonaNumBtn = tk.Button(frame, text="ok", command=lambda: self._create_persona(frame, int(self.senKWPersonaNum.get())))
            senKWPersonaNumBtn.grid(sticky="W", column=2, row=12)
            # row 13
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=13)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=13)
            # row 14
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=14)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=14)
            # row 15
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=15)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=15)
            # row 16
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=16)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=16)
            
            

    def _create_persona(self, frame, personaNum):
        # row 13 - X
        rowNum = 13
        self.senKWPersonaList = []
        if personaNum >= self.lastPersonaNum:
            for i in range(personaNum):
                ttk.Label(frame, text="Input persona").grid(sticky="E", column=0, row=rowNum+i)
                senKWPersona = tk.Entry(frame, width=21)
                senKWPersona.grid(sticky="W", column=1, row=rowNum+i)
                self.senKWPersonaList.append(senKWPersona)
        else:
            for i in range(personaNum):
                ttk.Label(frame, text="Input persona").grid(sticky="E", column=0, row=rowNum+i)
                senKWPersona = tk.Entry(frame, width=21)
                senKWPersona.grid(sticky="W", column=1, row=rowNum+i)
                self.senKWPersonaList.append(senKWPersona)
            for i in range(self.lastPersonaNum - personaNum):
                ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=rowNum+personaNum+i)
                ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=rowNum+personaNum+i)
        self.lastPersonaNum = personaNum

        # Assign task
        self.SENTENCE_PRED_TASK = "SENTENCE_KWICKCHAT"
        self.BOOL_SENTENCE_TINKERED = True


    def _sen_pred_approach_combobox(self, event, frame):
        
        if self.senPredApproach.get() == "Retrieval":
            # row 2
            self.senEntryApproach.state(["!disabled"])
            # row 4
            ttk.Label(frame, text="        Similarity").grid(sticky="E", column=0, row=4)
            self.senSimilarity = ttk.Combobox(frame, values=self.SEN_SIMILARITY, state="readonly")
            self.senSimilarity.grid(sticky="W", column=1, row=4)
            # self.senSimilarity.current(0)
            self.senSimilarity.bind("<<ComboboxSelected>>", lambda event: self._sen_similarity_combobox(event, frame))
            # row 5
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=5)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=5)
            # row 6
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=6)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=6)
            # row 7
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=7)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=7)
            # row 8
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=8)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=8)
            # row 9
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=9)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=9)
            # row 10
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=10)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=10)
            # row 11
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=11)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=11)
            # row 12
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=12)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=12)
            ttk.Label(frame, text="", width=5, padding=5).grid(sticky="W", column=2, row=12)
            # row 13
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=13)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=13)
            # row 14
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=14)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=14)
            # row 15
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=15)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=15)
            # row 16
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=16)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=16)
        elif self.senPredApproach.get() == "Generation":
            # row 2
            self.senEntryApproach.state(["!disabled"])
            # row 4
            ttk.Label(frame, text="Select Method").grid(sticky="E", column=0, row=4)
            self.senGenMethod = ttk.Combobox(frame, values=self.SEN_GEN_METHOD, state="readonly")
            self.senGenMethod.grid(sticky="W", column=1, row=4)
            # self.senGenMethod.current(1)
            self.senGenMethod.bind("<<ComboboxSelected>>", lambda event: self._sen_gen_method_combobox(event, frame))
            # row 5
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=5)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=5)
            # row 6
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=6)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=6)
            # row 7
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=7)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=7)
            # row 8
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=8)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=8)
             # row 9
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=9)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=9)
            # row 10
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=10)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=10)
            # row 11
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=11)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=11)
            # row 12
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=12)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=12)
            ttk.Label(frame, text="", width=5, padding=5).grid(sticky="W", column=2, row=12)
            # row 13
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=13)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=13)
            # row 14
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=14)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=14)
            # row 15
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=15)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=15)
            # row 16
            ttk.Label(frame, text="", width=19, padding=5).grid(sticky="E", column=0, row=16)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1, row=16)

    def _sentence_prediction_panel(self, root, frame):
        # row 0
        ttk.Label(frame, text ="Sentence Prediction", font=('bold')).grid(sticky="E", column = 0, row = 0)

        # row 1
        ttk.Label(frame, text ="Max Prediction Number").grid(sticky="E", column=0, row=1)
        self.maxSenPredNum = ttk.Combobox(frame, values=self.SEN_PRED_NUM, state="readonly")
        self.maxSenPredNum.grid(sticky="W", column=1, row=1)
        self.maxSenPredNum.current(3)
        

        # row 2
        ttk.Label(frame, text ="Sentence Entry Approach").grid(sticky="E", column=0, row=2)
        self.senEntryApproach = ttk.Combobox(frame, values=self.SEN_ENTRY_APPROACH, state="readonly")
        self.senEntryApproach.grid(sticky="W", column=1, row=2)
        self.senEntryApproach.current(0)

        # row 3
        ttk.Label(frame, text="Prediction Approach").grid(sticky="E", column=0, row=3)
        self.senPredApproach = ttk.Combobox(frame, values=self.SEN_PRED_APPROACH, state="readonly")
        self.senPredApproach.grid(sticky="W", column=1, row=3)
        # self.senPredApproach.current(0)
        self.senPredApproach.bind("<<ComboboxSelected>>", lambda event: self._sen_pred_approach_combobox(event, frame))

        
if __name__ == '__main__':
    panel = View_tinker()
    panel.run()
