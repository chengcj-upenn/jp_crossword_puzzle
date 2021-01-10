import frontend as fe
import importer
import importlib
importlib.reload(fe)
importlib.reload(importer)
import PySimpleGUI as sg
import re
import random

"""
    Prototype frontend application that 1) takes japanese user input 2) displays puzzle 3) shows puzzle answers
"""
# import dictionary
my_importer = importer.Importer('./dictionary_files/vocab.json')
my_dict = my_importer.export_searchable_dict()

# define the word
def gen_random_word(my_dict,length,regexp):
    
    horizontal = random.randint(0,1)
    row = random.randint(0,length-1)
    col = random.randint(0,length-1)
    words = my_dict.get_words(regexp)
    value = words[random.randint(0,len(words)-1)] 
    print(value[0])
    return [horizontal,row,col,value[0],value[1]]
    
def is_word_ok(word,words_matrix,placed_matrix):
    
    horizontal, row, col, value, clue = word[0],word[1],word[2],word[3],word[4]
    
    'check if the word is within bounds'
    if horizontal==0:
        if row+len(word)>len(words_matrix):
            return False;
    else:
        if col+len(word)>len(words_matrix):
            return False;
    
    'check if there is no overlapping word in the matrix'
    for i in range(0,len(words_matrix)):
        if horizontal==0:
            if words_matrix[row+i][col] != "None" or placed_matrix[row+i][col] == "1":
                return False
        else:
            if words_matrix[row][col+i] != "None" or placed_matrix[row][col+i] == "1":
                return False
            
    'check if there is no adjacement location is empty'
    if horizontal==0:
        if row!=0:
            if words_matrix[row-1][col] != "None":
                return False
        if row+len(value)<len(words_matrix):
            if words_matrix[row+1][col] != "None":
                return False
    else:
        if col!=0:
            if words_matrix[row][col-1] != "None":
                return False
        if col+len(value)<len(words_matrix):
            if words_matrix[row][col+1] != "None":
                return False    
        
    
def init_words_matrix(length):
    
    words_matrix = [ [None]*length for i in range(length)]
    placed_matrix = [ [None]*length for i in range(length)]
    
    return words_matrix,placed_matrix

def add_word_to_matrix(word,words_matrix,placed_matrix):
    
    horizontal, row, col, value, clue = word[0],word[1],word[2],word[3], word[4]
    
    placed_matrix[row,col] = "1";

    for i in range(len(value)):
        if horizontal==0:
            words_matrix[row+i,col] = value[i]
        else:
            words_matrix[row,col+i] = value[i]


def generate_words_matrix(length):
    
    # import dictionary
    my_importer = importer.Importer('./dictionary_files/vocab.json')
    my_dict = my_importer.export_searchable_dict()
    
    # initial matrix of length 8
    words_matrix,placed_matrix = init_words_matrix(8)
    count = 0
    print("Step1")
    while True:
        word = gen_random_word(my_dict,length,'.')
        if is_word_ok(word,words_matrix,placed_matrix):
            add_word_to_matrix(word,words_matrix,placed_matrix)
            print("Adding word" + word)
#            my_dict.remove([word[3],word[4]])
            count += 1
            break
    print("Step2")
    while True:
        random_index = random.randint(0,len(word)-1)
        while True:

            if word[0] == 0:
                new_word = gen_random_word(my_dict,length,'.*' + word[3][random_index] + '.*')
                new_word[0] = 1
                new_word[1] = random_index
                new_word[2] = word[2] - new_word[3].index(word[3][random_index])
            else:
                word = gen_random_word(my_dict,length,'.*' + word[3][random_index] + '.*')
                new_word[0] = 0
                new_word[1] = word[1] - new_word[3].index(word[3][random_index])
                new_word[2] = random_index

            if is_word_ok(word,words_matrix,placed_matrix):
                add_word_to_matrix(word,words_matrix,placed_matrix)
                print("Adding word" + word)
 #               words_matrix.remove([word[3],word[4]])
                count += 1
                break   

        word = new_word
        if count==10: break
    
        
    return words_matrix


generate_words_matrix(4)
        
    
    
    
#regex = '.'+chr(0x3044)
#list_of_words = my_dict.get_words(regex)
#print(gen_random_word(my_dict,5));

## make up some words to play with
#horizontal_words = [[0,0,chr(0x3042)+chr(0x3043), "clue1"], [4,4,chr(0x3044)+chr(0x3045), "clue2"]]
#vertical_words = [[0,0,chr(0x3042)+chr(0x3043), "clue1a"], [3,1,chr(0x3044)+chr(0x3045), "clue3"], [2,2,chr(0x3046), "clue4"], [6,7,chr(0x3046)+chr(0x3049), "clue5"]]
#words_matrix = [ [None]*8 for i in range(8)]
#
#for hori_word in horizontal_words:
#    start_row, start_col, word = hori_word[0], hori_word[1], hori_word[2]        
#    for i in range(len(word)):
#        words_matrix[start_row][start_col+i] = word[i]
#for vert_word in vertical_words:
#    start_row, start_col, word = vert_word[0], vert_word[1], vert_word[2]        
#    for i in range(len(word)):
#        words_matrix[start_row+i][start_col] = word[i]
#print(words_matrix)
