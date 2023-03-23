import tkinter as tk
from tkinter import ttk
from typing import Sized

import time
import ctypes
import glob
import os

from tkinter import filedialog
from pathlib import Path

from view_text_entry import View_text_edit
from view_tinker_panel import View_tinker
from view_trace_analysis import View_trace_analysis



class View_main(tk.Tk): 
    
    PAD = 10

    def __init__(self, controller):
        super().__init__() 
        self.controller = controller
        self.title("Tinkerable Keyboard")
        self.resizable()
        # self.geometry("1500x1000")
        self.state('zoomed')
        self.textBox = tk.StringVar()
        # self.option_add("*Font", ('Arial', 20))

class View_text_box:

    def __init__(self, controller, rootFrame): # textBox
        self.controller = controller
        self.entry = tk.Entry(rootFrame, textvariable=rootFrame.textBox, font=('Calibri', 18))
        self.entry.config(state="disabled")
        self.entry.config(disabledbackground="white")
        self.entry.config(disabledforeground="black")
        self.entry.place(height=50, width=1100, x=20, y=10)
        

class View_logging_indicator:
    def __init__(self, controller, rootFrame):
        self.loggingIndicatorFrame = tk.Frame(rootFrame, width=500, height=50)
        self.loggingIndicatorFrame.place(x=0, y=930)
        self.controller = controller
        # print("The width of the window: ", rootFrame.winfo_width())
        # print("The height of the window: ", rootFrame.winfo_height())
        self.loggingIndicatorBtn = tk.Label(self.loggingIndicatorFrame, text="Logging typing", font=('Calibri', 18))
        self.loggingIndicatorBtn.place(x=10, y=0)


   

