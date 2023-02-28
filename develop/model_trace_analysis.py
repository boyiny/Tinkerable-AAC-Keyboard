from datetime import datetime
import re
import string
import pandas as pd
import time

from sympy import li

class Model_Trace_Analysis:
    def __init__(self):
        timestr = time.strftime("%Y%m%d_%H%M%S")
        self.txt_path = './analysis/klm_bei_record/typing_log_'+str(timestr)+'.txt'
        self.result_path = './analysis/klm_bei_record/human_factor_analysis_'+str(timestr)+'.xlsx'
        self.f = open(self.txt_path, 'a+')
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
    def record_pressed_button(self, caption, wordPred, senPred, currentSen):
        currentTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        self.f = open(self.txt_path, 'a')
        self.f.write(currentTime + ' >> ' + caption + ', word pred: '+ '|'.join(wordPred).lower() + ', sentence pred: '+ '|'.join(senPred).lower()+ ', current sentence: '+ currentSen +'\n')
        self.f.close()
    """ trace typing above """

# Start trace analysis

    """ Extract data from a line below """
    def _extract_info_from_line(self, line):
        dateTime = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d{3}', line)
        # time = re.search(r'\d{2}:\d{2}:\d{2}.d{3}', line)
        dateTimeObj = datetime.strptime(dateTime.group(0), '%Y-%m-%d %H:%M:%S.%f')
        
        keyType = line[line.find('>> ')+3 : line[line.find('>> ')+3:].find(': ')+line.find('>> ')+3]


        keyValue = line[line.find(keyType)+len(keyType)+2 : line.find(', word pred: ')]
        if keyValue != 'Speak' and keyValue != 'Space' and keyValue != 'Clear All':
            keyValue.lower()
        wordPred = line[line.find(', word pred: ')+len(', word pred: ') : line.find(', sentence pred: ')].lower()
        senPred = line[line.find(', sentence pred: ')+len(', sentence pred: ') : line.find(', current sentence: ')].lower()
        currentSentence = line[line.find(', current sentence: ')+len(', current sentence: ') : line.find('\n')].lower()

        wordPredList = wordPred.split('|')
        senPredList = senPred.split('|')

        logDict = { 'timeTag': dateTimeObj,  
                    'keyType': keyType, 
                    'keyValue': keyValue,
                    'wordPred': wordPredList,
                    'sentencePred': senPredList,
                    'wordPredRoundIndex': 0,
                    'sentencePredRoundIndex': 0,
                    'currentSentence': currentSentence}

        return logDict
    """ Extract data from a line above """

    """ Run trace analyse below """

    def run_trace_analyse(self, traceLogFile, T_interrupt_threshold):
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
        
        # seprate by sentences
        oneSentence = []
        
        # result summary
        humanFactorsDistList = []

        sentenceNum = 0
        for line in logDictList:
            if line['keyValue'] != 'Speak':
                oneSentence.append(line)
            else:
                oneSentence.append(line)
                # Start analysis this sentence
                KS_all_temp, sentenceLengthInWord, sentenceLengthInChar, T_all_temp, KS_error_correction_temp, T_error_correction_temp, KS_irra_extra_temp, T_irra_extra_temp, T_interrupt_temp = self._cal_human_factors(oneSentence, T_interrupt_threshold)
                humanFactorsDist = {
                    'sentenceNum': sentenceNum,
                    'sentence': oneSentence,
                    'KS_all': KS_all_temp,
                    'sentenceLengthInWord': sentenceLengthInWord, 
                    'sentenceLengthInChar': sentenceLengthInChar,
                    'T_all': T_all_temp,
                    'KS_error_correction': KS_error_correction_temp,
                    'T_error_correction': T_error_correction_temp,
                    'KS_irra_extra': KS_irra_extra_temp,
                    'T_irra_extra': T_irra_extra_temp,
                    'T_interrupt': T_interrupt_temp,
                    'entry_rate': sentenceLengthInWord/(T_all_temp/60.0),
                    'KS_saving_rate': (sentenceLengthInChar-KS_all_temp)/sentenceLengthInChar,
                    'ETRI': 1 - T_error_correction_temp/(T_all_temp-T_interrupt_temp),
                    'EI': KS_error_correction_temp/(KS_all_temp-KS_irra_extra_temp),
                    'RI': 1 - KS_irra_extra_temp/(KS_all_temp-KS_error_correction_temp),
                    'II_KS': 1 - (KS_error_correction_temp+KS_irra_extra_temp)/KS_all_temp,
                    'II_T': 1 - (T_error_correction_temp+T_irra_extra_temp+T_interrupt_temp)/T_all_temp
                }
                humanFactorsDistList.append(humanFactorsDist)
                
                print('Sentence ' + str(sentenceNum) + ' human factor: ')
                print('ETRI = '+str(humanFactorsDist['ETRI']))
                print('EI = '+str(humanFactorsDist['EI']))
                print('RI = '+str(humanFactorsDist['RI']))
                print('II_KS = '+str(humanFactorsDist['II_KS']))
                print('II_T = '+str(humanFactorsDist['II_T']))

                oneSentence = []
                sentenceNum += 1


        # Overall human performance
        KS_all = 0
        T_all = 0.0
        KS_error_correction = 0
        T_error_correction = 0.0
        KS_irra_extra = 0
        T_irra_extra = 0.0
        T_interrupt = 0.0
        for hf in humanFactorsDistList:
            KS_all += hf['KS_all']
            T_all += hf['T_all']
            KS_error_correction += hf['KS_error_correction']
            T_error_correction += hf['T_error_correction']
            KS_irra_extra += hf['KS_irra_extra']
            T_irra_extra += hf['T_irra_extra']
            T_interrupt += hf['T_interrupt']
        
        ETRI = 1 - T_error_correction/(T_all-T_interrupt),
        EI = KS_error_correction/(KS_all-KS_irra_extra),
        RI = 1 - KS_irra_extra/(KS_all-KS_error_correction),
        II_KS = 1 - (KS_error_correction+KS_irra_extra)/KS_all,
        II_T = 1 - (T_error_correction+T_irra_extra+T_interrupt)/T_all

        print('Overall human factors: ')
        print('ETRI = '+str(ETRI))
        print('EI = '+str(EI))
        print('RI = '+str(RI))
        print('II_KS = '+str(II_KS))
        print('II_T = '+str(II_T))

        df = pd.DataFrame.from_dict(humanFactorsDistList)
        df.to_excel(self.result_path)



    """ Run trace analyse above """

    def _add_to_pred_pool(self, index, timeTag, predList):
        dict = {}
        dict['round'] = index
        dict['timeTag'] = timeTag
        dict['prediction'] = predList
        return dict


    def _cal_human_factors(self, logDictList, T_interrupt_threshold):
        KS_current = 0
        sentenceLengthInWord = 0
        sentenceLengthInChar = 0
        if logDictList:
            T_all = (logDictList[-1]['timeTag'] - logDictList[0]['timeTag']).total_seconds()

        KS_irra_extra = 0
        T_irra_extra = 0.0
        word_irra_extra_buffer = []

        KS_error_correction = 0
        T_error_correction = 0.0
        boolDeletionCombo = False
        N_deletion_combo = 0
        errorSentence = ""
        lastSentence = ""

        T_interrupt = 0.0
        lastLogDict = {}

        currentWordPredFistShowInRound = {}
        currentSentencePredFistIrrationalAction = {}

        currentWord = ""
        currentSentence = ""

        currentWordPredListDictList = []
        currentSentencePredListDictList = []
        currentWordPredRoundIndex = 0
        currentSentencePredRoundIndex = 0

        boolCheckWordPredIrrational = False
        boolCheckSentencePredIrrational = False

        boolFirstWord = True
        
        for logDict in logDictList:
            KS_current += 1
            boolFinishAWord = False
            boolFinishASentence = False
            currentSentence = logDict['currentSentence']

            if logDict.get('keyValue') == 'Space' or logDict.get('keyValue') == ',' or logDict.get('keyValue') == '.' or logDict.get('keyType') == 'word' or logDict.get('keyType') == 'sentence':
                # indicate the end of a word
                boolFinishAWord = True
                boolFinishASentence = False
            if logDict.get('keyValue') == 'Speak':
                # indicate the end of a sentence
                boolFinishAWord = True
                boolFinishASentence = True 
            
            """Form a sentence below """

            if logDict.get('keyType') == 'key':
                # Delete a letter
                if logDict.get('keyValue') == '<-':
                    print("<-, Error sentence: "+logDict['currentSentence'])
                    if N_deletion_combo == 0:
                        errorSentence = lastSentence
                    N_deletion_combo += 1
                    if currentWord:
                        currentWord = currentWord[:-1]
                # Typing a word
                elif boolFinishAWord == False:
                    if N_deletion_combo != 0:
                        boolDeletionCombo = True

                    currentWord = currentWord + logDict.get('keyValue')
                    # Extend wordPred and sentencePred list
                    if boolFirstWord == True:
                        boolFirstWord = False
                    else:
                        currentWordPredRoundIndex += 1
                        currentSentencePredRoundIndex += 1
                    currentWordPredListDictList.append(self._add_to_pred_pool(index=currentWordPredRoundIndex, timeTag=logDict.get('timeTag'), predList=logDict.get('wordPred')))
                    currentSentencePredListDictList.append(self._add_to_pred_pool(index=currentSentencePredRoundIndex, timeTag=logDict.get('timeTag'), predList=logDict.get('sentencePred')))
                    currentWordPredPool = ''
                    currentSentencePredPool = ''
                    currentWordPredPoolDictList = []
                    currentSentencePoolDictList = []
                    for currentWordPred in currentWordPredListDictList:
                        currentWordPredPool = currentWordPredPool + str(currentWordPred['round']) +': '+ '||'.join(currentWordPred['prediction']) + '; '
                        tempDict = {
                            'round': currentWordPred['round'],
                            'prediction': currentWordPred['prediction']
                        }
                        currentWordPredPoolDictList.append(tempDict)
                    for currentSentencePred in currentSentencePredListDictList:
                        currentSentencePredPool = currentSentencePredPool + str(currentSentencePred['round']) + ': ' + '||'.join(currentSentencePred['prediction'])+ '; '
                        tempDict = {
                            'round': currentSentencePred['round'],
                            'prediction': currentSentencePred['prediction']
                        }
                        currentSentencePoolDictList.append(tempDict)

                    print('Typing a word, currentWord: '+currentWord)
                    print('   current word prediction: '+'|'.join(logDict.get('wordPred')))
                    print('   current sentence prediction: '+'|'.join(logDict.get('sentencePred')))
                    print('      current word prediction pool: '+currentWordPredPool)
                    print('      current sentence prediction pool: '+currentSentencePredPool)
                    print('         current sentence: '+currentSentence)
                
                # currentSentence = logDict['currentSentence']
                if boolDeletionCombo == True:
                    # Find when errorStartSentence first shows in log
                    errorStart = 0
                    if N_deletion_combo > 1:
                        errorStartSentence = errorSentence[:-(N_deletion_combo-1)]
                    else:
                        errorStartSentence = errorSentence
                    for tempLog in logDictList[:KS_current]:
                        errorStart += 1
                        if errorStartSentence == tempLog['currentSentence']:
                            break
                    # Calculate deletion and error time and KS
                    if errorStart != 0:
                        # current sentence is shown before, account error KS and time
                        KS_error_correction += KS_current - errorStart
                        T_error_correction += (logDict['timeTag'] - logDictList[errorStart-1]['timeTag']).total_seconds()
                    else:
                        # current sentence is not shown before, only add correction KS and time (select a pred word but delete part of it)
                        KS_error_correction += N_deletion_combo
                        T_error_correction += (logDict['timeTag'] - logDictList[KS_current-N_deletion_combo]['timeTag']).total_seconds()
                    boolDeletionCombo = False
                    N_deletion_combo = 0
                    errorSentence = ""
                

            if boolFinishAWord == True and boolFinishASentence == False and logDict.get('keyType') != 'sentence':
                # A word is finished, but the sentence is not finished
                if logDict.get('keyType') == 'word':
                    # Use word prediction to finish the word
                    currentWord = logDict.get('keyValue').lower()
                
                # Check word rationality
                currentWord = currentWord.strip().lower()
                currentWordFinishInRound = len(currentWordPredListDictList) # Finishes in the next round that is not recorded in this list, therefore we use the maximum round in the list plus one
                currentWordFinishTime = logDict['timeTag']
                currentWordPredFirstIrrationalAction = {}
                for recordByRound in currentWordPredListDictList:
                    # Record the first miss of the predicted word
                    if currentWord in recordByRound['prediction'] and len(currentWord)>1:
                        if boolCheckWordPredIrrational == True:
                            currentWordPredFirstIrrationalAction = {
                                'round': recordByRound['round'],
                                'timeTag': recordByRound['timeTag']}
                            KS_irra_extra = KS_irra_extra + currentWordFinishInRound - currentWordPredFirstIrrationalAction['round'] 
                            T_irra_extra = T_irra_extra + (currentWordFinishTime-currentWordPredFirstIrrationalAction['timeTag']).total_seconds()
                            temp_irra_extra_dict = {
                                'round': KS_current, # in sentence level
                                'KS_irra_extra': KS_irra_extra,
                                'T_irra_extra': T_irra_extra
                            }
                            word_irra_extra_buffer.append(temp_irra_extra_dict)
                            print("-> Current KS_irra_extra = "+str(KS_irra_extra))
                            print("-> Current T_irra_extra = "+str(T_irra_extra))
                            break
                        
                        boolCheckWordPredIrrational = True
                            
                boolCheckWordPredIrrational = False
                               
                # Renew wordPred list
                currentWordPredRoundIndex = 0
                currentWordPredListDictList = []
                currentWordPredListDictList.append(self._add_to_pred_pool(index=currentWordPredRoundIndex, timeTag=logDict.get('timeTag'), predList=logDict.get('wordPred')))
                # Extend sentencePred list
                currentSentencePredRoundIndex += 1
                currentSentencePredListDictList.append(self._add_to_pred_pool(index=currentSentencePredRoundIndex, timeTag=logDict.get('timeTag'), predList=logDict.get('sentencePred')))
                print('A word is finished, currentWord: '+currentWord+', currentSentence: '+currentSentence+'*')
                
                # print trace
                currentWordPredPool = ''
                currentSentencePredPool = ''
                currentWordPredPoolDictList = []
                currentSentencePredPoolDictList = []
                for currentWordPred in currentWordPredListDictList:
                    currentWordPredPool = currentWordPredPool + str(currentWordPred['round']) +': '+ '||'.join(currentWordPred['prediction']) + '; '
                    tempDict = {
                            'round': currentWordPred['round'],
                            'prediction': currentWordPred['prediction']
                        }
                    currentWordPredPoolDictList.append(tempDict)
                for currentSentencePred in currentSentencePredListDictList:
                    currentSentencePredPool = currentSentencePredPool + str(currentSentencePred['round']) + ': ' + '||'.join(currentSentencePred['prediction'])+ '; '
                    tempDict = {
                        'round': currentSentencePred['round'],
                        'prediction': currentSentencePred['prediction']
                    }
                    currentSentencePredPoolDictList.append(tempDict)
                print('   current word prediction: '+'|'.join(logDict.get('wordPred')))
                print('   current sentence prediction: '+'|'.join(logDict.get('sentencePred')))
                print('      current word prediction pool: '+currentWordPredPool)
                print('      current sentence prediction pool: '+currentSentencePredPool)
                print('         current sentence: '+currentSentence)
                
                currentWord = ''
                # currentWordPredFistShowInRound = None
                currentWordPredFistShowInRound = {}

            if boolFinishAWord == True and boolFinishASentence == False and logDict.get('keyType') == 'sentence':
                # A word is finished, and a sentence prediction is selected 
                currentWord = ''

                # Check sentence rationality
                currentSentenceFinishInRound = len(currentSentencePredListDictList) # Finishes in the next round that is not recorded in this list, therefore we use the maximum round in the list plus one 
                currentSentenceFinishTime = logDict['timeTag']
                for recordByRound in currentSentencePredListDictList:
                    if boolCheckSentencePredIrrational == True:
                            currentSentencePredFistIrrationalAction = {
                                'round': recordByRound['round'], 
                                'timeTag': recordByRound['timeTag']}
                            
                            # Check if the sentence irrational action is after any word finishment actions                       
                            boolIrrationalInSentenceLevel = True
                            if word_irra_extra_buffer:
                                for buffer in reversed(word_irra_extra_buffer):
                                    if buffer['round'] < currentSentencePredFistIrrationalAction['round']:
                                        boolIrrationalInSentenceLevel = False
                                    if boolIrrationalInSentenceLevel == False:
                                        KS_irra_extra = buffer['KS_irra_extra'] + currentSentenceFinishInRound - currentSentencePredFistIrrationalAction['round']
                                        T_irra_extra = buffer['T_irra_extra'] + (currentSentenceFinishTime-currentSentencePredFistIrrationalAction['timeTag']).total_seconds()
                            else:
                                KS_irra_extra = currentSentenceFinishInRound - currentSentencePredFistIrrationalAction['round']
                                T_irra_extra = (currentSentenceFinishTime-currentSentencePredFistIrrationalAction['timeTag']).total_seconds()

                            print("-> Current KS_irra_extra = "+str(KS_irra_extra))
                            print("-> Current T_irra_extra = "+str(T_irra_extra))
                            break
                        
                    if currentSentence.strip() in recordByRound['prediction']:
                        boolCheckSentencePredIrrational = True

                        
                boolCheckSentencePredIrrational = False

                # Renew the wordPred and sentencePred list
                currentWordPredRoundIndex += 1
                currentSentencePredRoundIndex += 1
                
                currentWordPredListDictList.append(self._add_to_pred_pool(index=currentWordPredRoundIndex, timeTag=logDict.get('timeTag'), predList=logDict.get('wordPred')))
                currentSentencePredListDictList.append(self._add_to_pred_pool(index=currentSentencePredRoundIndex, timeTag=logDict.get('timeTag'), predList=logDict.get('sentencePred')))
                
                
                # print
                currentWordPredPool = ''
                currentSentencePredPool = ''
                currentWordPredPoolDictList = []
                currentSentencePredPoolDictList = []
                for currentWordPred in currentWordPredListDictList:
                    currentWordPredPool = currentWordPredPool + str(currentWordPred['round']) +': '+ '||'.join(currentWordPred['prediction']) + '; '
                    tempDict = {
                        'round': currentWordPred['round'],
                        'prediction': currentWordPred['prediction']
                    }
                    currentWordPredPoolDictList.append(tempDict)
                for currentSentencePred in currentSentencePredListDictList:
                    currentSentencePredPool = currentSentencePredPool + str(currentSentencePred['round']) + ': ' + '||'.join(currentSentencePred['prediction'])+ '; '
                    tempDict = {
                        'round': currentSentencePred['round'],
                        'prediction': currentSentencePred['prediction']
                    }
                    currentSentencePredPoolDictList.append(tempDict)
                print('Select a sentence prediction: '+currentSentence)
                print('   current word prediction: '+'|'.join(logDict.get('wordPred')))
                print('   current sentence prediction: '+'|'.join(logDict.get('sentencePred')))
                print('      current word prediction pool: ' + currentWordPredPool)
                print('      current sentence prediction pool: ' + currentSentencePredPool)
                print('         current sentence: '+currentSentence)
                currentWordPredListDictList = []
                currentSentencePredListDictList = []
                currentWordPredRoundIndex = 1
                currentSentencePredRoundIndex = 1
                currentWordPredFistShowInRound = {}
                currentSentencePredFistIrrationalAction = {}


            if boolFinishAWord == True and boolFinishASentence == True:
                # A sentence is finished
                # Set wordPred and sentencePred to []
                currentWordPredListDictList = []
                currentSentencePredListDictList = []
                currentWordPredRoundIndex = 0
                currentSentencePredRoundIndex = 0
                sentenceLengthInWord = lastSentence.count(' ') + 1
                sentenceLengthInChar = len(lastSentence)
                print('A sentence is finished, currentSentence: '+lastSentence+'*')
            
            lastSentence = currentSentence
            
            """ Form a sentence above """

            """ Calculate interruption time below """
            # Assume interruption does not happen in irrational and erronous actions
            if lastLogDict:
                timeDifference = (logDict['timeTag'] - lastLogDict['timeTag']).total_seconds()
                if timeDifference > T_interrupt_threshold:
                    T_interrupt += timeDifference
            """ Calculate interruption time above """

            lastLogDict = logDict

        print('KS_all = '+str(KS_current))
        print('T_all = '+str(T_all))
        print('KS_error_correction = '+str(KS_error_correction))
        print('T_error_correction = '+str(T_error_correction))
        print('KS_irra_extra = '+str(KS_irra_extra))
        print('T_irra_extra = '+str(T_irra_extra))
        print('T_interrupt = '+str(T_interrupt))
        return KS_current, sentenceLengthInWord, sentenceLengthInChar, T_all, KS_error_correction, T_error_correction, KS_irra_extra, T_irra_extra, T_interrupt
        