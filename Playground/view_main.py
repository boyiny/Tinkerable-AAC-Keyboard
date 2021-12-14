import tkinter as tk
from tkinter import ttk

class View_main(tk.Tk):
    
    PAD = 10

    def __init__(self, controller):
        super().__init__()
        # self.application = tk.Tk()
        self.controller = controller
        self.title("Tinkerable Keyboard")
        self.resizable()
        self.geometry("1500x1000")
        self.textBox = tk.StringVar()
        self.mainView = self._make_main_view(self)
        
        

    def _make_main_view(self, frame):
        # self.rootFrame = tk.Frame(frame)
        # self.rootFrame.pack(padx=self.PAD, pady=self.PAD)

        self.viewMenu = View_menu(frame)
        self.viewEntry = View_entry(frame, self.textBox)
        self.viewKeypad = View_keypad(self.controller, frame, self.viewEntry, self.textBox)

        

class View_entry:

    def __init__(self, rootFrame, textBox):
        self.entry = tk.Entry(rootFrame, textvariable=textBox, font=('Calibri', 18))
        self.entry.place(height=50, width=1100, x=20, y=10)
        


    

class View_keypad:

    KEY_SIZE_X = 80
    KEY_SIZE_Y = 80
    KEY_SPEAK_SIZE_X = 120
    KEY_SPEAK_SIZE_Y = 80
    KEY_CLEAR_SIZE_X = 120
    KEY_CLEAR_SIZE_Y = 80
    KEY_SPACE_SIZE_X = 260
    KEY_SPACE_SIZE_Y = 80

    KEY_ROW_LOC_X = 20
    KEY_ROW_LOC_Y = 200

    KEY_COL_GAP = 5
    KEY_ROW_GAP = 120
    KEY_INDENT = 70

    KEY_DRAGABLE = False

    keyList = [['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '<-'], 
        ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'Speak'], 
        ['z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', 'Clear All'],
        ['Space']]

    def __init__(self, controller, rootFrame, entry, textBox):
        self.rootFrame = rootFrame
        self.entry = entry
        self.controller = controller
        self.textBox = textBox
        
        self._make_letterpad()

    def _make_letterpad(self):
        
        keyIndex = 0

        for i in range(len(self.keyList)):
            
            for keyChar in self.keyList[i]:
                column = self.keyList[i].index(keyChar)

                placeX = 0
                placeY = 0
                sizeX = 0
                sizeY = 0
                indent = 0

                if i>0:
                    indent = self.KEY_INDENT
                
                if keyChar == "Space":
                    placeX = column*self.KEY_ROW_LOC_X+(column+5)*(self.KEY_COL_GAP+self.KEY_SIZE_X)+indent
                    placeY = (i+1)*self.KEY_ROW_LOC_Y
                    sizeX = self.KEY_SPACE_SIZE_X
                    sizeY = self.KEY_SPACE_SIZE_Y

                elif keyChar == "Speak":
                    placeX = column*self.KEY_ROW_LOC_X+(column+1)*(self.KEY_COL_GAP+self.KEY_SIZE_X)+indent
                    placeY = (i+1)*self.KEY_ROW_LOC_Y
                    sizeX = self.KEY_SPEAK_SIZE_X
                    sizeY = self.KEY_SPEAK_SIZE_Y

                elif keyChar == "Clear All":
                    placeX = column*self.KEY_ROW_LOC_X+(column+1)*(self.KEY_COL_GAP+self.KEY_SIZE_X)+indent
                    placeY = (i+1)*self.KEY_ROW_LOC_Y 
                    sizeX = self.KEY_CLEAR_SIZE_X
                    sizeY = self.KEY_CLEAR_SIZE_Y

                else:
                    placeX = column*self.KEY_ROW_LOC_X+(column+1)*(self.KEY_COL_GAP+self.KEY_SIZE_X)+indent
                    placeY = (i+1)*self.KEY_ROW_LOC_Y
                    sizeX = self.KEY_SIZE_X
                    sizeY = self.KEY_SIZE_Y
                
                self._make_button(self.rootFrame, keyChar, placeX, placeY, sizeX, sizeY)
                keyIndex+=1


    def _make_dragable(self,widget):
        widget.bind("<Button-1>", self._on_drag_start)
        widget.bind("<B1-Motion>", self._on_drag_motion)

    def _on_drag_start(self, event):
        widget = event.widget
        widget._drag_start_x = event.x
        widget._drag_start_y = event.y

    def _on_drag_motion(self, event):
        widget = event.widget
        x = widget.winfo_x() - widget._drag_start_x + event.x
        y = widget.winfo_y() - widget._drag_start_y + event.y
        widget.place(x=x, y=y)

    def _make_button(self, frame, caption, placeX, placeY, sizeX, sizeY):
        command = (lambda button=caption: self.controller.on_button_click(button))

        keyBtn = tk.Button(frame, text=caption, command=command, bg='#C0C0C0', fg='black', font=('Calibri', 26))

        if self.KEY_DRAGABLE:
            self._make_dragable(keyBtn)
        
        keyBtn.place(x=placeX, y=placeY, width=sizeX, height=sizeY)