class View_keypad:

    KEY_SIZE_X = 80
    KEY_SIZE_Y = 80
    KEY_SPEAK_SIZE_X = 120
    KEY_SPEAK_SIZE_Y = 80
    KEY_CLEAR_SIZE_X = 120
    KEY_CLEAR_SIZE_Y = 80
    KEY_SPACE_SIZE_X = 300
    KEY_SPACE_SIZE_Y = 80

    KEY_INIT_LOC_X = 15
    KEY_INIT_LOC_Y = 140

    KEY_COL_GAP = 15
    KEY_ROW_GAP = 120
    KEY_INDENT = 70

    KEY_DRAGABLE = False

    PRED_WORD_COL_GAP = 5
    PRED_WORD_ROW_GAP = 30

    PRED_WORD_INIT_LOC_X = 15
    PRED_WORD_INIT_LOC_Y = 110

    PRED_SENT_COL_GAP = 10
    PRED_SENT_INIT_LOC_X = 1100
    PRED_SENT_INIT_LOC_Y = 60

    buttons = []
    buttonsAttributes = []

    currentPressedKey = []
    
    predictedWordButtons = []
    predictedSentenceButtons = []

    newKeyPositionX = 0
    newKeyPositionY = 0

    lastPressedKeyIndex = 0

    BOOL_WORD_PRED_DISPLAY = True
    BOOL_WORD_PRED_PRESSED_KEY = False
    WORD_PRED_NUM = 4
    SENT_PRED_NUM = 4

    BOOL_SENT_PRED_DISPLAY = True

    BOOL_ENTRY_BY_KEYWORDS = False

    BOOL_TRACE = False


    keyList = [['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '<-'], 
        ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'Speak'], 
        ['z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', 'Clear All'],
        ['Space']]

    

    def __init__(self, controller, rootFrame, entry): 
        self.keypadFrame = tk.Frame(rootFrame, width=1500, height=870)
        self.keypadFrame.place(x=0, y=50)
        self.controller = controller
        self.entry = entry
        self.textBox = rootFrame.textBox
        
        if len(self.buttons) == 0:
            self.make_letterpad()
        else:
            self._refresh_letterpad()

    """ General functions below """

    

    def _get_index_in_keyList(self, caption):
        index = 0
        if caption and (len(caption)==1 or caption == "Space" or caption == "Clear" or caption == "Clear All" or caption == "Speak" or caption == "<-"):
            for i in range(len(self.keyList)):
                for key in self.keyList[i]:
                    if caption == key:
                        self.lastPressedKeyIndex = index
                        return index
                    else:
                        index += 1
        else:
            index = self.lastPressedKeyIndex
        # print(f"caption ({caption}) is not in the keyList, index = {index}.")
        return index


    def _get_current_button_attribute(self, caption):
        self.record_button_position()
        index = self._get_index_in_keyList(caption)
        if index < len(self.buttonsAttributes):
            currentBtnAttr = self.buttonsAttributes[index]
        else:
            # currentBtnAttr = get previous key press
            pass
        
        return currentBtnAttr

    def record_button_position(self):
        shiftCompensationX = 0 #  by calculating the shift for each shift when click On/Off of Dragable function
        shiftCompensationY = 103 # (0, 103) is the shift compensation for Dell XPS, full screen 
        self.buttonsAttributes = []
        for button in self.buttons:
            self.buttonsAttributes.append([button.winfo_name(), button.winfo_rootx()-shiftCompensationX, button.winfo_rooty()-shiftCompensationY, button.winfo_width(), button.winfo_height()])            
    
    def write_button_position(self):

        timestr = time.strftime("%Y%m%d_%H%M%S")
        fileName = "./analysis/ui_setting/key_layout_"+str(timestr)+".txt"
        f = open(fileName, "w")
        for button in self.buttons:
            indexKeyList = int(button.winfo_name())
            caption = ""
            if indexKeyList < 11:
                caption = self.keyList[0][indexKeyList]
            elif indexKeyList < 21: 
                caption = self.keyList[1][indexKeyList-11]
            elif indexKeyList < 31: 
                caption = self.keyList[2][indexKeyList-21]
            else: 
                caption = self.keyList[3][indexKeyList-31]

            key = "index: " + str(indexKeyList) + ", caption: " + caption + ", placeX: " + str(button.winfo_rootx()) + ", placeY: " + str(button.winfo_rooty()) + ", sizeX: " + str(button.winfo_width()) + ", sizeY: " + str(button.winfo_height()) + "\n"
            f.write(key)
        f.close()
        print("saved keyboard layout")

    def pop_up_layout_saved_notification(self):
        ctypes.windll.user32.MessageBoxW(0, "Current keypad layout has been saved.", "Info", 0)

    def auto_load_the_latest_button_position(self):
        if not os.listdir('./analysis/ui_setting/'):
            # If no previous setting (i.e. folder is empty), load the default one
            self.make_letterpad()
        else:
            # If there are previous settings (i.e. folder is not empty), load the latest one
            fileList = glob.glob('./analysis/ui_setting/*.txt')
            latestFile = max(fileList, key=os.path.getctime)
            self._load_button_position(latestFile)

    def _load_button_position(self, filePath):
        # print("load button position")
        # print(filePath)
        shiftCompensationX = 0 #  by calculating the shift for each shift when click On/Off of Dragable function
        shiftCompensationY = 103 # (0, 103) is the shift compensation for Dell XPS, full screen 

        # read line by line 
        with open(filePath) as f:
            lines = f.readlines()
        
        # assign to self.buttonsAttributes
        for line in lines:
            index = line[line.find("index: ")+len("index: ") : line.find(", caption")]
            caption = line[line.find("caption: ")+len("caption: ") : line.find(", placeX")]
            placeX = line[line.find("placeX: ")+len("placeX: ") : line.find(", placeY")]
            placeY = line[line.find("placeY: ")+len("placeY: ") : line.find(", sizeX")]
            sizeX = line[line.find("sizeX: ")+len("sizeX: ") : line.find(", sizeY")]
            sizeY = line[line.find("sizeY: ")+len("sizeY: ") : line.find("\n")]
            self.buttons.append(self._make_button(self.keypadFrame, caption, int(placeX)-shiftCompensationX, int(placeY)-shiftCompensationY, sizeX, sizeY, index))
            # self.buttons.append(self._make_button(self.keypadFrame, caption, int(placeX), int(placeY), sizeX, sizeY, index))

        # call self._refresh()

        


    def browse_button_position_files(self):
        filePath = filedialog.askopenfilename(initialdir="/",title="Select a File", filetypes=(("Text files", "*.txt"),))
        # fileName = Path(filePath).stem
        self.controller.traceLogFile = filePath
        self._load_button_position(filePath)

    """ General functions above """


    


    """ word prediction below """

    def _make_word_prediction_button(self, frame, predWord, currentBtnPlaceX, currentBtnPlaceY, previousX):
        command = (lambda button=predWord: self.controller.on_predicted_word_button_click(button+' '))
        x = 0
        y = 0

        predWordBtn = tk.Button(frame, text=predWord, command=command, pady=5, bg='#C0C0C0', fg='black', font=('Calibri', 22))

        if self.BOOL_WORD_PRED_PRESSED_KEY:
            x = currentBtnPlaceX + previousX
            y = currentBtnPlaceY - predWordBtn.winfo_reqheight() - self.PRED_WORD_ROW_GAP
        else:
            x = self.PRED_WORD_INIT_LOC_X + previousX
            y = self.PRED_WORD_INIT_LOC_Y - predWordBtn.winfo_reqheight()

        predWordBtn.place(x=x, y=y)

        previousX = previousX + predWordBtn.winfo_reqwidth() + self.PRED_WORD_COL_GAP
        # print(f"predWord = {predWord}")
        # print(f"predWordBtn.winfo_reqwidth() = {predWordBtn.winfo_reqwidth()}")
        
        if self.KEY_DRAGABLE:
            self._make_dragable(predWordBtn) # , predWord

        return predWordBtn, previousX

    def clear_placed_words(self):
        if self.predictedWordButtons:
            for predWordBtn in self.predictedWordButtons:
                predWordBtn.destroy()
            self.predictedWordButtons = []

    def place_predicted_words(self, caption, predWords):

        currentBtnAttr = self._get_current_button_attribute(caption)
        
        previousX = 0
        if len(predWords) < self.WORD_PRED_NUM:
            for word in predWords: 
                predictedWordBtn, previousX = self._make_word_prediction_button(frame=self.keypadFrame, predWord=word, currentBtnPlaceX=currentBtnAttr[1], currentBtnPlaceY=currentBtnAttr[2], previousX=previousX)
                self.predictedWordButtons.append(predictedWordBtn)
        else:
            for i in range(self.WORD_PRED_NUM):
                predictedWordBtn, previousX = self._make_word_prediction_button(frame=self.keypadFrame, predWord=predWords[i], currentBtnPlaceX=currentBtnAttr[1], currentBtnPlaceY=currentBtnAttr[2], previousX=previousX) # self.wordPred
                self.predictedWordButtons.append(predictedWordBtn)

        # return predictedWordButtons

    """ word prediction above """

    """ sentence prediction below """  

    def _make_sentence_prediction_button(self, frame, predSentence, previousY):
        command = (lambda button=predSentence: self.controller.on_predicted_sentence_button_click(button))

        predSentenceBtn = tk.Button(frame, text=predSentence, command=command, wraplength=350, justify='left', pady=5, bg='#C0C0C0', fg='black', font=('Calibri', 22))
        x = self.PRED_SENT_INIT_LOC_X
        y = self.PRED_SENT_INIT_LOC_Y + previousY
        # print(f"In view_main, _make_sentence_prediction_button: predSentence = {predSentence}")

        predSentenceBtn.place(x=x, y=y)
        previousY = previousY + predSentenceBtn.winfo_reqheight() + self.PRED_SENT_COL_GAP

        if self.KEY_DRAGABLE:
            self._make_dragable(predSentenceBtn) # , predSentence
        
        return predSentenceBtn, previousY

    def place_predicted_sentences(self, predSentence):
        previousY = 0
        print(f"In view_main, predSentence button: {predSentence}, lenth: {len(predSentence)}")
        if len(predSentence) < self.SENT_PRED_NUM:
            for sentence in predSentence: 
                predictedSentenceBtn, previousY = self._make_sentence_prediction_button(frame=self.keypadFrame, predSentence=sentence, previousY=previousY)
                self.predictedSentenceButtons.append(predictedSentenceBtn)
        else:
            for i in range(self.SENT_PRED_NUM):
                predictedSentenceBtn, previousY = self._make_sentence_prediction_button(frame=self.keypadFrame, predSentence=predSentence[i], previousY=previousY) # self.wordPred
                self.predictedSentenceButtons.append(predictedSentenceBtn)  

    def clear_placed_sentences(self):
        if self.predictedSentenceButtons:
            for predSentenceBtn in self.predictedSentenceButtons:
                predSentenceBtn.destroy()
            self.predictedSentenceButtons = []

    

    """ sentence prediction above """

    """ refresh letterpad below """

    def _refresh_letterpad(self):
        
        self.buttons = []
        for btn in self.buttonsAttributes:
            index = int(btn[0])
            placeX = btn[1]
            placeY = btn[2]
            sizeX = btn[3]
            sizeY = btn[4]

            
            if int(index/len(self.keyList[0])) == 0:
                caption = self.keyList[0][index]
            elif int(index/len(self.keyList[0]) > 0 and index/(len(self.keyList[0])+len(self.keyList[1]))) == 0:
                caption = self.keyList[1][index%len(self.keyList[0])]
            elif int(index/(len(self.keyList[0])+len(self.keyList[1])) > 0 and index/(len(self.keyList[0])+len(self.keyList[1])+len(self.keyList[2]))) == 0:
                caption = self.keyList[2][index%(len(self.keyList[0])+len(self.keyList[1]))]
            else:
                caption = self.keyList[3][index%(len(self.keyList[0])+len(self.keyList[1])+len(self.keyList[2]))]

            self.buttons.append(self._make_button(self.keypadFrame, caption, placeX, placeY, sizeX, sizeY, index))
        self.buttonsAttributes = []

    
    def refresh(self, controller, rootFrame, entry):
        self.keypadFrame.destroy()
        self.__init__(controller, rootFrame, entry)

    """ refresh letterpad above """

    

    def make_letterpad(self):
        
        keyIndex = 0

        for row in range(len(self.keyList)):
            
            for keyChar in self.keyList[row]:
                column = self.keyList[row].index(keyChar)

                placeX = 0
                placeY = 0
                sizeX = 0
                sizeY = 0
                indent = 0

                if row>0:
                    indent = self.KEY_INDENT
                
                if keyChar == "Space":
                    indent += self.KEY_SPACE_SIZE_X
                    placeX = indent + self.KEY_INIT_LOC_X + column * (self.KEY_SIZE_X + self.KEY_COL_GAP)
                    placeY = self.KEY_INIT_LOC_Y + row * (self.KEY_SIZE_Y + self.KEY_COL_GAP + self.KEY_ROW_GAP)
                    sizeX = self.KEY_SPACE_SIZE_X
                    sizeY = self.KEY_SPACE_SIZE_Y

                elif keyChar == "Speak":
                    placeX = indent + self.KEY_INIT_LOC_X + column * (self.KEY_SIZE_X + self.KEY_COL_GAP)
                    placeY = self.KEY_INIT_LOC_Y + row * (self.KEY_SIZE_Y + self.KEY_COL_GAP + self.KEY_ROW_GAP)
                    sizeX = self.KEY_SPEAK_SIZE_X
                    sizeY = self.KEY_SPEAK_SIZE_Y

                elif keyChar == "Clear All":
                    placeX = indent + self.KEY_INIT_LOC_X + column * (self.KEY_SIZE_X + self.KEY_COL_GAP)
                    placeY = self.KEY_INIT_LOC_Y + row * (self.KEY_SIZE_Y + self.KEY_COL_GAP + self.KEY_ROW_GAP)
                    sizeX = self.KEY_CLEAR_SIZE_X
                    sizeY = self.KEY_CLEAR_SIZE_Y

                else:
                    placeX = indent + self.KEY_INIT_LOC_X + column * (self.KEY_SIZE_X + self.KEY_COL_GAP)
                    placeY = self.KEY_INIT_LOC_Y + row * (self.KEY_SIZE_Y + self.KEY_COL_GAP + self.KEY_ROW_GAP)
                    sizeX = self.KEY_SIZE_X
                    sizeY = self.KEY_SIZE_Y
                
                self.buttons.append(self._make_button(self.keypadFrame, keyChar, placeX, placeY, sizeX, sizeY, keyIndex))
                keyIndex+=1
                self.buttonsAttributes = []





    def _make_dragable(self,widget): # ,caption
        widget.bind("<Button-1>", self._on_drag_start)
        widget.bind("<B1-Motion>", self._on_drag_motion)
        # widget.caption = caption

        

    def _on_drag_start(self, event):
        widget = event.widget
        widget._drag_start_x = event.x
        widget._drag_start_y = event.y

    def _on_drag_motion(self, event):
        widget = event.widget
        x = widget.winfo_x() - widget._drag_start_x + event.x
        y = widget.winfo_y() - widget._drag_start_y + event.y
        widget.place(x=x, y=y)

    def _make_button(self, frame, caption, placeX, placeY, sizeX, sizeY, index):
        command = (lambda button=caption: self.controller.on_key_button_click(button))
        

        keyBtn = tk.Button(frame, name=str(index), text=caption, command=command, bg='#C0C0C0', fg='black', font=('Calibri', 26))
        keyBtn.place(x=placeX, y=placeY, width=sizeX, height=sizeY)
        
        if self.KEY_DRAGABLE:
            self._make_dragable(keyBtn) # , caption
        return keyBtn








