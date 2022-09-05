#!/usr/bin/env python

import os.path
import urllib2
import json

datain = raw_input("Enter the path to your 'address' file:")

if os.path.exists(datain):
	data = open(datain, "r")
	outfile = open("balances.txt", 'w')
	print "Extracting balances, please wait....."
	for line in data:
		bal = "https://blockchain.info/balance?active=%s" % line.rstrip()
		balance = urllib2.urlopen(bal)
		data2 = json.loads(balance.read())
		print line
		print data2[line.rstrip()]['final_balance']
		outfile.write(str(data2) + "\n")
	outfile.close()
	data.close()
else:
	sorry = "Sorry, not a valid path, please re-run the program"
	print sorry