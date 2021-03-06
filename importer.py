"""
importer does the following:
- reads file and store as dictionary
- filters out words, leaving only hiragana and length no more than 8 chars
- returns a searchable dictionary
"""

import json
import re

class Importer:
    def __init__(self, path):
        #with open('./dictionary_files/vocab.json') as f:
        with open(path, encoding='utf-8') as f:
            self.data = json.load(f)
    
    def get_cleaned_dictionary(self):
        hiragana = set([chr(i) for i in range(0x3041, 0x3097)])
        my_japanese_dict = {}
        counter = 10
        for entry in self.data:
            japanese_word = entry['Kana']
            
            if (set(japanese_word).issubset(hiragana) and
                len(japanese_word) < 9 and
                len(japanese_word) > 1  
               ):

                clue = entry['Meaning']
                my_japanese_dict[japanese_word] = clue
        return my_japanese_dict
    
    def export_searchable_dict(self):
        mySearchableDict = SearchableDict(self.get_cleaned_dictionary())
        return mySearchableDict

class SearchableDict(dict):

    def __init__(self, japanese_dict):
        self.myDict = japanese_dict
        
    def get_matching(self, event):
        return (self[key] for key in self if re.match(key, event))    

    def get_words(self, regular_exp):
        result = []
        for key in self.myDict.keys():
            if re.match(regular_exp, key):
                result.append([key, self.myDict[key]])
        return result
