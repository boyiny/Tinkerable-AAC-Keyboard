from cProfile import label
import tkinter as tk
from tkinter import BOTTOM, ttk

from click import command


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
    SEED_GPT2 = 0

    MODEL_ROBERTA = ["distilroberta-base","roberta-base", "roberta-large", "xlm-roberta-base", "xlm-roberta-large", "Please input..."]

    


    SENTENCE_PRED_NUM = [1,2,3,4]



    def __init__(self):
        pass
        
       

    def run(self):
        

        root = tk.Tk()
        root.title("Tinker Panel")

        baseFrame = ttk.Frame(root)
        baseFrame.pack(padx=5, pady=5)

        tabControl = ttk.Notebook(baseFrame)
        
        tabWordPredFrame = ttk.Frame(tabControl)
        tabSenPredFrame = ttk.Frame(tabControl)
        
        tabControl.add(tabWordPredFrame, text ='Word Prediction')
        tabControl.add(tabSenPredFrame, text ='Sentence Prediction')
        tabControl.pack(expand = 1, fill ="both")


        cancelBtn = ttk.Button(baseFrame, text="Cancel")
        cancelBtn.pack(padx=5, pady=5, side=tk.RIGHT)

        confirmBtn = ttk.Button(baseFrame, text="Confirm")
        confirmBtn.pack(padx=5, pady=5, side=tk.RIGHT)

        

        self._word_pred_panel(tabWordPredFrame)
        self._sentence_prediction_panel(tabSenPredFrame)
         
        
                    
        # ttk.Button(buttonFrame, text="Confirm").

        root.mainloop() 

    def _word_pred_method_combobox(self, event, frame):
        # TODO when "Confirm" button is clicked -> record data via .get()

        # frame = self.wordPredPanelFrame
        # row 4 - 
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

            # print("Select BM25Okpi")
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

        elif self.wordPredMethod.get() == "GPT-2":
            # row 4
            ttk.Label(frame, text="Model").grid(sticky="E", column=0, row=4)
            modelGpt2 = ttk.Combobox(frame, values=self.MODEL_GPT2)
            modelGpt2.current(1)
            modelGpt2.grid(sticky="W", column=1, row=4)
            # row 5
            ttk.Label(frame, text="Seed").grid(sticky="E", column=0, row=5)
            seedGpt2String = tk.StringVar(frame, self.SEED_GPT2)
            seedGpt2 = tk.Entry(frame, width=21, textvariable=seedGpt2String)
            seedGpt2.grid(sticky="W", column=1, row=5)
            #  row 6
            ttk.Label(frame, text="", width=8, padding=5).grid(sticky="E", column=0, row=6)
            ttk.Label(frame, text="", width=21, padding=5).grid(sticky="W", column=1,row=6)

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

    def _word_pred_panel(self, frame):
        self.wordPredPanelFrame = frame
        # row 0
        ttk.Label(frame, text ="Word Prediction", font=('Helvetica',13,'bold')).grid(sticky="E", column=0, row=0)

        # row 1
        ttk.Label(frame, text ="Max Prediction Number").grid(sticky="E", column=0, row=1)
        maxWordPredNum = ttk.Combobox(frame, values=self.WORD_PRED_NUM, state='readonly')
        maxWordPredNum.grid(sticky="W", column=1, row=1)
        maxWordPredNum.current(3)

        # row 2
        ttk.Label(frame, text ="Display Location").grid(sticky="E", column=0, row=2)
        wordDisplayLocation = ttk.Combobox(frame, values=self.WORD_DISP_LOC, state='readonly')
        wordDisplayLocation.grid(sticky="W", column=1, row=2)
        wordDisplayLocation.current(1)

        # row 3
        ttk.Label(frame, text ="Method").grid(sticky="E", column=0, row=3)
        self.wordPredMethod = ttk.Combobox(frame, values=self.WORD_PRED_METHOD, state="readonly")
        self.wordPredMethod.grid(sticky="W", column=1, row=3)
        self.wordPredMethod.current(0)
        self.wordPredMethod.bind("<<ComboboxSelected>>", lambda event: self._word_pred_method_combobox(event, frame))
        # print(f"wordPredMethod.current() = {wordPredMethod.current()}")
        # print(f"wordPredMethod.get() = {wordPredMethod.get()}")
        
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
        


    def _sentence_prediction_panel(self, frame):
        ttk.Label(frame, text ="Sentence Prediction", font=('Helvetica',13,'bold')).grid(sticky="E", column = 0, row = 0, padx = 3, pady = 3)

if __name__ == '__main__':
    panel = View_tinker()
    panel.run()