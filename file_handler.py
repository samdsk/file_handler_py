import sys, os, pathlib as Path, re, codecs, shutil
from tinytag import TinyTag as TT

artist_escape = 'w+\.[a-zA-Z0-9]+\.[a-zA-Z0-9]|unknown'
artist_splitter = "(\s&|\sfeat|,|;|\s-|\sft|\svs\s|/|\sand\s|\x00|\sx\s|\||\sx\s)"

def collectFiles(files,address):
    #print('working on:',address)
    for p in os.listdir(address):
        fullPath = os.path.join(address,p)
        if os.path.isfile(fullPath) and p.endswith((".mp3",".m4a",".flac",".alac")):
            #print('Found file: '+p)
            files.append(fullPath)
        elif os.path.isdir(fullPath):
            #print('Found folder: '+p,fullPath)
            collectFiles(files,fullPath)
    return

def findArtist(artists):
    artist = re.split(artist_splitter,artists,flags=re.IGNORECASE)[0].strip()
    return artist

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def fileCopy(f,des):
    try:
        shutil.copy2(f,des,follow_symlinks=True)
        print("File copied successfully.")
    # If source and destination are same
    except Exception as e:
        print('Error:',e)
    return

def fileHandler(files,destination):
    for f in files:
        try:
            print('Working on:',f)
            try:
                print('Working on artist and handling the file.')
                artists = None
                artist = None
                filename = os.path.basename(f)
                audiofile = TT.get(f)
                if hasattr(audiofile,'artist'):
                    artists = audiofile.artist
                if artists != None and len(artists)>1 and re.search(artist_escape,artists,flags=re.IGNORECASE) == None:
                    artist = findArtist(artists)
                else:
                    artist = findArtist(filename)
                print(artists,'>>>>',artist)

                artist = artist.title()

                temp_dpath = os.path.join(destination,artist)
                temp_fullpath = os.path.join(temp_dpath,filename)

                if os.path.exists(temp_dpath):
                    if not os.path.exists(temp_fullpath):
                        print('WARNING: File not found in destination. >> Copying.')
                        fileCopy(f,temp_dpath)
                    else:
                        print('File already exists!')
                else:
                    print('Artist not found',artist)
                    try:
                        os.mkdir(temp_dpath)
                        print('Created folder named:',artist,'in destination.')
                        print('Copying file to newly created folder.')
                        fileCopy(f,temp_dpath)
                    except Exception as e:
                        print('>>>>>>>>>>> Error: while creating folder.')
                        print(e)
            except Exception as e:
                print('>>>>>>>>>>> Error:')
                print(e)
        except Exception as e:
            print('>>>>>>>>>>> Error:')
            print(e)
            print(str(os.path.basename(f)).encode())
        print('---------------------------------------------------------------')
    return

def main():
    source = Path.Path("M:\\_working_repo\\file_handler\\content\\source")
    destination = Path.Path("M:\\_working_repo\\file_handler\\content\\destination")
    sFiles = []
    sys.stdout = open('artist_log','w+')
    if os.path.exists(source):
        #print("OK: source path found")
        collectFiles(sFiles,source)
        fileHandler(sFiles,destination)
    else:
        print("Error: source path error")
        return

main()
