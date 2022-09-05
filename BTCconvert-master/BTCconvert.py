#################################################################################
#   Copyright © 2017 DCScoder
#
#                                    ~ BTCconvert ~
#
#   Description:  BTCconvert is an interactive historic Bitcoin cryptocurrency converter.
#
#   Usage:        python  BTCconvert.py
#
#   Change Log:   v1.0 Initial release for any currency and historic date conversion
#
#################################################################################

import requests
import sys

__version__ = 'v1.0'
__author__ = 'DCScoder'
__email__ = 'dcscoder@gmail.com'

print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print("~ BTCconvert " + __version__ + " developed by",__author__, "~")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

print("Powered by CoinDesk\n")

def main():
    # Arguments
    value = float(input("\nInsert BTC (i.e.: '1.0') -> "))
    print("\n")
    date = str(input("Insert required DATE (i.e.: '2017-10-01') -> "))
    print("\n")
    currency = str(input("Insert required CURRENCY CODE (i.e.: 'GBP') -> "))
    print("\n")

    # Utilises Coindesk Bitcoin Price Index API to determine valuation of BTC
    url1 = "https://api.coindesk.com/v1/bpi/historical/close.json&?start="
    url2 = "&end="
    url3 = "&currency="
    req_currency = currency
    req_date = date
    source = url1 + req_date + url2 + req_date + url3 + req_currency

    try:
        data = (requests.get(source)).json()
    except:
        sys.exit("Error obtaining currency rates, ensure internet connection is active...")

    # Process BTC value and convert to currency value
    rate = (data['bpi'][req_date]) * value
    c = str(round(rate, 2))
    print(value, "BTC =",c, req_currency +"\n")

    main()

if __name__ == "__main__":
    main()