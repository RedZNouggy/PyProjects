#!/usr/bin/python3

# Made by Samuel PAGES 19/03/2023
import re
import os
import argparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import shutil
import subprocess

# Retrieving the Spotify album link from the command line arguments
parser = argparse.ArgumentParser(description='Download Spotify album as MP3')
parser.add_argument('album_url', type=str, help='Link of the Spotify album')
args = parser.parse_args()
album_url = args.album_url

# Retrieve artist name and album name from Spotify page title
html = requests.get(album_url).text
soup = BeautifulSoup(html, 'html.parser')
title = soup.find('title').text
album_name = re.sub(r' - .* by .*', '', title).strip()
artist_name = re.sub(r'.* - .* by ', '', title).replace(' | Spotify', '').strip()

# Creating a folder with the artist's name
if not os.path.exists(f'{Change-Path}{artist_name}/'):
    os.mkdir(f'{Change-Path}{artist_name}/')

# Create a folder with the name of the album
if not os.path.exists(f'{Change-Path}{artist_name}/{album_name}/'):
    os.mkdir(f'{Change-Path}{artist_name}/{album_name}/')

# Download the album with spotdl
subprocess.run(["python3", "-m", "spotdl", f' -o {Change-Path}{artist_name}/{album_name}/', album_url], check=True)

dir_path = f"{Change-Path}{artist_name}/{album_name}/"

# Move all MP3 files to the destination folder
for file_name in os.listdir("{Change-Path}"):
    if file_name.endswith(".mp3"):
        src_path = os.path.join(os.getcwd(), file_name)
        dst_path = os.path.join(dir_path, file_name)
        shutil.move(src_path, dst_path)

if os.path.exists(f'{Change-Path}.spotdl-cache'):
    os.remove('{Change-Path}.spotdl-cache')
