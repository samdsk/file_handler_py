# Windows music files organizer
import os
import pathlib as path
import eyed3

print('''
File Handler v.py
version 0.1
Developed by Sam. K.
''')

source = path.Path("M:\\_working_repo\\file_handler\\content")

if os.path.exists(source):
    print("OK: source path found")

files = []

for p in os.listdir(source):
    full = os.path.join(source,p)
    if os.path.isfile(full):
        files.append(full)

for f in files:
    file = eyed3.load(f)
    print(file.tag.artist)
    print('\n')
