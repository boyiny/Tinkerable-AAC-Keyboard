import time
from datetime import datetime
from pathlib import Path

class Model_Log_Data:
    def __init__(self) -> None:
        Path('./analysis/klm_bei_record/').mkdir(parents=True, exist_ok=True)
        Path('./analysis/text_entry_record/').mkdir(parents=True, exist_ok=True)
        Path('./analysis/prediction_setting/').mkdir(parents=True, exist_ok=True)   
        Path('./analysis/ui_setting/').mkdir(parents=True, exist_ok=True)
        # Path('./analysis/test/').mkdir(parents=True, exist_ok=True)
        timestr = time.strftime("%Y%m%d_%H%M%S")
        self.word_level_record_path = './analysis/text_entry_record/word_level_record_'+str(timestr)+'.txt'
        self.sentence_level_record_path = './analysis/text_entry_record/sentence_level_record_'+str(timestr)+'.txt'
        self.f_word = open(self.word_level_record_path, 'a+')
        self.f_sentence = open(self.sentence_level_record_path, 'a+')
        # print("trace analysis initialisation")
    
    
    def record_word_level_input(self, wordPredAlgo, sentencePredAlgo, sentenceEntryApproach, currentSen):
        currentTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        self.f_word = open(self.word_level_record_path, 'a')
        self.f_word.write(currentTime + ' | ' + wordPredAlgo + ' | ' + sentencePredAlgo + ' | ' + sentenceEntryApproach + ' >> '  + currentSen +'\n')
        self.f_word.close()
    
    def record_sentence_level_input(self, wordPredAlgo, sentencePredAlgo, sentenceEntryApproach, finishedSen):
        currentTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        self.f_sentence = open(self.sentence_level_record_path, 'a')
        self.f_sentence.write(currentTime + ' | ' + wordPredAlgo + ' | ' + sentencePredAlgo + ' | ' + sentenceEntryApproach + ' >> ' + finishedSen +'\n')
        self.f_sentence.close()

    def record_conversation_partner_input(self, partnerSen):
        currentTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        self.f_sentence = open(self.sentence_level_record_path, 'a')
        self.f_sentence.write('PARTNER: ' + currentTime + ' >> ' + partnerSen + '\n')
        self.f_sentence.close()