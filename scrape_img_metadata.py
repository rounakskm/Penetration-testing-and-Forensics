#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May 10 17:47:08 2018

@author: starboy
"""

# Script connects to specified url address
# scrapes all images present in the website
# downloads and extracts all the metadata

import urllib2
import optparse
from urlparse import urlsplit
from os.path import basename
from bs4 import BeautifulSoup
from PIL import Image
from PIL.ExifTags import TAGS

# Takes url address and returns list of images
def find_imgs(url):
    print '[+] Finding images in: '+ url
    
    url_content = urllib2.urlopen(url).read()
    soup = BeautifulSoup(url_content)
    
    img_tags = soup.findAll('img')
    return img_tags

# Download images 
def download_img(tag):
    try:
        print '[+] Downloading images...'
        img_src = tag['src']
        img_content = urllib2.urlopen(img_src).read()
        img_filename = basename(urlsplit(img_src)[2])
        img_file = open(img_filename, 'wb')
        img_file.write(img_content)
        img_file.close()
        return img_filename
    except:
        return ''
    
# Check for metadata
def img_exif(img_filename):
    try:
        exif_data ={}
        img_file = img.open(img_filename)
        info = img_file._getexif()
        if info:
            for key,value in info.items():
                decoded = TAGS.get(tag, tag)
                exif_data[decoded] = value
                exif_gps = exif_data['GPSInfo']
                if exif_gps:
                    print '[*] '+img_filename+ ' contains GPS metadata'
    except:
        pass
    
# Option parsing
parser = optparse.OptionParser('Usage:: -u <URL of the webpage>')
parser.add_option('-u', dest='url', type='string', help='enter the URL')
(options, args) = parser.parse_args()
url = options.url

# Check if parameters entered are empty
if (url == None):
    print(parser.usage)
    exit(0)
    
    
img_tags = find_imgs(url)

for tag in img_tags:
    img_filename = download_img(tag)
    img_exif(img_filename)
        

        
        
        
        