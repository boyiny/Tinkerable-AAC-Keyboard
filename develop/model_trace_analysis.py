from data_types import Word_importance
from datetime import datetime

class Model_Trace_Analysis:
    def __init__(self):
        self.txt_path = './Develop/Dataset/typing_log.txt'
        self.f = open(self.txt_path, 'a')
        print("trace analysis initialisation")
        

    def set_trace(self, boolTrace):
        if boolTrace == True:
            self.f = open(self.txt_path, 'a')
            self.f.write("----------------Start a new log----------------\n")
            self.f.close()
            print("trace on")
        else:
            self.f = open(self.txt_path, 'a')
            self.f.write("----------------End the log----------------\n")
            self.f.close()
            print("trace off")
        return boolTrace

    """ trace typing below """
    def record_pressed_button(self, caption):
        currentTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        self.f = open(self.txt_path, 'a')
        self.f.write(currentTime + ' >> ' + caption+'\n')
        self.f.close()
        
        
    """ trace typing above """