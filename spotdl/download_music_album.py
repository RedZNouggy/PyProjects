#!/usr/bin/python3

import re
import os
import argparse
import shutil
import subprocess
from colorama import Fore, Style
import requests
from bs4 import BeautifulSoup

# Retrieving the Spotify album link from the command line arguments
parser = argparse.ArgumentParser(description='Download Spotify album in MP3')
parser.add_argument('album_url', type=str,
                    help='Link of Spotify album')
parser.add_argument('--temp-path', action="store", type=str,
                    help='Enter the path where MP3 will be temporary stored')
parser.add_argument('--final-path', action="store", type=str,
                    help='Enter the path where MP3 will be definitly stored like '
                    '"{final_path} + / + artist_name + / + album_name + / + file_name"')

args = parser.parse_args()
album_url = args.album_url


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


if not args.temp_path:
    errortext("You have to use --temp-path")
else:
    temp_path = args.temp_path
if not args.final_path:
    errortext("You have to use --final-path")
else:
    final_path = args.final_path

# Retrieve artist name and album name from Spotify page title
html = requests.get(album_url, timeout=300).text
soup = BeautifulSoup(html, 'html.parser')

title = soup.find('title').text
album_name = re.sub(r' - .* by .*', '', title).strip()
artist_name = re.sub(r'.* - .* by ', '', title).replace(' | Spotify', '').strip()

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
