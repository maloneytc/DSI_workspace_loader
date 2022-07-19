from pathlib import Path
import sys
import PySimpleGUI as sg
import random
import string
import pandas as pd
import subprocess as sp
import main as dwl

import pdb

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

def main(file_path):

    dsi_studio_path = dwl.get_dsi_path()
    #df = pd.read_csv(file_path, names=['Path'])
    df = pd.read_csv(file_path)


    # ------ Make the Table Data ------
    # # TODO: Change to just take a list of directories and construct the Dataframe from that
    data = df.to_numpy().tolist()
    headings = list(df.columns)
    # data = make_table(num_rows=15, num_cols=6)
    #headings = [str(data[0][x])+'     ..' for x in range(len(data[0]))]

    # ------ Window Layout ------
    layout = [[sg.Table(values=data, headings=headings, max_col_width=55,
                        # background_color='light blue',
                        auto_size_columns=True,
                        display_row_numbers=True,
                        justification='right',
                        num_rows=df.shape[0],
                        alternating_row_color='green',
                        key='-TABLE-',
                        row_height=35,
                        tooltip='This is a table')],
              [sg.Button('Read'), sg.Button('Double'), sg.Button('Open'), sg.Button('Approve')],
              [sg.Text('Read = read which rows are selected')],
              [sg.Text('Double = double the amount of data in the table')],
              [sg.Text('Change Colors = Changes the colors of rows 8 and 9')]]

    #XXX Add export button

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
        elif event == 'Open':
            selected_values = values.get('-TABLE-')
            selected_value = selected_values[0]
            print(selected_value)
            print(data[selected_value])
            workspace_path = Path(data[selected_value][1])
            if workspace_path.exists():
                dwl.view_workspace(workspace_path, dsi_studio_path)
        elif event == 'Approve':
            selected_values = values.get('-TABLE-')
            selected_value = selected_values[0]
            data[selected_value][3] = 1
            window['-TABLE-'].update(values=data)
        # elif event == 'Change Colors':
        #     window['-TABLE-'].update(row_colors=((8, 'white', 'red'), (9, 'green')))

    window.close()

if __name__ == "__main__":
    file_path = Path(sys.argv[1])
    main(file_path)
