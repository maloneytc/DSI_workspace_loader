from pathlib import Path
import subprocess as sp

import sys

def view_workspace(workspace_dir, dsi_studio_path):
    workspace_dir = Path(workspace_dir)
    assert workspace_dir.exists()
    source_dir = workspace_dir.joinpath('slices')
    source_files = list(source_dir.glob('*.nii*')) + list(source_dir.glob('*.fib.gz'))
    source_file = source_files[0]
    query = [str(dsi_studio_path),
             '--action=vis',
             f'--source={str(source_file)}',
             '--stay_open=1',
             f'--cmd=load_workspace,{str(workspace_dir)}+add_surface']
    res = sp.check_output(query)

def get_dsi_path():
    dsi_path_mac = Path('/Applications/dsi_studio.app/Contents/MacOS/dsi_studio')
    if dsi_path_mac.exists():
        dsi_studio_path = dsi_path_mac
    else:
        dsi_studio_path = Path(input('Please enter the path to the dsi studio executable:'))

    if not dsi_studio_path.exists():
        print('The path to the dsi studio executable could not be found.')
        sys.exit(1)

    return dsi_studio_path


if __name__ == "__main__":
    usage = """python main.py [workspace list/main directory]"""

    if not len(sys.argv) == 2:
        print(usage)
        sys.exit(1)

    dsi_path = get_dsi_path()

    workspace_list = Path(sys.argv[1])
    assert workspace_list.exists()

    if workspace_list.is_file():
        with open(workspace_list, 'r') as fopen:
            lines = fopen.readlines()

        for line_num, line in enumerate(lines):
            if line.strip() == '':
                continue
            try:
            	subj_id, workspace_dir = line.strip().split(',')
            except ValueError:
                subj_id = None
                workspace_dir = line.strip()
            workspace_dir = Path(workspace_dir)
            if not workspace_dir.exists():
                print(f'Could not find the workspace directory {workspace_dir}')
                continue

            print(f'Loading subject {subj_id} ({line_num+1} of {len(lines)})\n')
            view_workspace(workspace_dir, dsi_path)

            print(20*'=')
    elif workspace_list.is_dir():
        subject_dirs = list(workspace_list.iterdir())
        n_dirs = len(subject_dirs)
        for line_num, subject_dir in enumerate(subject_dirs):
            subj_id = subject_dir.name
            if subject_dir.name == '.DS_Store':
                continue
            if not subject_dir.is_dir():
                continue

            workspace_dir = subject_dir.joinpath('DSI_workspace')
            if not workspace_dir.exists():
                print(f'Could not find the workspace directory {workspace_dir}')
                continue

            print(f'Loading subject {subj_id} ({line_num+1} of {n_dirs})\n')
            view_workspace(workspace_dir, dsi_path)

            print(20*'=')
