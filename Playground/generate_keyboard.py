from tkinter import *
import tkinter as tk
from tkinter.dnd import Tester as DragWindow, Icon as Dragable

class Generate_key:
    def __init__(self): 
        self.keySizeX = 80
        self.keySizeY = 80
        self.keySpeakSizeX = 120
        self.keyClearSizeX = 120
        self.keySpaceSizeX = 260

        self.keyRowLocX = 20
        self.keyRowLocY = 200

        self.keyGap = 5
        self.keyRowGap = 120
        self.keyIndent = 70

        self.dragable = True

    def text_editing(self, value, entry):
        if value == "<-":
            entry2 = entry.get()
            # pos = entry2.find("")
            pos = entry2[:-1]
            entry.delete(0 ,tk.END)
            entry.insert(0, pos)
        elif value == "Space":
            entry.insert(tk.END, ' ')
        elif value == "Tab ":
            entry.insert(tk.END, '    ')
        elif value == "Speak":
            pass
        elif value == "Clear All":
            entry.delete(0,tk.END)
        else:
            entry.insert(tk.END,value)

    def make_btn(self, btnText, placeX, placeY, sizeX, sizeY, command):
        # The functional part of the main window is the canvas.
        # Dragable(btnText).attach(frame.canvas)

        keyBtn = tk.Button(text=btnText, command=command, bg='#C0C0C0', fg='black', font=('Calibri', 26))
        
        # TODO link to menu
        if self.dragable: 
            make_draggable(keyBtn)

        keyBtn.place(x=placeX, y=placeY, width=sizeX, height=sizeY)

    def create_letterpad(self, rootFrame, entry):

        keyList = [['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '<-'], 
        ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'Speak'], 
        ['z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', 'Clear All'],
        ['Space']]

        # row1, row2, row3, row4 = None, None, None, None
        # rowFrameList = [row1, row2, row3, row4]
        keyIndex = 0
        # keyFrameList = []

        

        # keyboardFrame = DragWindow(rootFrame)

        for i in range(len(keyList)):
            
            for keyChar in keyList[i]:
                column = keyList[i].index(keyChar)
                command = lambda value=keyChar: self.text_editing(value,entry)
                
                placeX = 0
                placeY = 0
                sizeX = 0
                indent = 0
                if i>0:
                    indent = self.keyIndent
                
                if keyChar == "Space":
                    placeX = column*self.keyRowLocX+(column+5)*(self.keyGap+self.keySizeX)+indent
                    placeY = (i+1)*self.keyRowLocY
                    sizeX = self.keySpaceSizeX

                elif keyChar == "Speak":
                    placeX = column*self.keyRowLocX+(column+1)*(self.keyGap+self.keySizeX)+indent
                    placeY = (i+1)*self.keyRowLocY
                    sizeX = self.keyClearSizeX

                elif keyChar == "Clear All":
                    placeX = column*self.keyRowLocX+(column+1)*(self.keyGap+self.keySizeX)+indent
                    placeY = (i+1)*self.keyRowLocY 
                    sizeX = self.keyClearSizeX

                else:
                    placeX = column*self.keyRowLocX+(column+1)*(self.keyGap+self.keySizeX)+indent
                    placeY = (i+1)*self.keyRowLocY
                    sizeX = self.keySizeX
                
                self.make_btn(keyChar, placeX, placeY, sizeX, self.keySizeY, command)
                keyIndex+=1
         

# Make the widget draggable
def make_draggable(widget):
    widget.bind("<Button-1>", on_drag_start)
    widget.bind("<B1-Motion>", on_drag_motion)

def on_drag_start(event):
    widget = event.widget
    widget._drag_start_x = event.x
    widget._drag_start_y = event.y

def on_drag_motion(event):
    widget = event.widget
    x = widget.winfo_x() - widget._drag_start_x + event.x
    y = widget.winfo_y() - widget._drag_start_y + event.y
    widget.place(x=x, y=y)

class DragDropMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        make_draggable(self)

class DnDFrame(DragDropMixin, tk.Frame):
    pass


