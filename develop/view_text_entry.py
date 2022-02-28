from os import system

class View_text_edit:
    
    BOOL_ENTRY_BY_KEYWORDS = False

    def __init__(self):
        self.previousEntry = ''
        self.entry = ''
        self.prediction = ''

    def edit_text_letter(self, caption):
        if caption == "<-":
            self.previousEntry = self.entry
            self.entry = self.entry[:-1]
        elif caption == "Space":
            self.entry = self.entry + ' '
        elif caption == "Tab":
            self.entry = self.entry + '    '
        elif caption == "Speak":
            system(f'say {self.entry}')
        elif caption == "Clear All":
            self.entry = ''
            self.previousEntry = ''
        else:
            """ Caption is a letter """
            if self.entry == "":
                """ Blank textbox """
                self.entry = self.entry + caption.upper()
                    # self.entry = self.entry + caption[0].upper() + caption[1:]
            else:
                """ Textbox has content """
                if caption == "," or caption == "." or caption == "?" or caption == "!":
                    if self.entry[-1] == " ":
                        self.entry = self.entry[0:-1] + caption
                    else:
                        self.entry = self.entry + caption
                else:
                    self.entry = self.entry + caption

        return self.entry


    def edit_text_word(self, caption):
        """ Caption is a word prediction """
        if caption[0] == "'":
            self.entry = self.entry + caption
        else:
            if self.entry == "":
                """ Blank textbox """
                self.entry = self.entry + caption[0].upper() + caption[1:]
            else:
                """ Textbox has content """
                if self.entry[-1] == " ":
                    """ A word is finished """
                    self.entry = self.entry + caption
                else:
                    """ A word is not finished """
                    wordList = self.entry.split()
                    lastWord = wordList[-1]
                    indexOfLastWord = self.entry.rfind(lastWord) 
                    self.entry = self.entry[0:indexOfLastWord] + caption
        
        return self.entry

    def edit_text_sentence(self, caption):
        """ Caption is a sentence prediction """
        if self.BOOL_ENTRY_BY_KEYWORDS:
            self.entry = caption
            self.entry = self.entry[0].upper() + self.entry[1:]
        else:
            if self.entry == "":
                """ Blank textbox """
                self.entry = self.entry + caption[0].upper() + caption[1:]
            elif " " not in self.entry:
                self.entry = caption[0].upper() + caption[1:]
            else:
                """ Textbox has content """
                # entryWordList = self.entry.split()
                captionWordList = caption.split()
                captionFirstWord = captionWordList[0]
                indexOfFirstWordOfCaptionInEntry = self.entry.lower().rfind(captionFirstWord.lower())
                self.entry = self.entry[0:indexOfFirstWordOfCaptionInEntry] + caption
                self.entry = self.entry[0].upper() + self.entry[1:] + " "

        return self.entry