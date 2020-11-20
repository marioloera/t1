#!/usr/bin/env python3
import os
from yapf.yapflib.yapf_api import FormatFile  # reformat a file

directory = os.path.dirname(os.path.realpath(__file__))
os.chdir(directory)
print(f'directory:\n {directory}')

files_to_format = []
for root, _, files in os.walk(directory):

    for name in files:
        if '.py' not in name:
            continue
        print(name)
        file = os.path.join(root, name)

        files_to_format.append(file)

style = 'google'
print(f'Formated files with {style}_style:')
for file in files_to_format:
    file = os.path.join(directory, file)
    print(' {f}'.format(f=file))
    FormatFile(file, style_config=style, in_place=True)
