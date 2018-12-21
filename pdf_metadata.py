#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  9 14:58:55 2018

@author: starboy
"""
# Extracting metadata from a pdf document

import optparse
from pyPdf import PdfFileReader

# Extracts and prints the metadata
def print_metadata(file_name):
    pdf_file = PdfFileReader(open(file_name, 'rb'))
    doc_info = pdf_file.getDocumentInfo()
    
    print"[*] Metadata for:"+ str(file_name)
    
    for item in doc_info:
        print "[+]"+str(item)+"  : "+str(doc_info[item])
        
# Option parsing
parser = optparse.OptionParser('Usage:: -P <PDF file name>')
parser.add_option('-P', dest='file', type='string', help='enter the PDF file name')
(options, args) = parser.parse_args()
file1 = options.file

# Check if parameters entered are empty
if (file1 == None):
    print(parser.usage)
    exit(0)
    
print_metadata(file1)
        
