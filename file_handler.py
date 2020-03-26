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

def collectFiles(files,address):
    #print('working on:',address)
    for p in os.listdir(address):
        fullPath = os.path.join(address,p)
        if os.path.isfile(fullPath):
            #print('Found file: '+p)
            files.append(fullPath)
        elif os.path.isdir(fullPath):
            #print('Found folder: '+p,fullPath)
            collectFiles(files,fullPath)
    return

def collectFolders(files,address):
    #print('working on:',address)
    for p in os.listdir(address):
        fullPath = os.path.join(address,p)
        if os.path.isdir(fullPath):
            #print('Found folder: '+p,fullPath)
            files.append(fullPath)
            collectFolders(files,fullPath)
    return

def findArtist(artists):
    regexp = "(\s&|\sfeat|,|;|\s-|\sft|\svs\s)"
    artist = re.split(regexp,artists,flags=re.IGNORECASE)[0].strip()
    return artist

source = path.Path("M:\\_working_repo\\file_handler\\content\\source")
destination = path.Path("M:\\_working_repo\\file_handler\\content\\destination")

sFiles = []
dFolders = []
folders = []

if os.path.exists(source):
    print("OK: source path found")
    if os.path.exists(destination):
        print("OK: destination path found")
        collectFiles(sFiles,source)
        collectFolders(dFolders,destination)

filesLength = len(sFiles)
print('Found:',filesLength,'files in source')
print('Found:',len(dFolders),'folders in destination')


for f in sFiles:
    file = eyed3.load(f)
    artist = file.tag.artist

    if artist != None and len(artist)>1 and re.search('www',artist,flags=re.IGNORECASE) == None:
        artist = findArtist(file.tag.artist)
    else:
        _,artist = os.path.split(f)
        artist = findArtist(artist)

    print(artist)
