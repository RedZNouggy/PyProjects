#!/usr/bin/python3

import requests
import argparse

API_KEY = "" # METTRE VOTRE API KEY HERE

# Fonction pour récupérer le SHA1 à partir du SHA256
def get_sha1(sha256):
    url = f"https://www.virustotal.com/api/v3/files/{sha256}"
    headers = {
        "x-apikey": API_KEY
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if "data" in data:
            attributes = data["data"]["attributes"]
            if "sha1" in attributes:
                return attributes["sha1"]
    return None

# Fonction pour récupérer le MD5 à partir du SHA256
def get_md5(sha256):
    url = f"https://www.virustotal.com/api/v3/files/{sha256}"
    headers = {
        "x-apikey": API_KEY
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if "data" in data:
            attributes = data["data"]["attributes"]
            if "md5" in attributes:
                return attributes["md5"]
    return None

# Récupération du hash SHA256 en paramètre
parser = argparse.ArgumentParser(description='Récupère le SHA1 et le MD5 correspondants à un hash SHA256')
parser.add_argument('sha256', type=str, help='Hash SHA256')
args = parser.parse_args()
sha256 = args.sha256

# Récupération du SHA1 et du MD5 correspondants
sha1 = get_sha1(sha256)
md5 = get_md5(sha256)

# Affichage du résultat SHA1
if sha1:
    print("\033[32m" + f"[+] Le SHA1 correspondant est : {sha1}" + "\033[0m")
else:
    print("\033[31m" + "[-] Impossible de récupérer le SHA1 correspondant." + "\033[0m")

# Affichage du résultat MD5
if md5:
    print("\033[32m" + f"[+] Le MD5 correspondant est : {md5}" + "\033[0m")
else:
    print("\033[31m" + "[-] Impossible de récupérer le MD5 correspondant." + "\033[0m")
