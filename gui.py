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

sg.theme('BlueMono')


# ------ Some functions to help generate data for the table ------
def dataframe_to_lists(dataframe):
    return dataframe.to_numpy().tolist()

def main(file_path):
    file_path = Path(file_path)
    dsi_studio_path = dwl.get_dsi_path()
    #df = pd.read_csv(file_path, names=['Path'])
    df = pd.read_csv(file_path)

    # ------ Make the Table Data ------
    # # TODO: Change to just take a list of directories and construct the Dataframe from that
    data = dataframe_to_lists(df)
    headings = list(df.columns)
    tracks = [this.replace(' Approved', '') for this in headings if 'Approved' in this]
    print(tracks)
    data_saved = True # Set to True when the data is the same as on file and False when not

    # ------ Window Layout ------
    layout = [[sg.Table(values=data, headings=headings, max_col_width=55,
                        # background_color='light blue',
                        auto_size_columns=True,
                        display_row_numbers=True,
                        justification='right',
                        num_rows=10,
                        alternating_row_color='lightblue',
                        key='-TABLE-',
                        row_height=35,
                        tooltip='This is a table')],
              [sg.Button('Open')],
              [[sg.Button(f'Approve {track}'), sg.Button(f'Exclude {track}'), sg.Button(f'Comment {track}')] for track in tracks],
              [sg.Button('Save')],
             ]

    # ------ Create Window ------
    window = sg.Window('QA Table', layout,
                       # font='Helvetica 25',
                       )

    def save_results(default_path):
        save_file = sg.popup_get_file('Select file to save results to:', default_path=str(default_path))
        save_file = Path(save_file)
        df.to_csv(save_file, index=False)
        data_saved = True


    # ------ Event Loop ------
    while True:
        event, values = window.read()
        print(event, values)

        if event == sg.WIN_CLOSED:
            #res = sg.popup_ok_cancel('Have you saved your results?')
            #print(res)
            if not data_saved:
                save_results(file_path)
            break

        if event == 'Open':
            selected_values = values.get('-TABLE-')
            if selected_values == []:
                #TODO: Add popup to warn no row selected
                continue
            selected_value = selected_values[0]
            workspace_path = Path(df.loc[selected_value, 'Path'])
            if workspace_path.exists():
                dwl.view_workspace(workspace_path, dsi_studio_path)
                df.loc[selected_value, 'Reviewed'] = True
                data = dataframe_to_lists(df)
                data_saved = False
                window['-TABLE-'].update(values=data, select_rows=[selected_value])
            else:
                sg.popup('Workspace path not found!')
        elif 'Approve' in event:
            track = event.replace('Approve ','')
            print(track)
            assert track in tracks
            selected_values = values.get('-TABLE-')
            if selected_values == []:
                #TODO: Add popup
                continue
            selected_value = selected_values[0]
            df.loc[selected_value, f'{track} Approved'] = True
            data = dataframe_to_lists(df)
            data_saved = False
            window['-TABLE-'].update(values=data, select_rows=[selected_value])
        elif 'Exclude' in event:
            track = event.replace('Exclude ','')
            print(track)
            assert track in tracks
            selected_values = values.get('-TABLE-')
            if selected_values == []:
                #TODO: Add popup
                continue
            selected_value = selected_values[0]
            df.loc[selected_value, f'{track} Approved'] = False
            data = dataframe_to_lists(df)
            data_saved = False
            window['-TABLE-'].update(values=data, select_rows=[selected_value])
        elif 'Comment' in event:
            print(track)
            track = event.replace('Comment ','')
            assert track in tracks
            comment = sg.popup_get_text(f'{track} Comment:')
            selected_values = values.get('-TABLE-')
            if selected_values == []:
                #TODO: Add popup
                continue
            selected_value = selected_values[0]
            df.loc[selected_value, f'{track} Comment'] = comment
            data = dataframe_to_lists(df)
            data_saved = False
            window['-TABLE-'].update(values=data, select_rows=[selected_value])
        elif event == 'Save':
            save_results(file_path)
            data_saved = True

    window.close()

if __name__ == "__main__":
    file_path = Path(sys.argv[1])
    main(file_path)
