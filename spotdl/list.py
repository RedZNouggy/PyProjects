#!/usr/bin/python3

import sys
import os
import argparse
import subprocess
from colorama import Fore, Style


# Retrieving the Spotify album link from the command line arguments
parser = argparse.ArgumentParser(description='Launch download_music_artist.py and download_music_album.py')
parser.add_argument('-artist', action="store_true", required=False, help='Use Artist Links')
parser.add_argument('--album', action="store_true", required=False, help='Use Album Links')
parser.add_argument('tabl', help='Path to tabl.txt')
parser.add_argument('--verbose', action="store_true", required=False, help='get verbose for download_music*.py')
args = parser.parse_args()


# Error message
def errortext(msg) -> str:
    '''Display success message on console in green
    Arguments:
    msg -- text to be printed
    '''
    print(Fore.RED + "[-] " + msg + Style.RESET_ALL)


# Checking the number of arguments
if not args.tabl or (not args.album and not args.artist) or (args.album and args.artist):
    errortext("Usage: python3 list.py --album tabl.txt || or || python3 list.py --artist tabl.txt")
    sys.exit(1)

# Opening the text file in read mode
FILE_NAME = args.tabl

with open(FILE_NAME, 'r', encoding="utf-8") as f:
    if os.path.getsize(FILE_NAME) == 0:
        errortext("Nothing in the txt file")
    else:
        # Reading the file line by line
        for line in f:
            # Removal of spaces at the beginning and end of a line
            line = line.strip()
            if args.artist:
                # Execution of the "download line" command using subprocess
                if args.verbose:
                    subprocess.run([
                        "python3",
                        "/opt/data2To/download/download_music_artist.py",
                        "--temp-path", "/opt/data2To/download",
                        "--final-path" ,"/opt/data2To/Musics",
                        line,
                        "--verbose"
                    ], check=False)
               else:
                    subprocess.run([
                        "python3",
                        "/opt/data2To/download/download_music_artist.py",
                        "--temp-path", "/opt/data2To/download",
                        "--final-path" ,"/opt/data2To/Musics",
                        line
                    ], check=False)
            if args.album:
                # Execution of the "download line" command using subprocess
                if args.verbose:
                    subprocess.run([
                        "python3",
                        "/opt/data2To/download/download_music_album.py",
                        "--temp-path", "/opt/data2To/download",
                        "--final-path" ,"/opt/data2To/Musics",
                        line,
                        "--verbose"
                    ], check=False)
               else:
                    subprocess.run([
                        "python3",
                        "/opt/data2To/download/download_music_album.py",
                        "--temp-path", "/opt/data2To/download",
                        "--final-path" ,"/opt/data2To/Musics",
                        line
                    ], check=False)
