# Windows music files organizer
import os
import pathlib as path
import eyed3
import re

print('''
File Handler v.py
version 0.1
Developed by Sam. K.
''')

def collectFiles(source):
    for p in os.listdir(source):
        fullPath = os.path.join(source,p)
        if os.path.isfile(fullPath):
            #print('Found file: '+p)
            files.append(fullPath)
        elif os.path.isdir(fullPath):
            #print('Found folder: '+p)
            collectFiles(fullPath)
    return
def findArtist(artists):
    regexp = "(\s&|\sfeat|,|;|\s-|\sft|\svs\s)"
    artist = re.split(regexp,artists,flags=re.IGNORECASE)[0].strip()
    return artist

source = path.Path("M:\\_working_repo\\file_handler\\content\\source")
destination = path.Path("M:\\_working_repo\\file_handler\\content\\destination")

files = []
folders = []

if os.path.exists(source):
    print("OK: source path found")
    if os.path.exists(destination):
        print("OK: destination path found")
        collectFiles(source)

filesLength = len(files)
print('Found:',filesLength,'files')

for f in files:
    file = eyed3.load(f)

    temp = file.tag.artist

    if temp != None and len(temp)>1 and re.search('www',temp,flags=re.IGNORECASE) == None:
        artist = findArtist(file.tag.artist)
    else:
        _,artist = os.path.split(f)
        artist = findArtist(artist)

    print(artist)
