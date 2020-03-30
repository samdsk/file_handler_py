# Windows music files organizer
#eyed3, in header file commented log error out 'Lame tag CRC check failed'
#set as pass

import os
import pathlib as path
import eyed3
import re
import shutil
import hashlib
#import logging

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

def collectFolders(dFolders,address):
    #print('working on:',address)
    for p in os.listdir(address):
        fullPath = os.path.join(address,p)
        if os.path.isdir(fullPath):
            #print('Found folder: '+p,fullPath)
            _,artist = os.path.split(fullPath)
            dFolders[artist] = fullPath
            collectFolders(dFolders,fullPath)
    return

def findArtist(artists):
    regexp = "(\s&|\sfeat|,|;|\s-|\sft|\svs\s|/|\sand\s|\x00|\sx\s)"
    print(re.split(regexp,artists,flags=re.IGNORECASE))
    artist = re.split(regexp,artists,flags=re.IGNORECASE)[0].strip()
    return artist

def fileCopy(f,des):
    try:
        shutil.copy2(f,des,follow_symlinks=True)
        print("File copied successfully.")
    # If source and destination are same
    except Exception as e:
        print('Error:',e)
    return

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def logWrite(msg):
    logFile.write(msg)
    logFile.write('\n')
    return

source = path.Path("M:\\_working_repo\\file_handler\\content\\source")
destination = path.Path("M:\\_working_repo\\file_handler\\content\\destination")
logPath = path.Path("M:\\_working_repo\\file_handler\\content\\log\\log.txt")

sFiles = []
dFolders = {}

logFile = open(logPath,'w+')

if os.path.exists(source):
    logWrite("OK: source path found")
    #print("OK: source path found")
    if os.path.exists(destination):
        logWrite("OK: destination path found")
        #print("OK: destination path found")
        collectFiles(sFiles,source)
        collectFolders(dFolders,destination)

filesLength = len(sFiles)
logWrite('Found: '+str(filesLength)+' files in source',)
logWrite('Found: '+str(len(dFolders))+' folders in source',)
print('Found:',filesLength,'files in source')
print('Found:',len(dFolders),'folders in destination')

web_re = 'w+\.[a-zA-Z0-9]+\.[a-zA-Z0-9]|unknown' #esclude url like artist tags
count = 0

for f in sFiles:
    print(f)
    ocs = md5(f)
    ncs = None
    fPath = None
    artist = None
    audiofile = eyed3.load(f)
    try:
        if hasattr(audiofile,'tag') and hasattr(audiofile.tag,'artist'):
            artist = audiofile.tag.artist
            logWrite('Original artist: '+str(artist))
            print('Original artist:',artist)

        _,filename = os.path.split(f)
        #find artist name
        if artist != None and len(artist)>1 and re.search(web_re,artist,flags=re.IGNORECASE) == None:
            artist = findArtist(artist)
        else:
            artist = findArtist(filename)

        logWrite('working on >> Artist: '+str(artist)+' >> Filename: '+str(filename))
        print('Artist:',artist,'Filename:',filename)
        #checking for destination folder

        if artist in dFolders:
            fPath = os.path.join(dFolders[artist],filename)
            if os.path.isfile(fPath):
                #logWrite('>>>>>>>>>>> OK: File already exists!')
                print('File already exists!')
                ncs = md5(fPath)
                count += 1
            else:
                #logWrite('>>>>>>>>>>> WARNING: File not found in destination. >> Copying.')
                print('WARNING: File not found in destination. >> Copying.')
                fileCopy(f,dFolders[artist])
                ncs = md5(fPath)
                count += 1
        else:
            #logWrite('>>>>>>>>>>> WARNING: Artist folder not found: '+str(artist)+' >> Continue as new artist.')
            print('Artist not found',artist)
            dfolder = os.path.join(destination,artist.title())

            #logWrite('>>>>>>>>>>> Formated folder name: '+str(dfolder))
            print(dfolder)

            if not os.path.exists(dfolder):
                try:
                    os.mkdir(dfolder)
                    #logWrite('>>>>>>>>>>> OK: Created folder named: '+str(artist)+' in destination')
                    print('Created folder named:',artist,'in destination')
                except Exception as e:
                    logWrite('>>>>>>>>>>> Error: '+str(e))
                    print(e)

                #logWrite('>>>>>>>>>>> OK: Copying file to newly created folder.')
                print('Copying file to newly created folder')
                fileCopy(f,dfolder)
                fPath = os.path.join(dfolder,filename)
                dFolders[artist] = dfolder
                ncs = md5(fPath)
                count += 1
            else:
                logWrite('>>>>>>>>>>> Folder exists so skipped.')
                print('Folder exists so skipped.')
    except:
        logWrite('>>>>>>>>>>>>ERROR CAUSED BY>>>>>>>>>>>>>>>>')
        logWrite(str(str.encode((f))))
        logWrite('>>>>>>>>>>>>>>>>>>><<<<>>>>>>>>>>>>>>>>>>>>')
    logWrite('-------------------------------------------------------------------')
    print(ocs,ncs,ocs==ncs)
print('Files handled:',count)

logFile.close()
