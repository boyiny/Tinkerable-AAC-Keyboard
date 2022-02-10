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
            ttk.Label(frame, text="   k1").grid(sticky="E", column=0, row=4)
            k1Bm25Okpi = tk.StringVar(frame, self.K1_BM25OKPI) # 
            k1BM25OkpiEntry = tk.Entry(frame, width = 21, textvariable = k1Bm25Okpi)
            
            k1BM25OkpiEntry.grid(sticky="W", column=1, row=4)
            # print(f"k1BM25OkpiEntry = {k1BM25OkpiEntry.get()}")


            # row 5
            ttk.Label(frame, text="   b").grid(sticky="E", column=0, row=5)
            # row 6
            ttk.Label(frame, text='   \u03B5').grid(sticky="E", column=0, row=6) # epsilon
            print("Select BM25Okpi")
        elif self.wordPredMethod.get() == "BM25L" or self.wordPredMethod.get() == "BM25Plus":
            # row 4
            ttk.Label(frame, text="   k1").grid(sticky="E", column=0, row=4)
            # row 5
            ttk.Label(frame, text="   b").grid(sticky="E", column=0, row=5)
            # row 6
            ttk.Label(frame, text='   \u03B4').grid(sticky="E", column=0, row=6) # delta
        elif self.wordPredMethod.get() == "GPT-2":
            # row 4
            ttk.Label(frame, text="Model").grid(sticky="E", column=0, row=4)
            # row 5
            ttk.Label(frame, text="Seed").grid(sticky="E", column=0, row=5)
            #  row 6
            ttk.Label(frame, text= "   ").grid(sticky="E", column=0, row=6)
        elif self.wordPredMethod.get() == "RoBERTa":
            # row 4
            ttk.Label(frame, text="Model").grid(sticky="E", column=0, row=4)
            # row 5
            ttk.Label(frame, text="   ").grid(sticky="E", column=0, row=5)
            #  row 6
            ttk.Label(frame, text="   ").grid(sticky="E", column=0, row=6)

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
        

        


    def _sentence_prediction_panel(self, frame):
        ttk.Label(frame, text ="Sentence Prediction", font=('Helvetica',13,'bold')).grid(sticky="E", column = 0, row = 0, padx = 3, pady = 3)

if __name__ == '__main__':
    panel = View_tinker()
    panel.run()