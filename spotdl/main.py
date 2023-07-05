#!/usr/bin/env python3
# -*- coding: utf-8 -*-

############################ Samuel's Script ############################
## Created by Samuel PAGES
## 05 July 2023
#########################################################################

"""Entry point."""
import os
import sys
import argparse
import re

from download_music_artist import download_artist, warntext, errortext
from download_music_album import download_album 

def samsrv_banner():
    '''
        Display Banner
        A part of this function is from https://github.com/t3l3machus/hoaxshell
    '''
    
    ##### Colors #####
    END = '\033[0m'
    
    padding = '  '
    S = [[' ', '┌','─','┐'], [' ', '└','─','┐'], [' ', '└','─','┘']]
    A = [[' ', '┌','─','┐'], [' ', '├','─','┤'], [' ', '┴',' ','┴']]
    M = [[' ', '┌','┬','┐'], [' ', '│','│', '│'], [' ', '┴',' ','┴']]
    R = [[' ', '┬','─','┐'], [' ', '├','┬','┘'], [' ', '┴','└','─']]
    V = [[' ', '┬',' ',' ','┬'], [' ', '└','┐','┌','┘'], [' ', ' ','└','┘',' ']]

    banner = [S, A, M, S, R, V]
    final = []
    print('\r')
    init_color = 36
    txt_color = init_color
    cl = 0
    for charset in range(0, 3):
        for pos in range(0, len(banner)):
            for i in range(0, len(banner[pos][charset])):
                clr = f'\033[38;5;{txt_color}m'
                char = f'{clr}{banner[pos][charset][i]}'
                final.append(char)
                cl += 1
                txt_color = txt_color + 36 if cl <= 3 else txt_color
            cl = 0
            txt_color = init_color
        init_color += 31
        if charset < 2:
            final.append('\n   ')
    print(f"   {''.join(final)}")
    print(f'{END}{padding}                         by Samuel PAGES\n')

samsrv_banner()

# Retrieving the Spotify album link from the command line arguments
parser = argparse.ArgumentParser(description='Download Spotify links as MP3 and store it')
parser.add_argument('-u', '--url', type=str, help='Link of Spotify (can be artist url or album url)')
parser.add_argument('--file', type=str, action="store", help='Path to txt file containing a spotify artist or album link for each lines')
parser.add_argument('-t', '--temp-path', action="store", required=True, type=str, help='Enter the path where MP3 will be temporary stored')
parser.add_argument('-f', '--final-path', action="store", required=True, type=str, help='Enter the path where MP3 will be definitly stored like "{final_path} + / + artist_name + / + album_name + / + file_name"')
parser.add_argument('-v', '--verbose', action="store_true", required=False, help='Get more infos')
args = parser.parse_args()

def check_spotify_artist_link(link):
    pattern = r"https:\/\/open\.spotify\.com\/artist\/[a-zA-Z0-9]+(\?.*)?$"
    return bool(re.match(pattern, link))

def check_spotify_album_link(link):
    pattern = r"https:\/\/open\.spotify\.com\/album\/[a-zA-Z0-9]+(\?.*)?$"
    return bool(re.match(pattern, link))

def main():
    '''Does everything'''

    if args.file:
        # Opening the text file in read mode
        with open(args.file, 'r', encoding="utf-8") as in_file:
            if os.path.getsize(args.file) == 0:
                errortext("Nothing in the txt file")
                sys.exit(1) # Exit Script with error
            else:
                # Reading the file line by line
                for line in in_file:
                    # Removal of spaces at the beginning and end of a line
                    line = line.strip()
                    if check_spotify_artist_link(line):
                        download_artist(line, args.temp_path, args.final_path, args.verbose)
                    elif check_spotify_album_link(line):
                        download_album(line, args.temp_path, args.final_path)
                    else:
                        warntext(f"The url : {line} is not valid (not used)")
    if args.url:
        if check_spotify_artist_link(args.url):
            download_artist(args.url, args.temp_path, args.final_path, args.verbose)
        elif check_spotify_album_link(args.url):
            download_album(args.url, args.temp_path, args.final_path)
        else:
            warntext(f"The url : {args.url} is not valid (not processed for it)")
if __name__ == "__main__":
    main()
