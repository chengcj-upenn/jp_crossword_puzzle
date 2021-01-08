import PySimpleGUI as sg

def generate_interface(title = 'Crossword Puzzle Using PySimpleGUI', 
                       puzzle_size=600,
                       input_panel_size=300,
                       graph_def_height=450                       
                      ):
    """
    generates the window which contains the app
    args: title, panel_size, manual_def_height    
    """
    layout = [
                [sg.Text(title), sg.Text('', key='-OUTPUT-')],
                [sg.Graph((puzzle_size, puzzle_size), # currently a square panel
                          (0, graph_def_height), # coordinate for lower left corner
                          (graph_def_height, 0), # coordinate for upper right corner
                          key='-Puzzle-', change_submits=True, drag_submits=False)],
                [sg.Graph((input_panel_size, input_panel_size), # currently a square panel
                          (0, graph_def_height+input_panel_size), # coordinate for lower left corner
                          (graph_def_height, 0), # coordinate for upper right corner
                          key='-InputPanel-', change_submits=True, drag_submits=False)],
                [sg.Button('Show'), sg.Button('Exit')]
            ]
    return layout
