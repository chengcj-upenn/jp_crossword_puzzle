import frontend as fe
import importer
import importlib
importlib.reload(fe)
importlib.reload(importer)
import re
import random


# Determine a random word from dictionary
def gen_random_word(my_dict,length,regexp):
    
    # randomly select the alignment
    horizontal = random.randint(0,1)
    # randomly select a row,column for the word to place in the crossword
    row = random.randint(0,length-1)
    col = random.randint(0,length-1)
    # get the words from the dictionary matching the regexp and randomly return one word out of them
    words = my_dict.get_words(regexp)
    value = words[random.randint(0,len(words)-1)] 
    
    # return the word
    return [horizontal,row,col,value[0],value[1]]

# Check if the given work is ok to place in the matrix
def is_word_ok(word,words_matrix,placed_matrix):
    
    horizontal, row, col, value, clue = word[0],word[1],word[2],word[3],word[4]
    
    # Check if the row and column is not out of bounds
    # - check if the row or column is not less than 0
    if row < 0 or col < 0:
        return False
    # - if the alignment is vertical, check if row will not become out of bound
    if horizontal==0:
        if row+len(word[3])>len(words_matrix)-1:
            return False;
    # - if the alignment is horizontal, check if the column will not become out of bound
    else:
        if col+len(word[3])>len(words_matrix)-1:
            return False;

    # Check if there is no overlapping or adjacent word
    # - Loop through each letter in the Japanese word
    for i in range(0,len(word[3])):
        # check that there are no words in the adjacent space apart from vertical crossing words
        # - check when word is vertically aligned
        if horizontal==0:

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
        # - check when word is horizontal aligned   
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
    # - check when word is vertically aligned
    if horizontal==0:
        if row!=0:
            if words_matrix[row-1][col] != None:
                return False
        if row+len(value)<len(words_matrix):
            if words_matrix[row+1][col] != None:
                return False
    # - check when word is horizontally aligned
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
    
    # words matrix to store the each letter
    words_matrix = [ [None]*length for i in range(length)]
    # placed matrix to indicate the position of the first letter of each word
    placed_matrix = [ [None]*length for i in range(length)]
    # list of words horizontally placed
    horizontal_words = []
    # list of words veritically placed
    vertical_words = []
    
    return words_matrix,placed_matrix,horizontal_words,vertical_words


# Add given word to the crossword matrix
def add_word_to_matrix(word,words_matrix,placed_matrix,horizontal_words,vertical_words):
    
    #print("Adding...")
    #print(word)
    
    horizontal, row, col, value, clue = word[0],word[1],word[2],word[3], word[4]
    
    # set the location of the fist letter of the word as 1 in placed matrix
    placed_matrix[row][col] = "1";

    # loop through each letter and place them at appropriate location in crossword matrix
    for i in range(len(value)):
        if horizontal==0:
            words_matrix[row+i][col] = value[i]
        else:
            words_matrix[row][col+i] = value[i]
    
    # append the word to either horizontal or vertical word list
    if horizontal==0:        
        vertical_words.append([row, col, value, clue])
    else:
        horizontal_words.append([row, col, value, clue])

        
# This is the main method to initialize and generate words for the crossword matrix
def generate_words_matrix(length):
    
    # import dictionary
    my_importer = importer.Importer('./dictionary_files/vocab.json')
    my_dict = my_importer.export_searchable_dict()
    
    
    # initiate the crossword matrix of the given length (row = column)
    words_matrix,placed_matrix,horizontal_words,vertical_words = init_words_matrix(length)
    
    # Algo to determine the words for crossword and place them on the crossword matrix
    # - count to track the number of words added to the crossworld matrix
    count = 0
    
    while True:
        # - Start with a random word - with random position on the crossword matrix
        word = gen_random_word(my_dict,length,'.')
        # - Check if the identified word is ok to place on the crossword matrix 
        if is_word_ok(word,words_matrix,placed_matrix):
            # - if yes, add the world to the matrix and break out of loop
            add_word_to_matrix(word,words_matrix,placed_matrix,horizontal_words,vertical_words)
            count += 1
            break
 
    while True:
        # - Randomly pick an index on the word added to the matrix
        random_index = random.randint(0,len(word[3])-1)
        
        iter = 0;
        while True:
            # - if the alignment of the last added word was vertical, next word alignment would be horizontal
            if word[0] == 0:
                # Randomly select a word which contains the letter at the randomly selected index of placed word
                regexp = '.*' + word[3][random_index] + '.*'
                new_word = gen_random_word(my_dict,length,regexp)
                # - set the alignment of the new word as horizontal and assign the location on crossword matrix
                new_word[0] = 1
                new_word[1] = random_index
                new_word[2] = word[2] - new_word[3].index(word[3][random_index])
            # - if the alignment of the last added word was horizontal
            else:
                regexp = '.*' + word[3][random_index] + '.*'
                new_word = gen_random_word(my_dict,length,regexp)
                # - set the alignment of the new word as vertical
                new_word[0] = 0
                new_word[1] = word[1] - new_word[3].index(word[3][random_index])
                new_word[2] = random_index

            # - check if its ok to place the word in the crossword matrix
            if is_word_ok(new_word,words_matrix,placed_matrix):
                # - if yes and increment the count
                add_word_to_matrix(new_word,words_matrix,placed_matrix,horizontal_words,vertical_words)
                count += 1
                break   

            if iter>5: break
            iter += 1
        # continue the loop with the new word set as the base word now    
        word = new_word
        # if numbers of words added is 10, then break the outer loop
        if count==10: break
    
    # return the words_matrix, horizontal_words, vertical_words    
    return words_matrix,horizontal_words,vertical_words


#words_matrix,horizontal_words,vertical_words = generate_words_matrix(8)
#print(horizontal_words)        