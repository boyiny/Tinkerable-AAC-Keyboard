from model_main import Model_main
from view_main import View_main, View_menu, View_entry, View_keypad


class Controller_main():
    def __init__(self):
        self.modelMain = Model_main()
        self.viewMain = View_main(self)
        
        self.viewEntry = View_entry(self, self.viewMain)
        self.viewKeypad = View_keypad(self, self.viewMain, self.viewEntry)
        self.viewMenu = View_menu(self, self.viewMain)

        self.currentPressedKey = ""


    def main(self):
        self.viewMain.mainloop()

    def on_key_button_click(self, caption): # , boolWordPred, boolSenPred
        # if boolWordPred:
        # # get current entry
        #     entry = self.viewEntry.entry.get()
        self.currentPressedKey = caption


        text = self.modelMain.edit_text(caption)
        self.viewMain.textBox.set(text)
        # print(f'button in lambda is: {caption}')
        # if boolWordPred:
        #     self.viewKeypad.make_word_prediction()

    """ Word Prediction Below """

    def set_word_pred_display(self, bool):
        if bool:
            # turn on the display
            print(f"Set word prediction display: On")
            self.set_word_pred_on_last_pressed_key(True)
        else:
            # turn off the display
            print(f"Set word prediction display: Off")



    def set_word_pred_on_last_pressed_key(self, bool):
        entry = self.viewEntry.entry.get()
        predictedWord = self._make_word_prediction(entry)
        self.currentPressedKey= "h"

        
        if bool and self.currentPressedKey != "" :
            # on_last_pressed_key
            # clear fixed word pred
            self.viewKeypad.place_predicted_words(self.currentPressedKey, predWords=predictedWord, predNum=40, boolOnTopOfPressedKey=bool)
        else:
            # on fixed location
            # clear last pressed 
            self.viewKeypad.place_predicted_words(self.currentPressedKey, predWords=predictedWord, predNum=40, boolOnTopOfPressedKey=bool)
    
    def _make_word_prediction(self, entry):
        predictedWord = self.modelMain.make_word_prediction(entry)
        return predictedWord
        # show word pred

    def _present_location_word_prediction(self, bool, predWord):
        if bool:

            # get pressed key location
            pass
        else:
            pass

    def on_word_prediction_click(self, entry, boolOnTopOfPressedKey):
        # predictedWord = self.modelMain.edit_text(entry)
        
        text = self.viewKeypad.make_word_prediction(predictedWord, boolOnTopOfPressedKey)
        self.viewMain.textBox.set(text)

    """ Word Prediction Above """
    
    def set_drag(self, boolDrag):
        self.viewKeypad.KEY_DRAGABLE = self.modelMain.set_drag(boolDrag)
        self.viewKeypad.record_button_position()
        self.viewKeypad.refresh(self, self.viewMain, self.viewEntry)


if __name__ == '__main__':
    keyboard = Controller_main()
    keyboard.main()