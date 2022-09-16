from cProfile import label
from fileinput import filename
import tkinter as tk 
from tkinter import BOTTOM, ttk
from tkinter import filedialog
from matplotlib.pyplot import text
from pathlib import Path

from soupsieve import select

class View_trace_analysis:

    def __init__(self):
        pass
    
    def _browse_files(self):
        filePath = filedialog.askopenfilename(initialdir="/",title="Select a File", filetypes=(("Text files", "*.txt"),))
        fileName = Path(filePath).stem
        print(fileName)
        self.filePathLabel = tk.Label(self.baseFrame, width=21, text=fileName).grid(sticky="E", column=0, row=0)

    def _close(self):
        self.root.destroy()

    def run(self):
        self.root = tk.Tk()
        self.root.title("Trace Analysis")

        self.baseFrame = ttk.Frame(self.root)
        self.baseFrame.pack(padx=5, pady=5)

        filePath = "File Path"
        # filePathString = tk.StringVar(baseFrame, self.filePath)
        self.filePathLabel = tk.Label(self.baseFrame, width=21, text=filePath).grid(sticky="E", column=0, row=0)
        selectFileBtn = ttk.Button(self.baseFrame, text="Open...", command=self._browse_files).grid(sticky="W",column=1, row=0)

        cancelBtn = ttk.Button(self.baseFrame, text="Analyse", command=self._close).grid(sticky="W", column=0, row=1)
        confirmBtn = ttk.Button(self.baseFrame, text="Cancel", command=self._close).grid(sticky="W", column=1, row=1)

        self.root.mainloop()


if __name__ == '__main__':
    panel = View_trace_analysis()
    panel.run()