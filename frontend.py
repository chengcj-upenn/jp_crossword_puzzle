import PySimpleGUI as sg

class GameGui:
    def __init__(self, 
                   box_size=15, 
                   title = 'Japanese Crossword Puzzle!', 
                   puzzle_size=500,
                   coor_sys_height=130
                  ):
        self.box_size = box_size
        sg.theme('SystemDefaultForReal') 
        
        layout = [
            [sg.Text(title), sg.Text('Press "Generate Puzzle" to start game', key='-Status-')],
            [sg.Graph((puzzle_size, puzzle_size), 
                      (0, coor_sys_height), 
                      (coor_sys_height, 0), 
                      key='-PuzzleBoard-',
                      change_submits=True, drag_submits=False), 
             sg.Text('\n                              '*24, key='-Clues-')
            ],
        ]        
        
        # Generate japanese character input buttons
        i = 0
        for row in range(4):
            input_buttons = []
            for col in range(22):
                # every button is associated with a single character for event detection
                input_buttons.append(sg.Button('{}'.format(chr(0x3041 + i))))
                i += 1
                if 0x3041 + i > 0x3096: break # remove unnecessary characters
            layout.append(input_buttons)        
        
        layout.append([sg.Button('Generate Puzzle'), sg.Button('Show Answer'), sg.Button('Exit')])
        
        self.window = sg.Window('Window Title', layout, finalize=True)
    
    def get_puzzle_interface(self):
        return self.window['-PuzzleBoard-']
    
    def monitor_events(self):
        return self.window.read()
    
    def get_selected_tile(self):
        mouse_coordinates = values['-PuzzleBoard-']
        arrayindexij = 0
        pass
    
    def display_puzzle(self, rows = 8, cols = 8, horizontal_words = [], vertical_words = [], show_answer=False):
        
        box_size = self.box_size
        puzzle_board = self.get_puzzle_interface()
        
        # build black background first
        for row in range(rows):
            for col in range(cols):
                self.render_rectangle(row, col, fill_color='black')   

        counter = 0
        
        # render white squares
        for hori_word in horizontal_words:            
            # unpack info:
            start_row, start_col, word_len, clue = hori_word[0], hori_word[1], len(hori_word[2]), hori_word[3]
            for i in range(start_col, start_col + word_len):
                self.render_rectangle(start_row, i, fill_color='white')                
                if show_answer: self.render_tile_char(start_row, i, hori_word[2][i-start_col],'blue')
        for vert_word in vertical_words:
            # unpack info:            
            start_row, start_col, word_len, clue = vert_word[0], vert_word[1], len(vert_word[2]), hori_word[3]      
            for i in range(start_row, start_row + word_len):
                self.render_rectangle(i, start_col, fill_color='white')
                if show_answer: self.render_tile_char(i, start_col, vert_word[2][i-start_row],'blue')
        
        # render tile lables for vertical and horizontal words
        self.render_tile_labels(horizontal_words, vertical_words)
        self.render_clues(horizontal_words, vertical_words)
        self.window['-Status-'].update("Generated Puzzle")
        
        if show_answer:
            self.window['-Status-'].update("Showing Answer")

    def render_rectangle(self, row, col, fill_color='black'):
        box_size = self.box_size
        puzzle_board = self.get_puzzle_interface()
        
        puzzle_board.draw_rectangle((col * box_size , row * box_size ), 
                                 ((col+1) * box_size , (row+1) * box_size ), 
                                 line_color='black',  fill_color=fill_color)
    
    def render_tile_char(self, row, col, tile_char, color='black'):
        box_size = self.box_size
        puzzle_board = self.get_puzzle_interface()
        
        self.render_rectangle(row, col, fill_color='white')
        letter_location = (col * box_size + box_size*.7,
                           row * box_size + box_size*.7)
        puzzle_board.draw_text(tile_char, letter_location, font='Courier 25', color=color)        
    
    def render_tile_label(self, row, col, tile_label):
        box_size = self.box_size
        puzzle_board = self.get_puzzle_interface()
        puzzle_board.draw_text(tile_label, (col * box_size + box_size*.2, row * box_size+ box_size*.2))
        
    def render_tile_labels(self, horizontal_words, vertical_words):
        box_size = self.box_size
        puzzle_board = self.get_puzzle_interface()

        counter = 0
        
        for hori_word in horizontal_words:
            
            # unpack info:
            start_row, start_col = hori_word[0], hori_word[1]
            self.render_tile_label(start_row, start_col, tile_label='h'+str(counter))
            counter += 1
        
        counter = 0
        for vert_word in vertical_words:
            # unpack info:            
            start_row, start_col = vert_word[0], vert_word[1]
            self.render_tile_label(start_row, start_col,tile_label='v'+str(counter))
            counter += 1

    def render_clues(self, horizontal_words, vertical_words):
        box_size = self.box_size
        puzzle_board = self.get_puzzle_interface()

        counter = 0
        clues = 'Clues:\n'
        for hori_word in horizontal_words:
            
            # unpack info:
            clue = hori_word[3]
            clues = clues + 'h'+str(counter) + ') ' + clue + '\n'
            counter += 1
        
        counter = 0
        for vert_word in vertical_words:
            # unpack info:            
            clue = vert_word[3]
            clues = clues + 'v'+str(counter) + ') ' + clue + '\n'
            counter += 1
        print(clues)

        self.window['-Clues-'].update(clues)