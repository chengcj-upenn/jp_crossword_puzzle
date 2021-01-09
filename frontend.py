import PySimpleGUI as sg

class GameGui:
    def __init__(self, 
                   box_size=20, 
                   title = 'Crossword Puzzle Using PySimpleGUI', 
                   puzzle_size=500,
                   coor_sys_height=150
                  ):
        self.box_size = box_size
        sg.theme('SystemDefaultForReal') 
        
        layout = [
            [sg.Text(title), sg.Text('Press Generate Puzzle to start game', key='-Status-')],
            [sg.Graph((puzzle_size, puzzle_size), 
                      (0, coor_sys_height), 
                      (coor_sys_height, 0), 
                      key='-PuzzleBoard-',
                      change_submits=True, drag_submits=False)],
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
    
    def display_puzzle(self, rows = 8, cols = 8, horizontal_words = [], vertical_words = []):
        
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
            start_row, start_col, word_len = hori_word[0], hori_word[1], len(hori_word[2])            
            for i in range(start_col, start_col + word_len):
                self.render_rectangle(start_row, i, fill_color='white')
        for vert_word in vertical_words:
            # unpack info:            
            start_row, start_col, word_len = vert_word[0], vert_word[1], len(vert_word[2])            
            for i in range(start_row, start_row + word_len):
                self.render_rectangle(i, start_col, fill_color='white')
                
        # render tile lables for vertical and horizontal words
        self.render_tile_labels(horizontal_words, vertical_words)

    def render_rectangle(self, row, col, fill_color='black', tile_label=''):
        box_size = self.box_size
        puzzle_board = self.get_puzzle_interface()
        
        puzzle_board.draw_rectangle((col * box_size + 5, row * box_size + 3), 
                                 ((col+1) * box_size + 5, (row+1) * box_size + 3), 
                                 line_color='black',  fill_color=fill_color)
        puzzle_board.draw_text(tile_label, (col * box_size + 10, row * box_size + 8))
    
    def render_tile_char(self, row, col, tile_char):
        box_size = self.box_size
        puzzle_board = self.get_puzzle_interface()
        
        self.render_rectangle(row, col, fill_color='white')
        letter_location = (col * box_size + box_size*.8,
                           row * box_size + box_size*.8)
        puzzle_board.draw_text(tile_char, letter_location, font='Courier 25')
        
    
    def render_tile_label(self, row, col, tile_label):
        box_size = self.box_size
        puzzle_board = self.get_puzzle_interface()
        puzzle_board.draw_text(tile_label, (col * box_size + box_size*.4, row * box_size+ box_size*.4))
        
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
