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
parser = argparse.ArgumentParser(description='Download Spotify artist productions in MP3')
parser.add_argument('artist_url', type=str,
                    help='Link of Spotify artist')
parser.add_argument('-t', '--temp-path', action="store", type=str,
                    help='Enter the path where MP3 will be temporary stored')
parser.add_argument('-f', '--final-path', action="store", type=str,
                    help='Enter the path where MP3 will be definitly stored like '
                    '"{final_path} + / + artist_name + / + album_name + / + file_name"')
parser.add_argument('-v', '--verbose', action="store_true", required=False, help='Get more infos')
args = parser.parse_args()
artist_url = args.artist_url

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

# Retrieve artist name
html_artist = requests.get(artist_url, timeout=300).text
soup_artist = BeautifulSoup(html_artist, 'html.parser')
artist_temp = soup_artist.find('title').text
artist_name = artist_temp.replace(' | Spotify', '').replace('/','').replace('\\','').strip()
infotext(artist_name)

# Retrive album links
album_links = []
for link in soup_artist.find_all("a"):
    href = link.get("href")
    if href and "/album/" in href:
        link_to_add = "https://open.spotify.com" + href
        if link_to_add not in album_links:
            album_links.append("https://open.spotify.com" + href)

# Check Album Links
albm_links = []
# for each links in artist spotify web page
for link in album_links:
    html_album = requests.get(link, timeout=300).content
    soup_album = BeautifulSoup(html_album, 'html.parser')
    TITLE_ALBUM = str(soup_album.find('title'))
    if artist_name in TITLE_ALBUM:
    #if artist_name in soup_album:
        if args.verbose:
            infotext("Found : " + link)
        # Retrieve Albm links and album names
        albm_links.append(link)
        album_name = re.sub(r' - .* by .*', '', TITLE_ALBUM).replace('/','').replace('<title>','').replace('\\','').strip()
        # Creating a folder with the artist's name
        if not os.path.exists(f'{final_path}/{artist_name}/'):
            os.mkdir(f'{final_path}/{artist_name}/')
            successtext(f"{final_path}/{artist_name}/ successfuly created")
        # Create a folder with the name of the album
        if not os.path.exists(f'{final_path}/{artist_name}/{album_name}/'):
            os.mkdir(f'{final_path}/{artist_name}/{album_name}/')
            successtext(f"{final_path}/{artist_name}/{album_name}/ successfuly created")
        # Download the album with spotdl
        subprocess.run(["spotdl", "--output", temp_path ,link], check=False)
        dir_path = f"{final_path}/{artist_name}/{album_name}/"
        # Move all MP3 files to the destination folder
        for file_name in os.listdir(f"{temp_path}"):
            if file_name.endswith(".mp3"):
                src_path = os.path.join(os.getcwd(), file_name)
                dst_path = os.path.join(dir_path, file_name)
                shutil.move(src_path, dst_path)
        if os.path.exists(f'{temp_path}/.spotdl-cache'):
            os.remove(f'{temp_path}/.spotdl-cache')
            if args.verbose:
                successtext(f"{temp_path}/.spotdl-cache successfuly removed")
    elif args.verbose:
        warntext("This link seems to be not related to " + artist_name + " " + link)
