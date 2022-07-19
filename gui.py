# import PySimpleGUI as sg
# from pathlib import Path
#
# import subprocess as sp
#
# import pdb
#
# # def view_workspace(workspace_dir, dsi_studio_path):
# #     workspace_dir = Path(workspace_dir)
# #     assert workspace_dir.exists()
# #     source_dir = workspace_dir.joinpath('slices')
# #     source_file = list(source_dir.glob('*.nii*'))[0]
# #     query = [str(dsi_studio_path), '--action=vis', f'--source={str(source_file)}', '--stay_open=1', f'--cmd=load_workspace,{str(workspace_dir)}']
# #     print(query)
# #     res = sp.check_output(query)
# #
# # if Path('/Applications/dsi_studio.app/Contents/MacOS/dsi_studio').exists():
# #     dsi_studio_path = Path('/Applications/dsi_studio.app/Contents/MacOS/dsi_studio')
# # else:
# #     dsi_studio_path = None
# #
# # sg.theme('Dark Blue 3')  # please make your windows colorful
# #
# # layout = [[sg.Text('Load info')],
# #       [sg.Text('DSI_Studio executable', size=(15, 1)), sg.InputText(), sg.FileBrowse(initial_folder=str(dsi_studio_path))]
# #       [sg.Text('Workspace list', size=(15, 1)), sg.InputText(), sg.FileBrowse()],
# #       [sg.Submit(), sg.Cancel()]]
# #
# # window = sg.Window('Select DSI Studio workspace list', layout)
# #
# # event, values = window.read()
# # window.close()
# #
# # pdb.set_trace()
# # file_path = Path(values[0])      # get the data from the values dictionary
# # print(file_path)


import PySimpleGUI as sg
import random
import string

"""
    Basic use of the Table Element
"""

sg.theme('Dark Blue 3')

# ------ Some functions to help generate data for the table ------
def word():
    return ''.join(random.choice(string.ascii_lowercase) for i in range(10))
def number(max_val=1000):
    return random.randint(0, max_val)

def make_table(num_rows, num_cols):
    data = [[j for j in range(num_cols)] for i in range(num_rows)]
    data[0] = [word() for __ in range(num_cols)]
    for i in range(1, num_rows):
        data[i] = [word(), *[number() for i in range(num_cols - 1)]]
    return data

# ------ Make the Table Data ------
data = make_table(num_rows=15, num_cols=6)
headings = [str(data[0][x])+'     ..' for x in range(len(data[0]))]

# ------ Window Layout ------
layout = [[sg.Table(values=data[1:][:], headings=headings, max_col_width=25,
                    # background_color='light blue',
                    auto_size_columns=True,
                    display_row_numbers=True,
                    justification='right',
                    num_rows=20,
                    alternating_row_color='lightyellow',
                    key='-TABLE-',
                    row_height=35,
                    tooltip='This is a table')],
          [sg.Button('Read'), sg.Button('Double'), sg.Button('Change Colors')],
          [sg.Text('Read = read which rows are selected')],
          [sg.Text('Double = double the amount of data in the table')],
          [sg.Text('Change Colors = Changes the colors of rows 8 and 9')]]

# ------ Create Window ------
window = sg.Window('The Table Element', layout,
                   # font='Helvetica 25',
                   )

# ------ Event Loop ------
while True:
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED:
        break
    if event == 'Double':
        for i in range(len(data)):
            data.append(data[i])
        window['-TABLE-'].update(values=data)
    elif event == 'Change Colors':
        window['-TABLE-'].update(row_colors=((8, 'white', 'red'), (9, 'green')))

window.close()
