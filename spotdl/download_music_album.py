#!/usr/bin/env python3

############################ Samuel's Script ############################
## Created by Samuel PAGES | 05 July 2023
## Retrieve the Spotify album link from the command line arguments
#########################################################################

import re
import os
import sys
import argparse
import shutil
import subprocess
from colorama import Fore, Style
import requests
from bs4 import BeautifulSoup

# Info message
def infotext(msg) -> str:
    '''Display informational message on console in blue
    Arguments: the creation date, hash, OS, scope, source, user as a verbose option.
    msg -- text to be printed
    '''
    print(Fore.BLUE + "[i] " + msg + Style.RESET_ALL)

# Error message
def errortext(msg) -> str:
    '''Display success message on console in green
    Arguments:
    msg -- text to be printed
    '''
    print(Fore.RED + "[-] " + msg + Style.RESET_ALL)

# Warning message
def warntext(msg) -> str:
    '''Display success message on console in green
    Arguments:
    msg -- text to be printed
    '''
    print(Fore.YELLOW + "[~] " + msg + Style.RESET_ALL)

# Success message
def successtext(msg) -> str:
    '''Display success message on console in green
    Arguments:
    msg -- text to be printed
    '''
    print(Fore.GREEN + "[+] " + msg + Style.RESET_ALL)

def download_album(album_url, temp_path, final_path):
    '''Retrieve the Spotify album link from the command line arguments

    Arguments:

    album_url --> Link of Spotify album
    temp_path --> Enter the path where MP3 will be temporary stored
    final_path --> Enter the path where MP3 will be definitly stored like ' '"{final_path} + / + artist_name + / + album_name + / + file_name"
    '''
    if not temp_path:
        errortext("You have to use --temp-path")
        sys.exit(1) # Exit Script with error
    if not final_path:
        errortext("You have to use --final-path")
        sys.exit(1) # Exit Script with error

    # Retrieve artist name and album name from Spotify page title
    html = requests.get(album_url, timeout=300).text
    soup = BeautifulSoup(html, 'html.parser')

    title = soup.find('title').text
    album_name = re.sub(r' - .* by .*', '', title).replace(',','').strip()
    artist_name = re.sub(r'.* - .* by ', '', title).replace(' | Spotify', '').replace(',','').strip()

    # Creating a folder with the artist's name
    if not os.path.exists(f'{final_path}/{artist_name}/'):
        os.mkdir(f'{final_path}/{artist_name}/')

    # Create a folder with the name of the album
    if not os.path.exists(f'{final_path}/{artist_name}/{album_name}/'):
        os.mkdir(f'{final_path}/{artist_name}/{album_name}/')

    # Download the album with spotdl
    subprocess.run(["spotdl", "--output", temp_path ,album_url], check=True)

    dir_path = f"{final_path}/{artist_name}/{album_name}/"

    # Move all MP3 files to the destination folder
    for file_name in os.listdir(f"{temp_path}"):
        if file_name.endswith(".mp3"):
            src_path = os.path.join(os.getcwd(), file_name)
            dst_path = os.path.join(dir_path, file_name)
            shutil.move(src_path, dst_path)

    if os.path.exists('{temp_path}/.spotdl-cache'):
        os.remove('{temp_path}/.spotdl-cache')

if __name__ == "__main__":
    # Parameters
    parser = argparse.ArgumentParser(description='Download Spotify album productions in MP3')
    parser.add_argument('album_url', type=str, help='Link of Spotify album')
    parser.add_argument('-t', '--temp-path', action="store", type=str, help='Enter the path where MP3 will be temporary stored')
    parser.add_argument('-f', '--final-path', action="store", type=str, help='Enter the path where MP3 will be definitly stored like "{final_path} + / + artist_name + / + album_name + / + file_name"')
    args = parser.parse_args()
