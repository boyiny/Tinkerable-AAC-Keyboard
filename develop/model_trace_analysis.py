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
    def record_pressed_button(self, caption, wordPred, senPred):
        currentTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        self.f = open(self.txt_path, 'a')
        self.f.write(currentTime + ' >> ' + caption + ', word pred: '+ '|'.join(wordPred) + ', sentence pred: '+ '|'.join(senPred)+ '\n')
        self.f.close()
    """ trace typing above """

# Start trace analysis

    """ Extract data from a line below """
    def _extract_info_from_line(self, line):
        dateTime = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d{3}', line)
        # time = re.search(r'\d{2}:\d{2}:\d{2}.d{3}', line)
        dateTimeObj = datetime.strptime(dateTime.group(0), '%Y-%m-%d %H:%M:%S.%f')
        
        keyType = line[line.find('>> ')+3 : line[line.find('>> ')+3:].find(': ')+line.find('>> ')+3]
        print(line.find('>> '))
        print(line[line.find('>> ')+3:].find(': '))

        key = line[line.find(keyType)+len(keyType)+2 : line.find(', word pred: ')]
        wordPred = line[line.find(', word pred: ')+len(', word pred: ') : line.find(', sentence pred: ')]
        senPred = line[line.find(', sentence pred: ')+len(', sentence pred: ') : line.find('\n')]

        wordPredList = wordPred.split('|')
        senPredList = senPred.split('|')

        logDict = { 'date': dateTimeObj.date(), 
                    'hour': dateTimeObj.hour, 
                    'minute': dateTimeObj.minute, 
                    'second': float(dateTimeObj.second+dateTimeObj.microsecond/1000000.0), 
                    # 'microsecond': dateTimeObj.microsecond,
                    'keyType': keyType, 
                    'keyValue': key,
                    'wordPred': wordPredList,
                    'sentencePred': senPredList}

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

