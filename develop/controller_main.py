from model_main import Model_main
from view_main import View_main, View_menu, View_entry, View_keypad


class Controller_main():
    def __init__(self):
        self.modelMain = Model_main()
        self.viewMain = View_main(self)
        self.viewMenu = View_menu(self, self.viewMain)
        self.viewEntry = View_entry(self, self.viewMain)
        self.viewKeypad = View_keypad(self, self.viewMain, self.viewEntry)

        

    def main(self):
        self.viewMain.mainloop()

    def on_button_click(self, caption):
        text = self.modelMain.edit_text(caption)
        self.viewMain.textBox.set(text)
    
    def set_drag(self, boolDrag):
        self.viewKeypad.KEY_DRAGABLE = self.modelMain.set_drag(boolDrag)
        self.viewKeypad.record_button_position()
        self.viewKeypad.refresh(self, self.viewMain, self.viewEntry)


if __name__ == '__main__':
    keyboard = Controller_main()
    keyboard.main()