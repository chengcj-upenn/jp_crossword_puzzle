import frontend as fe
import importer
import importlib
import puzzlegenerator as pg
importlib.reload(pg)
importlib.reload(fe)
importlib.reload(importer)
import PySimpleGUI as sg
import re

"""
    application that 1) takes japanese user input 2) displays puzzle 3) shows puzzle answers
"""
# initialize Puzzle Generator
my_puzzle_gen = pg.PuzzleGenerator(8,8)
# initialize GUI
my_game_window = fe.GameGui()

# Event Loop
while True:             
    event, values = my_game_window.monitor_events()
    mouse_coordinates = values['-PuzzleBoard-']
    #print(event, values)
    
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
        
    elif event == 'Generate Puzzle':        
        #words_matrix,horizontal_words,vertical_words = pg.generate_words_matrix(8)
        horizontal_words, vertical_words, words_matrix = my_puzzle_gen.generate_puzzle()
        my_game_window.display_puzzle(horizontal_words=horizontal_words, vertical_words=vertical_words)
    
    elif event == 'Show Answer':        
        my_game_window.display_puzzle(horizontal_words=horizontal_words, vertical_words=vertical_words, show_answer=True)

    elif event == '-PuzzleBoard-': # selecting a tile
        if mouse_coordinates == (None, None):
            continue        
        box_x = min(mouse_coordinates[0]//my_game_window.box_size,7)
        box_y = min(mouse_coordinates[1]//my_game_window.box_size,7)
        if not (words_matrix[box_y][box_x]): continue #ignore invalid selections
        my_game_window.clean_previous_selected_tiles(words_matrix)
        my_game_window.render_selected_tile(box_y, box_x)
        #print("selected box (x, y) =", box_x, box_y)        
    
    elif event in [chr(i) for i in range(0x3041, 0x3097)]: # check if input a japanese character
        color = 'black'
        # will only update tile if it is a white tile
        if not (words_matrix[box_y][box_x]): continue
        elif event != words_matrix[box_y][box_x]:
            color = 'red' # if the input is incorrect, show as red
        my_game_window.render_tile_char(box_y, box_x, event, color)
        my_game_window.render_tile_labels(horizontal_words, vertical_words)
        
my_game_window.window.close()