class View_menu:
    
    def __init__(self, controller, rootFrame):
        self.rootFrame = rootFrame
        self.controller = controller
        self._make_menu()
        self.tinkerView = View_tinker(self.controller)
        self.traceView = View_trace_analysis(self.controller)


    def _make_menu(self):
        def donothing():
            pass

        menuBar = tk.Menu(self.rootFrame)
        self.rootFrame.config(menu=menuBar)
        

        # fileMenu = tk.Menu(menuBar)
        # menuBar.add_cascade(label="File", menu=fileMenu)
        # fileMenu.add_command(label="Save Current Prediction Settings", font= ('', 50), command=lambda:self.controller.save_current_prediction_settings())
        # fileMenu.add_command(label="Load Previous Prediction Settings...", command=lambda:self.controller.load_previous_prediction_settings())


        uiControlMenu = tk.Menu(menuBar)
        menuBar.add_cascade(label="UI Control", menu=uiControlMenu, font=('Arial', 16))

        moveElementMenu = tk.Menu(uiControlMenu)
        uiControlMenu.add_cascade(label="Move Elements", font= ('Arial', 16), menu=moveElementMenu)
        moveElementMenu.add_command(label="On", font= ('Arial', 16), command=lambda:self.controller.set_drag(True))
        moveElementMenu.add_command(label="Off", font= ('Arial', 16), command=lambda:self.controller.set_drag(False))

        # uiControlMenu.add_command(label="Change the Button Size", command=lambda:self.controller.set_btn_size())
        uiControlMenu.add_command(label="Default Layout", font= ('Arial', 16), command=lambda:self.controller.load_default_layout())
        uiControlMenu.add_command(label="Save the Current Layout", font= ('Arial', 16), command=lambda:self.controller.save_current_keyboard_layout())
        uiControlMenu.add_command(label="Load Previous Layout...", font= ('Arial', 16), command=lambda:self.controller.load_previous_keyboard_layout())

        tinkerMenu = tk.Menu(menuBar)
        menuBar.add_cascade(label="Tinker", menu=tinkerMenu, font=('Arial', 16))
        tinkerMenu.add_command(label="Default Prediction Setting", font= ('Arial', 16), command=lambda:self.tinkerView.default_setting())
        tinkerMenu.add_command(label="Open Tinker Panel...", font= ('Arial', 16), command=lambda:self.tinkerView.run())
        tinkerMenu.add_command(label="Save Current Prediction Settings", font= ('Arial', 16), command=lambda:self.controller.save_current_prediction_settings())
        tinkerMenu.add_command(label="Load Previous Prediction Settings...", font= ('Arial', 16), command=lambda:self.controller.load_previous_prediction_settings())


        traceAnalysisMenu = tk.Menu(menuBar)
        menuBar.add_cascade(label="Trace Analysis",  menu=traceAnalysisMenu, font=('Arial', 16))

        traceTyping = tk.Menu(traceAnalysisMenu)
        traceAnalysisMenu.add_cascade(label="Trace Typing", font= ('Arial', 16), menu=traceTyping)
        traceTyping.add_command(label="On", font= ('Arial', 16), command=lambda:self.controller.set_trace(True))
        traceTyping.add_command(label="Off", font= ('Arial', 16), command=lambda:self.controller.set_trace(False))

        traceAnalysisMenu.add_command(label="Open Trace Analysis Panel...", font= ('Arial', 16), command=lambda:self.traceView.run())
