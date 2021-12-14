from model_main import Model_main
from view_main import View_main


class Controller_main():
    def __init__(self):
        self.modelMain = Model_main()
        self.viewMain = View_main(self)
        


    def main(self):
        self.viewMain.mainloop()

    def on_button_click(self, caption):
        text = self.modelMain.edit_text(caption)
        self.viewMain.textBox.set(text)
  

if __name__ == '__main__':
    keyboard = Controller_main()
    keyboard.main()