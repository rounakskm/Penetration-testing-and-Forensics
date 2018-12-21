#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 16 22:28:14 2018

@author: starboy
"""

import sys
import optparse
from scapy.all import *

def sniff_dot(p):
    if p.haslayer(Dot11ProbeResp):
        addr2 = p.getlayer(Dot11).addr2
        if addr2 in hidden_nets and addr2 not in unhidden_nets:
            name = p.getlayer(Dot11ProbeResp).info
            print(f"Decloacked Hidden SSID: {name} for MAC: {addr2}")
            unhidden_nets.append(addr2)
            
    if p.haslayer(Dot11Beacon):
        if p.getlayer(Dot11Beacon).info == '':
            addr2 = p.getlayer(Dot11).addr2
            if addr2 not in hidden_nets:
                print(f"[-]Detected Hidden SSID with MAC: {addr2}")
                hidden_nets.append(addr2)
                
                


# Option parsing
parser = optparse.OptionParser('usage % prog -i <interface>')
parser.add_option('-i', dest='interface', type='string', help='specify interface in monitor mode to listen on') 
(options, args) = parser.parse_args()
if options.interface == None:
	print (parser.usage)
	exit(0)


interface = options.interface
hidden_nets = []

unhidden_nets = []


try: 
	sniff(iface=interface, prn=sniff_dot)
except KeyboardInterrupt:
	exit(0)
except:
    print('Check if interface is in monitor mode')





