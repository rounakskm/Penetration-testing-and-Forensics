#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May 10 19:12:57 2018

@author: starboy
"""
# Script to extract all data from firefox databases
# Get what was downloaded
# Cookies and browser history, 
# use cookies to log into web-pages that need authentication
# Get search history if google search was performed

import re
import os
import sqlite3
import optparse

# Function to print all the files downloaded
def print_downloads(downloadsDB):
    conn = sqlite3.connect(downloadsDB)
    c= conn.cursor()
    c.execute('SELECT name, source, datetime(endTime/1000000, \'unixepoch\') FROM moz_downloads;')
    
    print '-----Files Downloaded----- '
    for row in c:
        print '[+] File: '+str(row[0])+' from source:'+str(row[1])+' at: '+str(row[2]) 
        
# Function to print cookies
def print_cookies(cookieDB):
    try:
        conn = sqlite3.connect(cookieDB)
        c= conn.cursor()
        c.execute('SELECT host, name, value FROM moz_cookies;')
        
        print '-----Cookies Found-----'
        for row in c:
            host = str(row[0])
            name = str(row[1])
            value = str(row[2])
            
            print '[+] Host: '+host+' Name: '+name+' Value: '+value
            
    except Exception as e:
        if 'encrypted' in str(e):
            print '[!] Error reading cookies database'
            print 'Please update Python-Sqlite3 library'
            
# Function to print browser history
def print_history(placesDB):
    try:
        conn = sqlite3.connect(placesDB)
        c= conn.cursor()
        c.execute('SELECT url, datetime(visit_date/1000000, \'unixepoch\') \
                  FROM moz_places, moz_historyvisits WHERE visit_count>0 \
                  and moz_places.id == moz_historyvisits.place_id;')
        
        print '-----Browser History Found-----'
        for row in c:
            url = str(row[0])
            date = str(row[1])
            
            print '[+] '+date+' |Visited: '+url
            
    except Exception as e:
        if 'encrypted' in str(e):
            print '[!] Error reading places database'
            print 'Please update Python-Sqlite3 library'
                
# Function to extract google search keyword
def google_search(placesDB):
    try:
        conn = sqlite3.connect(placesDB)
        c= conn.cursor()
        c.execute('SELECT url, datetime(visit_date/1000000, \'unixepoch\') \
                  FROM moz_places, moz_historyvisits WHERE visit_count>0 \
                  and moz_places.id == moz_historyvisits.place_id;')
        
        print '-----Google Search Keywords-----'
        for row in c:
            url = str(row[0])
            date = str(row[1])
            
            if 'google' in url.lower():
                r = re.findall(r'q=.*\&', url)
                if r:
                    search = r[0].split('&')[0]
                    search = search.replace('q=', '').replace('+', ' ')
                    print '[+] '+date+' Searched for: '+search 
                
    except Exception as e:
        if 'encrypted' in str(e):
            print '[!] Error reading places database'
            print 'Please update Python-Sqlite3 library'
    
# Option parsing
parser = optparse.OptionParser('Usage:: -p <firefox profile path>')
parser.add_option('-p', dest='profile_path', type='string', help='enter the firefox profile path which holds the .sqlite DBs')
(options, args) = parser.parse_args()
path = options.profile_path

# Check if parameters entered are empty
if (path == None):
    print(parser.usage)
    exit(0)
elif os.path.isdir(path) == False:
    print '[!] Path does not exist'
    exit(0)
else:
    downloadDB = os.path.join(path, 'downloads.sqlite')
    if os.path.isfile(downloadDB):
        print_downloads(downloadDB)
    else:
        print '[!] downloadDB does not exist'
    
    cookiesDB = os.path.join(path, 'cookies.sqlite')
    if os.path.isfile(cookiesDB):
        print_cookies(cookiesDB)
    else:
        print '[!] cookiesDB does not exist'
        
    placesDB = os.path.join(path, 'places.sqlite')
    if os.path.isfile(placesDB):
        print_history(placesDB)
        google_search(placesDB)
    else:
        print '[!] pplacesDB does not exist'
    