class Generate_menu: 

    

    def create_menu(root_frame):
        def donothing():
            x = 0
        
        menuBar = Menu(root_frame)
        root_frame.config(menu=menuBar)

        fileMenu = Menu(menuBar)
        menuBar.add_cascade(label="File", menu=fileMenu)
        fileMenu.add_command(label="Save Current Settings", command=donothing)
        fileMenu.add_command(label="Load Previous Settings...", command=donothing)

        predMethodMenu = Menu(menuBar)
        menuBar.add_cascade(label="Prediction Methods", menu=predMethodMenu)
        predMethodMenu.add_command(label="RoBERTa", command=donothing)
        predMethodMenu.add_command(label="GPT-2", command=donothing)

        bm25Menu = Menu(predMethodMenu)
        predMethodMenu.add_cascade(label="BM25", menu=bm25Menu)
        bm25Menu.add_command(label="Original", command=donothing)
        
        bm25StoryTellingMenu = Menu(bm25Menu)
        bm25Menu.add_cascade(label="Story Telling", menu=bm25StoryTellingMenu)
        bm25StoryTellingMenu.add_command(label="Context Aware On", command=donothing)
        bm25StoryTellingMenu.add_command(label="Context Aware Off", command=donothing)

        bm25RoutineConvMenu = Menu(bm25Menu)
        bm25Menu.add_cascade(label="Routine Conversation", menu=bm25RoutineConvMenu)
        bm25RoutineConvMenu.add_command(label="Context Aware On", command=donothing)
        bm25RoutineConvMenu.add_command(label="Context Aware Off", command=donothing)
        

        wordPredSettingMenu = Menu(menuBar)
        menuBar.add_cascade(label="Word Prediction", menu=wordPredSettingMenu)

        maxWordPredNumMenu = Menu(wordPredSettingMenu)
        wordPredSettingMenu.add_cascade(label="Max Word Prediction Number", menu=maxWordPredNumMenu)
        maxWordPredNumMenu.add_command(label="1", command=donothing)
        maxWordPredNumMenu.add_command(label="2", command=donothing)
        maxWordPredNumMenu.add_command(label="3", command=donothing)
        maxWordPredNumMenu.add_command(label="4", command=donothing)

        autoCapMenu = Menu(wordPredSettingMenu)
        wordPredSettingMenu.add_cascade(label="Auto-capitalisation", menu=autoCapMenu)
        autoCapMenu.add_command(label="On", command=donothing)
        autoCapMenu.add_command(label="Off", command=donothing)

        wordPredPlaceMenu = Menu(wordPredSettingMenu)
        wordPredSettingMenu.add_cascade(label="Word Predictions Place on Last-pressed Key", menu=wordPredPlaceMenu)
        wordPredPlaceMenu.add_command(label="On", command=donothing)
        wordPredPlaceMenu.add_command(label="Off", command=donothing)


        sentencePredSettingMenu = Menu(menuBar)
        menuBar.add_cascade(label="Sentence Prediction", menu=sentencePredSettingMenu)
        
        displayMenu = Menu(sentencePredSettingMenu)
        sentencePredSettingMenu.add_cascade(label="Display", menu=displayMenu)
        displayMenu.add_command(label="On", command=donothing)
        displayMenu.add_command(label="Off", command=donothing)

        startWithKeywordMenu = Menu(sentencePredSettingMenu) # Bag of key words
        sentencePredSettingMenu.add_cascade(label="Start with Keyword", menu=startWithKeywordMenu)
        startWithKeywordMenu.add_command(label="On", command=donothing)
        startWithKeywordMenu.add_command(label="Off", command=donothing)

        chooseCorpusMenu = Menu(sentencePredSettingMenu)
        sentencePredSettingMenu.add_cascade(label="Choose Corpus", menu=chooseCorpusMenu)
        chooseCorpusMenu.add_command(label="Mechanical Turk Dataset (Default)", command=donothing)
        chooseCorpusMenu.add_command(label="Collection from Previous CHI Paper", command=donothing)
        chooseCorpusMenu.add_command(label="Choose from File...", command=donothing)
        
        numOfSentenceMenu = Menu(sentencePredSettingMenu)
        sentencePredSettingMenu.add_cascade(label="Number of Sentences", menu=numOfSentenceMenu)
        numOfSentenceMenu.add_command(label="1", command=donothing)
        numOfSentenceMenu.add_command(label="2", command=donothing)
        numOfSentenceMenu.add_command(label="3", command=donothing)
        numOfSentenceMenu.add_command(label="4", command=donothing)

        adaptiveLearnMenu = Menu(sentencePredSettingMenu)
        sentencePredSettingMenu.add_cascade(label="Adaptive Learning", menu=adaptiveLearnMenu)

        adaptiveLearnOnMenu = Menu(adaptiveLearnMenu)
        adaptiveLearnMenu.add_cascade(label="On", menu=adaptiveLearnOnMenu)
        adaptiveLearnOnMenu.add_command(label="Combine with Current Corpus", command=donothing)
        adaptiveLearnOnMenu.add_command(label="Use Text Entered in This Session Only", command=donothing)

        adaptiveLearnMenu.add_command(label="Off", command=donothing)



        uiControlMenu = Menu(menuBar)
        menuBar.add_cascade(label="UI Control", menu=uiControlMenu)

        moveElementMenu = Menu(uiControlMenu)
        uiControlMenu.add_cascade(label="Move Elements", menu=moveElementMenu)
        moveElementMenu.add_command(label="On", command=donothing)
        moveElementMenu.add_command(label="Off", command=donothing)
        moveElementMenu.add_command(label="Window Size", command=donothing)

