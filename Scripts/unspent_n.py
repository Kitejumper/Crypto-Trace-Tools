import json
import requests

address = str(raw_input("Enter the bitcoin address? "))

myfile = open('unspent_%s.txt' % address, 'w')

resp = requests.get('https://blockchain.info/unspent?active=%s' % address)

utxo_set = json.loads(resp.text)["unspent_outputs"]

myfile.write('TX_ID TX_Number Amount' + '\n' + '\n')

for utxo in utxo_set:
	myfile.write("%s %d %ld Satoshis" % (utxo['tx_hash_big_endian'], utxo['tx_output_n'], utxo['value']) + '\n')

myfile.write('\n' + '\n')

myfile = open('balance_%s.txt' % address, 'w')

	
balance = requests.get('https://blockchain.info/balance?active=%s' % address)

for line in balance:
	myfile.write(line + '\n')
	