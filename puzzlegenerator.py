import importer
import re
import random

class PuzzleGenerator:
    def __init__(self, rows, cols):
        self.rows=rows
        self.cols=cols
        
        my_importer = importer.Importer('./dictionary_files/vocab.json')
        self.my_dict = my_importer.export_searchable_dict()
        
        self.status = [['empty']*cols for y in range(rows) ]
        self.words_matrix = [[None]*cols for y in range(rows) ]
        self.horizontal_words =[]
        self.vertical_words=[]
    
    def generate_puzzle(self):
        # reset puzzle
        self.reset_puzzle()
        
        # find a starting point of a horizontal word
        switch = True # starts with horizontal
        for i in range(20):
            orientation = 'horizontal' if switch else 'vertical'            
            
            start_row, start_col = self.select_start(orientation)
            print("start_row, start_col = ", start_row, start_col)
            regex = self.get_regex(start_row, start_col, orientation)
            if regex == 'false': continue # not possible to find word
            word, clue = self.get_one_word(regex) 
            if word == 'false': continue # not possible to find word
            self.update_puzzle_status(start_row, start_col, word, clue, orientation) #update stuff
            switch = not switch
        print(self.status)
        return self.horizontal_words, self.vertical_words, self.words_matrix
    
    def get_one_word(self, regex):
        """
        returns one random word that fits the puzzle
        the word can be shorter
        """
        words = self.my_dict.get_words(regex)
        if (len(words) == 0): return 'false', 'false'
        word_info = random.choice(words)
        jp_word, clue = word_info[0], word_info[1]
        return jp_word, clue
    
    def get_regex(self, start_row, start_col, orientation='horizontal'):
        regex = ''
        if orientation == 'horizontal':
            for col in range( start_col, self.cols):
                if self.status[start_row][col] == 'empty':
                    regex += '.'
                elif self.status[start_row][col] == 'v':
                    regex += self.words_matrix[start_row][col]
                elif self.status[start_row][col] == 'illegal':
                    break                    
        elif orientation == 'vertical':
            for row in range( start_row, self.rows):
                if self.status[row][start_col] == 'empty':
                    regex += '.'
                elif self.status[row][start_col] == 'h':
                    regex += self.words_matrix[row][start_col]
                elif self.status[row][start_col] == 'illegal':
                    break

        return self.replace_last_part_of_regex(regex) # allows matching for a shorter word
    
    def replace_last_part_of_regex(self, regex):
        count_dots = 0
        result = ''
        i = len(regex)-1
        
        for i in range(len(regex)-1, -1, -1):
            if regex[i] == '.':
                count_dots += 1
            else: break
        
        
        result = '^' + regex[0:i+1] + '(.){0,' + str(count_dots) + '}$'
        
        if (len(regex.replace('.',''))==0): 
            if (2>count_dots): 
                result = 'false'
            else:
                result = '^(.){2,' + str(count_dots) + '}$'
        print('regex result = ', result)
        return result
    
    def update_puzzle_status(self, row, col, word, clue, orientation='horizontal'):
        """
        updates the intermediate status of the puzzle during puzzle generation
        """
        print("col, len(word)", col, word)
        if orientation == 'horizontal':
            self.horizontal_words.append([row, col, word, clue])
            for i in range(col, col+len(word)):
                self.status[row][i] = 'h'
                self.words_matrix[row][i] = word[i-col]
            # add illegal spots on status
            if col > 0:
                self.status[row][col-1] = 'illegal'
            if col + len(word) - 1 != self.cols - 1 : # not touching the right edge
                self.status[row][col + len(word)] = 'illegal'
        elif orientation == 'vertical':
            self.vertical_words.append([row, col, word, clue])
            for i in range(row, row+len(word)):
                self.status[i][col] = 'v'
                self.words_matrix[i][col] = word[i-row]
            # add illegal spots on status
            if row > 0:
                self.status[row-1][col] = 'illegal'
            if row + len(word) - 1 != self.rows - 1 : # not touching the bottom
                self.status[row+len(word)][col] = 'illegal'
        
        
    def select_start(self, orientation='horizontal'):
        """
        randomly find a starting position for the word
        """
        possible_row_col = []
        print(self.status)
        
        if orientation == 'horizontal':
        
            for row in range(self.rows): 
                for col in range(self.cols - 1): #at least word of length 2
                    if self.status[row][col] in ['empty','v']:
                        possible_row_col.append((row,col))
            start_row, start_col = random.choice(possible_row_col)
        elif orientation == 'vertical':
            for row in range(self.rows-1): #at least word of length 2
                for col in range(self.cols): 
                    if self.status[row][col] in ['empty','h']:
                        possible_row_col.append((row,col))
            start_row, start_col = random.choice(possible_row_col)
            
        return start_row, start_col
    
    def reset_puzzle(self):
        self.status = [['empty']*self.cols for y in range(self.rows) ]
        self.words_matrix = [[None]*self.cols for y in range(self.rows) ]
        self.horizontal_words =[]
        self.vertical_words=[]
