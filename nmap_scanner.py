#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  8 02:06:55 2018

@author: starboy
"""
import nmap
import optparse
from threading import Thread

# Function to scan target host and given port using nmap, this performs the basic 
# TCP syn scan which is nmaps default scan
def nmap_scan(t_host, t_port):
    n_scan = nmap.PortScanner()
    n_scan.scan(t_host, t_port)
    # Extracting state information from nested dictionary created by scan
    state = n_scan[t_host]['tcp'][int(t_port)]['state']
    print('[*]'+t_host+'tcp/'+t_port+' '+ state)
    
# Option parsing
parser = optparse.OptionParser('Usage: -H <target host> -p <target port>')
parser.add_option('-H', dest='t_host', type='string', help='enter target host')
parser.add_option('-p', dest='t_port', type='string', help='enter target port/s separated by comma')
(options, args) = parser.parse_args()
t_host = options.t_host
t_port = str(options.t_port).split(',')

# Check if parameters entered are empty
if (t_host == None) or (t_port[0] == None):
    print(parser.usage)
    exit(0)

for port in t_port:
    t = Thread(target=nmap_scan, args=(t_host, port))
    t.start()
