from datetime import datetime
import re

from sympy import li

class Model_Trace_Analysis:
    def __init__(self):
        self.txt_path = './Dataset/typing_log.txt'
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
        currentTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        self.f = open(self.txt_path, 'a')
        self.f.write(currentTime + ' >> ' + caption+'\n')
        self.f.close()
    """ trace typing above """

# Start trace analysis

    """ Extract data from a line below """
    def _extract_info_from_line(self, line):
        dateTime = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d{3}', line)
        # time = re.search(r'\d{2}:\d{2}:\d{2}.d{3}', line)
        dateTimeObj = datetime.strptime(dateTime.group(0), '%Y-%m-%d %H:%M:%S.%f')
        
        inputType = line[line.find('>> ')+3:line.rfind(': ')]
        input = line[line.rfind(': ')+2:line.rfind('\n')]

        logDict = { 'date': dateTimeObj.date(), 
                    'hour': dateTimeObj.hour, 
                    'minute': dateTimeObj.minute, 
                    'second': dateTimeObj.second, 
                    'microsecond': dateTimeObj.microsecond,
                    'type': inputType, 
                    'input': input}

        return logDict
    """ Extract data from a line above """

    """ Run trace analyse below """

    def run_trace_analyse(self, traceLogFile):
        # print("In model_trace_analyse using file: " + traceLogFile)
        with open(traceLogFile) as f:
            lines = f.readlines()
        
        boolLogData = False
        logDictList = []
        for line in lines:
            if 'Start a new log' in line:
                boolLogData = True
                continue
            if 'End the log' in line:
                boolLogData = False
                break
            if boolLogData:
                logDictList.append(self._extract_info_from_line(line))
        print("log dictionary list:")
        print(logDictList)      



    """ Run trace analyse above """

