from pathlib import Path
import sys
import PySimpleGUI as sg
import random
import string
import pandas as pd
import subprocess as sp
import main as dwl

import pdb


# N.B. There are some bugs with registering mouse clicks on Mac Sonoma. 
# The solution is to upgade your python installation to 3.12 and make sure tkinter version is >=8.6.13
# Use the line below to check version information. 
#print(sg.get_versions())

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
    data_saved = True # Set to True when the data is the same as on file and False when not

    # ------ Window Layout ------
    layout = [[sg.Table(values=data, headings=headings, max_col_width=55,
                        # background_color='light blue',
                        auto_size_columns=True,
                        display_row_numbers=True,
                        justification='right',
                        num_rows=10,
                        vertical_scroll_only=False,
                        alternating_row_color='lightblue',
                        key='-TABLE-',
                        row_height=35,
                        enable_events=True,
                        enable_click_events=True,
                        bind_return_key=True,
                        tooltip='QA table')],
              [sg.Button('Open DSI Studio')],
              [sg.Frame('', [
                [sg.Button('Toggle all')] + [sg.Checkbox(f'Approve {track}', key=f'Chckbx-{track}', enable_events=True) for track in tracks],
                [sg.Button(f'Comment {track}', key=f'Commt-{track}') for track in tracks],
                [sg.Button('Comment all')],
                [sg.Button('Toggle Review')]
               ], visible=False, key='-FRAME-')],

              [sg.Button('Save')],
             ]

    # ------ Create Window ------
    window = sg.Window('QA Table', layout,
                        resizable=True
                       # font='Helvetica 25',
                       )

    def save_results(default_path):
        save_file = sg.popup_get_file('Select file to save results to:', default_path=str(default_path))
        if save_file is None:
            return
        save_file = Path(save_file)
        df.to_csv(save_file, index=False)

    def update_table(selected_row):
        data = dataframe_to_lists(df)
        window['-TABLE-'].update(values=data, select_rows=[selected_row])

    # ------ Event Loop ------
    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            #res = sg.popup_ok_cancel('Have you saved your results?')
            #print(res)
            if not data_saved:
                save_results(file_path)
            break

        if event == 'Open DSI Studio':
            selected_values = values.get('-TABLE-')
            if selected_values == []:
                #TODO: Add popup to warn no row selected
                continue
            selected_row = selected_values[0]
            workspace_path = Path(df.loc[selected_row, 'Path'])
            if workspace_path.exists():
                dwl.view_workspace(workspace_path, dsi_studio_path)
                df.loc[selected_row, 'Reviewed'] = True
                update_table(selected_row)
                data_saved = False
            else:
                sg.popup('Workspace path not found!')

        elif event == '-TABLE-':
            selected_values = values.get('-TABLE-')
            if selected_values == []:
                frame = window['-FRAME-'].update('', visible=False)
                continue
            selected_row = selected_values[0]
            selected_subject = df.loc[selected_row, 'ID']
            for track in tracks:
                track_approved = df.loc[selected_row, f'{track} Approved']
                if isinstance(track_approved, bool):
                    window[f'Chckbx-{track}'].update(value=track_approved)
                else:
                    window[f'Chckbx-{track}'].update(value=False)
            window['-FRAME-'].update(selected_subject, visible=True)

        elif '+CLICKED+' in event:
            # Double clicking on a comment cell
            row, col = cell = event[2]
            if row == -1: # indicates the header was clicked
                continue
            selected_col_name = df.columns[col]
            if ' Comment' in selected_col_name:
                existing_comment = df.loc[row, selected_col_name]
                if not isinstance(existing_comment, str):
                    existing_comment = ''
                comment = sg.popup_get_text(f'{selected_col_name}:', default_text=existing_comment)

                df.loc[row, selected_col_name] = comment
                update_table(row)
                data_saved = False

        elif event == 'Toggle all':
            selected_values = values.get('-TABLE-')
            selected_row = selected_values[0]
            for track in tracks:
                current_value = window[f'Chckbx-{track}'].get()
                new_value = not current_value
                window[f'Chckbx-{track}'].update(value=new_value)
                df.loc[selected_row, f'{track} Approved'] = new_value
            update_table(selected_row)
            data_saved = False

        elif event == 'Toggle Review':
            selected_values = values.get('-TABLE-')
            selected_row = selected_values[0]
            reviewed = df.loc[selected_row, 'Reviewed']
            df.loc[selected_row, 'Reviewed'] = not reviewed
            update_table(selected_row)
            data_saved = False

        elif 'Chckbx-' in event:
            track = event.replace('Chckbx-','')
            assert track in tracks
            selected_values = values.get('-TABLE-')
            selected_row = selected_values[0]
            track_approved = window[f'Chckbx-{track}'].get()
            df.loc[selected_row, f'{track} Approved'] = track_approved
            update_table(selected_row)
            data_saved = False

        elif event == 'Comment all':
            comment = sg.popup_get_text(f'Comment:')
            selected_values = values.get('-TABLE-')
            if selected_values == []:
                #TODO: Add popup
                continue
            selected_row = selected_values[0]
            for track in tracks:
                df.loc[selected_row, f'{track} Comment'] = comment
            update_table(selected_row)
            data_saved = False

        elif 'Commt' in event:
            track = event.replace('Commt-','')
            assert track in tracks
            selected_values = values.get('-TABLE-')
            selected_row = selected_values[0]
            existing_comment = df.loc[selected_row, f'{track} Comment']
            if not isinstance(existing_comment, str):
                existing_comment = ''
            comment = sg.popup_get_text(f'{track} Comment:', default_text=existing_comment)

            df.loc[selected_row, f'{track} Comment'] = comment
            update_table(selected_row)
            data_saved = False

        elif event == 'Save':
            save_results(file_path)
            data_saved = True

        window.refresh()

    if not data_saved:
        save_results(file_path)

    window.close()

if __name__ == "__main__":
    file_path = Path(sys.argv[1])
    main(file_path)
