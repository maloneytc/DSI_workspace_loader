# DSI_workspace_loader
Author: Tom Maloney malonetc@mail.uc.edu

Simple utility scripts to load workspaces in DSI_Studio

There is bug with Mac Sonoma and tkinter version 8.6.12 that causes buttons to stop working, to overcome this you’ll need to install python 3.12, which has an updated version of tkinter.

Dependencies:
pip install PySimpleGUI
pip install pandas

Usage: 
`load_workspace <path to workspace directory>`

or

`python gui.py <path to review csv file>`

Buttons:
“Open DSI Studio” – Opens DSI studio and loads the tracks of the patient in the selected row of the table.
“Toggle all” – Toggles all track approval checkboxes.
“Comment <track name>” – Adds a review comment to the specified track.
“Comment all” – Adds a comment to all tracks.
“Toggle Review” – Toggles the ‘Reviewed’ column of the currently selected row.
“Save” – Opens dialog box to select path to save results to.