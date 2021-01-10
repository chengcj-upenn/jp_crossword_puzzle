import frontend as fe
import importer
import importlib
importlib.reload(fe)
importlib.reload(importer)
import re
import random


# Determine a random word from dictionary
def gen_random_word(my_dict,length,regexp):
    
    horizontal = random.randint(0,1)
    row = random.randint(0,length-1)
    col = random.randint(0,length-1)
    words = my_dict.get_words(regexp)
    value = words[random.randint(0,len(words)-1)] 
    
    return [horizontal,row,col,value[0],value[1]]

# Check if the given work is ok to place in the matrix
def is_word_ok(word,words_matrix,placed_matrix):
    
    horizontal, row, col, value, clue = word[0],word[1],word[2],word[3],word[4]
    
    # Check if the row and column is not out of bounds
    if row < 0 or col < 0:
        return False
    
    if horizontal==0:
        if row+len(word[3])>len(words_matrix)-1:
            return False;
    else:
        if col+len(word[3])>len(words_matrix)-1:
            return False;

    # Check if there is no overlapping or adjacent word
    for i in range(0,len(word[3])):
        
        if horizontal==0:
#            print(row+i,col)
#            print(words_matrix[row+i][col], row, col)
            if col!=0 and col!=len(words_matrix)-1:
                if words_matrix[row+i][col+1] != None or words_matrix[row+i][col-1] != None:
                    if words_matrix[row+i][col] == None:
                        return False
            elif col==0:
                if words_matrix[row+i][col+1] != None:
                    if words_matrix[row+i][col] == None:
                        return False
            else:
                if words_matrix[row+i][col-1] != None:
                    if words_matrix[row+i][col] == None:
                        return False 
                        
            if placed_matrix[row+i][col] == "1":
                return False
            
        else:

            if 0 < row < len(words_matrix)-1:
                if words_matrix[row+1][col+i] != None or words_matrix[row-1][col+i] != None:
                    if words_matrix[row][col+i] == None:
                        return False
            elif row==0:
                if words_matrix[row+1][col+i] != None:
                    if words_matrix[row][col+i] == None:
                        return False
            else:
                if words_matrix[row-1][col+i] != None:
                    if words_matrix[row][col+i] == None:
                        return False 
                
            if placed_matrix[row][col+i] == "1":               
                return False
            

    # Check if the location adjacent to head and tail of the word is empty
    if horizontal==0:
        if row!=0:
            if words_matrix[row-1][col] != None:
                return False
        if row+len(value)<len(words_matrix):
            if words_matrix[row+1][col] != None:
                return False
    else:
        if col!=0:
            if words_matrix[row][col-1] != None:
                return False
        if col+len(value)<len(words_matrix):
            if words_matrix[row][col+1] != None:
                return False 
    return True

# Initialize the matrix
def init_words_matrix(length):
    
    words_matrix = [ [None]*length for i in range(length)]
    placed_matrix = [ [None]*length for i in range(length)]
    horizontal_words = []
    vertical_words = []
    
    return words_matrix,placed_matrix,horizontal_words,vertical_words

# Add word to the matrix
def add_word_to_matrix(word,words_matrix,placed_matrix,horizontal_words,vertical_words):
    
    print("Adding...")
    print(word)
    
    horizontal, row, col, value, clue = word[0],word[1],word[2],word[3], word[4]
    
    placed_matrix[row][col] = "1";

    for i in range(len(value)):
        if horizontal==0:
            words_matrix[row+i][col] = value[i]
            
        else:
            words_matrix[row][col+i] = value[i]
    
    if horizontal==0:        
        vertical_words.append([row, col, value, clue])
    else:
        horizontal_words.append([row, col, value, clue])

# Initialize and generate word for the matrix
def generate_words_matrix(length):
    
    # import dictionary
    my_importer = importer.Importer('./dictionary_files/vocab.json')
    my_dict = my_importer.export_searchable_dict()
    
    
    # initial matrix of length 8
    words_matrix,placed_matrix,horizontal_words,vertical_words = init_words_matrix(length)
    count = 0
    print("Step1")
    while True:
        word = gen_random_word(my_dict,length,'.')
        if is_word_ok(word,words_matrix,placed_matrix):
            add_word_to_matrix(word,words_matrix,placed_matrix,horizontal_words,vertical_words)
            count += 1
            break
 
    while True:
        random_index = random.randint(0,len(word[3])-1)
        iter = 0;
        while True:
            if iter>5: break
            iter += 1
            if word[0] == 0:
                regexp = '.*' + word[3][random_index] + '.*'
                new_word = gen_random_word(my_dict,length,regexp)
                new_word[0] = 1
                new_word[1] = random_index
                new_word[2] = word[2] - new_word[3].index(word[3][random_index])
            else:
                regexp = '.*' + word[3][random_index] + '.*'
                new_word = gen_random_word(my_dict,length,regexp)
                new_word[0] = 0
                new_word[1] = word[1] - new_word[3].index(word[3][random_index])
                new_word[2] = random_index

            if is_word_ok(new_word,words_matrix,placed_matrix):
                add_word_to_matrix(new_word,words_matrix,placed_matrix,horizontal_words,vertical_words)
                count += 1
                break   

        word = new_word
        if count==10: break
    
        
    return words_matrix,horizontal_words,vertical_words


#words_matrix,horizontal_words,vertical_words = generate_words_matrix(8)
#print(horizontal_words)        