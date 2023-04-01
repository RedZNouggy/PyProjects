## spotdl

[To Download spotdl](https://github.com/spotDL/spotify-downloader)

### DON'T FORGET TO CHANGE EVERY {ChangePath} IN "download-music.py" AND "list.py"

To launch it if you use the alias in .bashrc : 
```
download {spotify-link}
```

usage: download_music.py [-h] [--temp-path TEMP_PATH] [--final-path FINAL_PATH] album_url

Download Spotify album in MP3

positional arguments:
  album_url             Link of Spotify album

optional arguments:
  -h, --help            show this help message and exit
  --temp-path TEMP_PATH
                        Enter the path where MP3 will be temporary stored
  --final-path FINAL_PATH
                        Enter the path where MP3 will be definitly stored like "{final_path} + / + artist_name + / + album_name + / + file_name"
                        

To launch it with a list of album links to earn some time :
```
./list.py tabl.txt
```
![Capture d'écran 2023-03-19 001746](https://user-images.githubusercontent.com/81537743/226145030-8031e764-a70c-45be-a2d1-57d39c25b524.png)
