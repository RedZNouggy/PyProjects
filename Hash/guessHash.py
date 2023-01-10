#!/usr/bin/python3

from urllib.request import urlopen
import hashlib
from termcolor import colored

sha1hash = input("[+] Enter sha1 Hash value: ")

try:
    passwordList = str(urlopen('https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10-million-password-list-top-1000000.txt').read(), 'utf-8')
    for password in passwordList.split('\n'):
        hashguess = hashlib.sha1(bytes(password,'utf-8')).hexdigest()
        if hashguess == sha1hash:
            print(colored("[+] The password is: "+str(password),'green'))
            break 
        else:
            print(colored("[-] Essaie " + password + " : Pas valable",'red'))
except Exception as exc:
    print('There was a problem: %s' % (exc))
