#!/usr/bin/python3

import sys
import subprocess

# Checking the number of arguments
if len(sys.argv) != 2:
    print("Usage: python3 list.py tabl.txt")
    sys.exit(1)

# Opening the text file in read mode
filename = sys.argv[1]
with open(filename, 'r') as f:
    # Reading the file line by line
    for line in f:
        # Removal of spaces at the beginning and end of a line
        line = line.strip()
        # Execution of the "download line" command using subprocess
        subprocess.run(["python3", "{ChangePath}download-music.py", line], check=True)
