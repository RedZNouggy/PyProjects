#!/usr/bin/python3

# The subprocess module in Python allows you to spawn new processes, connect to their input/output/error pipes,
# and obtain their return codes. It is a powerful tool for running system commands,
# as it allows you to leverage the functionality of the underlying operating system.
import subprocess 

# https://psutil.readthedocs.io/ 
import psutil

# To compare strings with regex patern
import re

# The colored module is a Python library that allows you to add color to your text and ANSI escape codes to your console output.
# It provides a number of functions for printing text in different colors, each of which corresponds to a specific ANSI color code.
from termcolor import colored

# Test MAC ADDRESS
def is_valid_mac_address(mac_address):
    # Compile a regular expression to match the MAC address pattern
    pattern = r'^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$'
    regex = re.compile(pattern)
    
    # Return True if the string matches the pattern, False otherwise
    return regex.match(mac_address) is not None


# Get a list of all network interfaces and their status
interfaces = psutil.net_if_addrs()
number = 0
itf = ""

print('\033[4mEvery interfaces :\033[0m')
# Find every interfaces
for interface, addresses in interfaces.items():
    number = number + 1
    print("[" + str(number) + "] " ,end="")
    itf = itf + ":" + str(interface) 
    print(interface)

# Choose your interface
selected_interface = int(input(colored("[?] Select your interface : [1], [2], ... :",'magenta')))
interface = itf.split(":")[selected_interface]

# Infos + OLD MAC ADDRESS
print(colored("[i] You 've chosen : ",'cyan'),end="")
print(colored(interface,'yellow'))
old_mac = interfaces[interface][2].address
print(colored("[i] Your actual mac address on ",'cyan'),end="")
print(colored(interface,'yellow'),end="")
print(colored(" is : ",'cyan'),end="")
print(colored(old_mac,'yellow'))

# NEW MAC ADDRESS
mac = input(colored("[?] Enter your new mac address : ",'magenta'))
mac = mac.replace(' ','')

if is_valid_mac_address(mac) == True : # Valid new mac address
    print(colored("[i] Your new mac address has a valid pattern ",'cyan'))

else: # Error new mac address not valid
    if is_valid_mac_address(old_mac) == True :
        print(colored("[-] Your new mac adddress has not valid pattern (pattern example : " + old_mac + ")",'red'))
    else:
        print(colored("[-] Your new mac adddress has not valid pattern (pattern example : 01:23:45:67:89:ab)",'red'))



def change_mac_address (interface,mac):

    # Commands
    disable_mac = ["sudo ip link set " + interface + " down"]
    set_mac_address = ["sudo ip link set " + interface + " address " + mac]
    enable_mac = ["sudo ip link set " + interface + " up"]

    # Run Commands
    subprocess.call(disable_mac, shell=True)
    subprocess.call(set_mac_address, shell=True)
    subprocess.call(enable_mac, shell=True)

change_mac_address(interface,mac)

interfaces = psutil.net_if_addrs()
new_mac = interfaces[interface][1].address

if str(old_mac) == str(new_mac):
    print(colored("[-] Your 'new mac adddress' has not been applied",'red'))
    print(colored("[-] Your actual mac address is : " + new_mac, 'red'))
else:
    print(colored("[+] Your 'new mac adddress' has been applied",'green'))
    print(colored("[+] Your new mac : ",'green'),end="")
    print(colored(new_mac, 'yellow'))
