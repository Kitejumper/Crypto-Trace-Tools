##################################################
# This uses the "API" of Blockchain.info         #
# Since Blockchain.info doesn't support Bech32   #
# addresses in their API, they will not show up. #
# If you want to work with Bech32, use a         #
# different API.                                 ## Daniel.Buetikofer@zuerich.ch                   #
##################################################

import json
import requests

def find_cluster_address(target_address,step):
    global address_found
    global f
    global steps
    global outputs

    if (step < steps):

        r = requests.get("https://blockchain.info/address/%s?filter=1&format=json" % target_address)

        try:
            tx_sent_json = json.loads(r.text)["txs"]
        except:
            tx_sent_json = {}
            print("[x] An error occured while grabbing address: %s" % (target_address))
            print(">>> %s" % r.text)

        if (len(tx_sent_json) > 0):
            for tx in tx_sent_json:
                # checking inputs
                input_values = []
                if (len(tx["inputs"]) > 1):
                    for input in tx["inputs"]:
                        # this has to be done because of Bech32 not beeing supported and therefore the address doesn't show up in the json
                        if (input["prev_out"].get("addr")):
                            # saving input values to check for change
                            input_values.append(int(input["prev_out"]["value"]))
                            if (input["prev_out"]["addr"] not in address_found):
                                print("[!] Cluster address found (multi-input heuristic): %s" % input["prev_out"]["addr"])
                                address_found.append(input["prev_out"]["addr"])
                                f.write("%s\n" % input["prev_out"]["addr"])
                                find_cluster_address(input["prev_out"]["addr"], step + 1)
                    # checking change address - BUGGY - but works for practical
                    input_values.sort()
                    if (len(input_values) > 0):
                        if (len(tx["out"]) <= outputs) and (len(tx["out"]) > 1):
                            for output in tx["out"]:
                                if (int(output["value"]) < input_values[0]) and (output["addr"][:1] == target_address[:1]) and (output["addr"] not in address_found):
                                    print("[!] Change address found (optimal change heuristic):  %s" % output["addr"])
                                    address_found.append(output["addr"])
                                    f.write("%s\n" % output["addr"])
                                    find_cluster_address(output["addr"], step + 1)
                        else:
                            print("[x] More than your specified outputs: %s (specified: %s)" % (len(tx["out"]) , outputs))
                            break
                else:
                    print("[x] Only one input, can't identify change address (all outputs would qualify)")
                    break


address = str(input("Enter the bitcoin address to cluster: "))
print("----------------------------------------------------------------------------------")

while (address[:3] == "bc1") or address == "":
    print("[x] Bech32 (starting with bc1) addresses not supported")
    print("----------------------------------------------------------------------------------")
    address = str(input("Enter the bitcoin address to cluster: "))
    print("----------------------------------------------------------------------------------")

print("The more outputs you choose, the less reliable the script is...")
try:
    outputs = int(input("Whats is the maximum of outputs you want to work with? (Default=2): "))
except:
    outputs = 2

if (outputs < 1):
    outputs = 2

print("Each level is one crawl. Every address identified as belonging to the cluster in that crawl, will get crawled until the level specified is reached.")
try:
    steps = int(input("How many levels do you want to go down? (Default=1): "))
except:
    steps = 1

if (steps < 1):
    steps = 1

print("----------------------------------------------------------------------------------")
f = open("cluster_%s.txt" % address, "w")
# write header
f.write("ADDR\n")
f.write("%s\n" % address)

address_found = list()
address_found.append(address)
print("[!] Initial address added: %s" % address)

find_cluster_address(address,0)

# Lets see if we need to do more...

print("----------------------------------------------------------------------------------")
print("[!] Finished... %s addresses found" % len(address_found))
print("[!] Output located at: cluster_%s.txt" % address)
print("----------------------------------------------------------------------------------")