class View_menu:
    
    def __init__(self, rootFrame):
        self.rootFrame = rootFrame
        self._make_menu()

    def _make_menu(self):
        def donothing():
            pass

        menuBar = tk.Menu(self.rootFrame)
        self.rootFrame.config(menu=menuBar)

        fileMenu = tk.Menu(menuBar)
        menuBar.add_cascade(label="File", menu=fileMenu)
        fileMenu.add_command(label="Save Current Settings", command=donothing)
        fileMenu.add_command(label="Load Previous Settings...", command=donothing)

        predMethodMenu = tk.Menu(menuBar)
        menuBar.add_cascade(label="Prediction Methods", menu=predMethodMenu)
        predMethodMenu.add_command(label="RoBERTa", command=donothing)
        predMethodMenu.add_command(label="GPT-2", command=donothing)

        bm25Menu = tk.Menu(predMethodMenu)
        predMethodMenu.add_cascade(label="BM25", menu=bm25Menu)
        bm25Menu.add_command(label="Original", command=donothing)
        
        bm25StoryTellingMenu = tk.Menu(bm25Menu)
        bm25Menu.add_cascade(label="Story Telling", menu=bm25StoryTellingMenu)
        bm25StoryTellingMenu.add_command(label="Context Aware On", command=donothing)
        bm25StoryTellingMenu.add_command(label="Context Aware Off", command=donothing)

        bm25RoutineConvMenu = tk.Menu(bm25Menu)
        bm25Menu.add_cascade(label="Routine Conversation", menu=bm25RoutineConvMenu)
        bm25RoutineConvMenu.add_command(label="Context Aware On", command=donothing)
        bm25RoutineConvMenu.add_command(label="Context Aware Off", command=donothing)
        

        wordPredSettingMenu = tk.Menu(menuBar)
        menuBar.add_cascade(label="Word Prediction", menu=wordPredSettingMenu)

        maxWordPredNumMenu = tk.Menu(wordPredSettingMenu)
        wordPredSettingMenu.add_cascade(label="Max Word Prediction Number", menu=maxWordPredNumMenu)
        maxWordPredNumMenu.add_command(label="1", command=donothing)
        maxWordPredNumMenu.add_command(label="2", command=donothing)
        maxWordPredNumMenu.add_command(label="3", command=donothing)
        maxWordPredNumMenu.add_command(label="4", command=donothing)

        autoCapMenu = tk.Menu(wordPredSettingMenu)
        wordPredSettingMenu.add_cascade(label="Auto-capitalisation", menu=autoCapMenu)
        autoCapMenu.add_command(label="On", command=donothing)
        autoCapMenu.add_command(label="Off", command=donothing)

        wordPredPlaceMenu = tk.Menu(wordPredSettingMenu)
        wordPredSettingMenu.add_cascade(label="Word Predictions Place on Last-pressed Key", menu=wordPredPlaceMenu)
        wordPredPlaceMenu.add_command(label="On", command=donothing)
        wordPredPlaceMenu.add_command(label="Off", command=donothing)


        sentencePredSettingMenu = tk.Menu(menuBar)
        menuBar.add_cascade(label="Sentence Prediction", menu=sentencePredSettingMenu)
        
        displayMenu = tk.Menu(sentencePredSettingMenu)
        sentencePredSettingMenu.add_cascade(label="Display", menu=displayMenu)
        displayMenu.add_command(label="On", command=donothing)
        displayMenu.add_command(label="Off", command=donothing)

        startWithKeywordMenu = tk.Menu(sentencePredSettingMenu) # Bag of key words
        sentencePredSettingMenu.add_cascade(label="Start with Keyword", menu=startWithKeywordMenu)
        startWithKeywordMenu.add_command(label="On", command=donothing)
        startWithKeywordMenu.add_command(label="Off", command=donothing)

        chooseCorpusMenu = tk.Menu(sentencePredSettingMenu)
        sentencePredSettingMenu.add_cascade(label="Choose Corpus", menu=chooseCorpusMenu)
        chooseCorpusMenu.add_command(label="Mechanical Turk Dataset (Default)", command=donothing)
        chooseCorpusMenu.add_command(label="Collection from Previous CHI Paper", command=donothing)
        chooseCorpusMenu.add_command(label="Choose from File...", command=donothing)
        
        numOfSentenceMenu = tk.Menu(sentencePredSettingMenu)
        sentencePredSettingMenu.add_cascade(label="Number of Sentences", menu=numOfSentenceMenu)
        numOfSentenceMenu.add_command(label="1", command=donothing)
        numOfSentenceMenu.add_command(label="2", command=donothing)
        numOfSentenceMenu.add_command(label="3", command=donothing)
        numOfSentenceMenu.add_command(label="4", command=donothing)

        adaptiveLearnMenu = tk.Menu(sentencePredSettingMenu)
        sentencePredSettingMenu.add_cascade(label="Adaptive Learning", menu=adaptiveLearnMenu)

        adaptiveLearnOnMenu = tk.Menu(adaptiveLearnMenu)
        adaptiveLearnMenu.add_cascade(label="On", menu=adaptiveLearnOnMenu)
        adaptiveLearnOnMenu.add_command(label="Combine with Current Corpus", command=donothing)
        adaptiveLearnOnMenu.add_command(label="Use Text Entered in This Session Only", command=donothing)

        adaptiveLearnMenu.add_command(label="Off", command=donothing)



        uiControlMenu = tk.Menu(menuBar)
        menuBar.add_cascade(label="UI Control", menu=uiControlMenu)

        moveElementMenu = tk.Menu(uiControlMenu)
        uiControlMenu.add_cascade(label="Move Elements", menu=moveElementMenu)
        moveElementMenu.add_command(label="On", command=lambda:self.set_drag(True))
        moveElementMenu.add_command(label="Off", command=lambda:self.set_drag(False))
        moveElementMenu.add_command(label="Window Size", command=donothing)