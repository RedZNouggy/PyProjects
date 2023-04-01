#!/usr/bin/python3

import sys
import os
import subprocess
from colorama import Fore, Style

# Checking the number of arguments
if len(sys.argv) != 2:
    print("Usage: python3 list.py tabl.txt")
    sys.exit(1)


# Error message
def errortext(msg) -> str:
    '''Display success message on console in green
    Arguments:
    msg -- text to be printed
    '''
    print(Fore.RED + "[-] " + msg + Style.RESET_ALL)


# Opening the text file in read mode
FILE_NAME = sys.argv[1]
with open(FILE_NAME, 'r', encoding="utf-8") as f:
    if os.path.getsize(FILE_NAME) > 0:
        errortext("Nothing in the txt file")
    else:
        # Reading the file line by line
        for line in f:
            # Removal of spaces at the beginning and end of a line
            line = line.strip()
            # Execution of the "download line" command using subprocess
            subprocess.run([
                "python3",
                "{ChangePath}download_music.py",
                "--temp-path '{ChangePath}'",
                "--final-path '{ChangePath}'",
                line
            ], check=False)
