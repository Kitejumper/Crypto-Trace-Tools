#################################################################################
#   Copyright © 2018 DCScoder
#
#                                    ~ BATriage ~
#
#   Description:  BATriage is an interactive triaging tool which can be used to search
#                 a valid bitcoin address and return information on the address in fast time.
#                 Results are returned into command terminal for quick access and an .xlsx report
#                 is also generated for each bitcoin address queried, which contains retrieved data.
#
#                 Utilises Blockchain.info API to search for valid P2PKH/P2SH addresses
#                 and fetch account summary data along with recent activity (50 max).
#
#                 Utilises Coindesk API to obtain up-to-date conversion rates for BTC
#                 to standard currencies incl. GBP, USD and EUR.
#
#                 Utilises ShapeShift API to check for any cryptocurrency exchanging.
#
#   Usage:        python  BATriage.py
#
#   Artefacts:    Address
#                 Hash160
#                 Address to micro message decoding
#                 Total transactions count
#                 Total BTC received
#                 Total BTC sent
#                 Current BTC balance
#                 BTC to GBP, USD, EUR real-time currency converters
#                 Timestamps of recent transactions (50 max)
#                 SHA256 hash values of recent transactions (50 max)
#                 ShapeShift lookup, transaction ID, coin type exchanged, withdrawal address
#
#   Change Log:   v1.0  Initial release on CLI for basic address info
#                 v1.1  Currency converter built-in and excel report generation
#                 v1.2  Improved excel report formatting
#                 v1.3  Restructure of code
#                 v1.4  ShapeShift lookup built-in & address/hash160 to micro message decode
#                 v1.5  Reviewed and updated ShapeShift lookup facility
#
#################################################################################

import requests
import datetime
import xlsxwriter
import binascii

__version__ = 'v1.5'
__author__ = 'DCScoder'
__email__ = 'dcscoder@gmail.com'

# UNIX-10 digit timestamp converter
def UNIX10(timestamp):
    return datetime.datetime.utcfromtimestamp(timestamp).strftime("%a %d %B %Y %H:%M:%S")

# BTC stored as whole no so multiplied value by 10^-8 to represent as float
def BTC2F(BTC):
    return BTC * 10**-8

# HEX to ASCII
def H2A(mm):
    return (binascii.unhexlify(mm)).decode("latin-1")

print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print("~ BATriage " + __version__ + " developed by",__author__, "~")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

print("Tips:\n"
      "1. Ensure you have an active internet connection.\n"
      "2. Ensure address is 26-35 alphanumeric characters.\n"
      "3. P2PKH (Pay To PubKey Hash) regular expression: 1[a-km-zA-HJ-NP-Z1-9]{25,34}\n"
      "4. P2SH (Pay To Script Hash) regular expression: 3[a-km-zA-HJ-NP-Z1-9]{25,34}")

def main():
    # Utilises Blockchain API to search input address
    url = "https://blockchain.info/rawaddr/"
    input_address = input("\nInsert address to triage -> ")
    source = url + input_address

    try:
        data = (requests.get(source)).json()
    except:
        print("\nError, refer to tips and try again...")
        main()

    # Create .xlsx report and format
    workbook = xlsxwriter.Workbook("BATriage_" + input_address + ".xlsx")
    worksheet_1 = workbook.add_worksheet("Address Summary")
    worksheet_2 = workbook.add_worksheet("Currency Conversions")
    worksheet_3 = workbook.add_worksheet("Recent Transaction Timestamps")
    worksheet_4 = workbook.add_worksheet("Recent Transaction Hashes")
    worksheet_5 = workbook.add_worksheet("ShapeShift Lookup")
    worksheet_6 = workbook.add_worksheet("About")
    row1 = 2
    row2 = 2
    col1 = 1
    col2 = 1
    format1 = workbook.add_format()
    format1.set_font_size(18)
    format1.set_bold()
    format2 = workbook.add_format()
    format2.set_bold()
    format2.set_align('right')
    format3 = workbook.add_format()
    format3.set_align('center')
    format4 = workbook.add_format()
    format4.set_bold()
    format4.set_align('center')
    worksheet_1.set_column('B:B', 16) + worksheet_1.set_column('C:C', 42)
    worksheet_2.set_column('B:B', 17) + worksheet_2.set_column('C:C', 13)
    worksheet_2.set_column('D:D', 13) + worksheet_2.set_column('E:E', 13)
    worksheet_3.set_column('B:B', 29)
    worksheet_4.set_column('B:B', 65)
    worksheet_5.set_column('B:B', 45) + worksheet_5.set_column('C:C', 65)
    worksheet_6.set_column('B:B', 110)
    worksheet_1.write("A1", "Address Summary", format1)
    worksheet_2.write("A1", "Currency Conversions", format1) + worksheet_2.write("B4", "Total Received:", format2)
    worksheet_2.write("B5", "Total Sent:", format2) + worksheet_2.write("B6", "Final Balance:", format2)
    worksheet_2.write("C3", "GBP", format4) + worksheet_2.write("D3", "USD", format4)
    worksheet_2.write("E3", "EUR", format4) + worksheet_2.write("B8", "Rates Last Updated:", format4)
    worksheet_3.write("A1", "Recent Transaction Timestamps", format1)
    worksheet_4.write("A1", "Recent Transaction Hashes", format1)
    worksheet_5.write("A1", "ShapeShift Lookup", format1)
    worksheet_6.write("A1", "About", format1) + worksheet_6.write("B3", "BATriage " + __version__)
    worksheet_6.write("B5", "The currency conversion rates are powered by CoinDesk.")
    worksheet_6.write("B6", "Maximum 50 records returned for transaction timestamps and hashes, if present.")
    worksheet_6.write("B7", "Micro message is decoded from hash160. Visual inspection on decoded string required "
                            "to determine if address is a micro message.")

    # Summary of bitcoin address
    # Micro message decoding (20 bytes)
    print("\n---------- Address Summary: ----------\n")
    h160 = (data['hash160'])
    print("Hash160:", h160)
    worksheet_1.write("B3", "Hash160:", format2) + worksheet_1.write("C3", str(h160), format3)
    #micro_msg = (binascii.unhexlify(h160)).decode("latin-1")
    micro_msg = H2A(h160)
    print("Micro Message:", "*see report*")
    worksheet_1.write("B4", "Micro Message:", format2) + worksheet_1.write("C4", str(micro_msg), format3)
    addy = (data['address'])
    print("Address:", addy)
    worksheet_1.write("B5", "Address:", format2) + worksheet_1.write("C5", str(addy), format3)
    tt = (data['n_tx'])
    print("Total Transactions:", tt)
    worksheet_1.write("B6", "Total Transactions:", format2) + worksheet_1.write("C6", str(tt), format3)
    tr = BTC2F(data['total_received'])
    print("Total Received:", tr, "BTC")
    worksheet_1.write("B7", "Total Received:", format2) + worksheet_1.write("C7", str(tr) + " BTC", format3)
    ts = BTC2F(data['total_sent'])
    print("Total Sent:", ts, "BTC")
    worksheet_1.write("B8", "Total Sent:", format2) + worksheet_1.write("C8", str(ts) + " BTC", format3)
    fb = BTC2F(data['final_balance'])
    print("Final Balance:", fb, "BTC")
    worksheet_1.write("B9", "Final Balance:", format2) + worksheet_1.write("C9", str(fb) + " BTC", format3)

    # Optional BTC to standard currency converter GBP, USD and EUR
    # Utilises Coindesk Bitcoin Price Index API to determine valuation of BTC
    converter = input("\nWould you like to apply standard currency converter to BTC? ('y' or 'n'):")
    if converter == 'y':
        print("\n---------- Currency Conversions: ----------\n")
        rate = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json").json()
        # Last updated rate timestamp ISO format
        lutime = (rate['time']['updatedISO'])
        print("Powered by CoinDesk - Last Updated:", lutime, "\n")
        worksheet_2.write("C8", str(lutime))

        # British Pound Sterling
        print("British Pound Sterling\n")
        gbp_rate = (rate['bpi']['GBP']['rate_float']) * BTC2F(data['total_received'])
        tr_p = str(round(gbp_rate, 2))
        print("Total Received:", tr_p, "GBP")
        worksheet_2.write("C4", tr_p, format3)
        gbp_rate = (rate['bpi']['GBP']['rate_float']) * BTC2F(data['total_sent'])
        ts_p = str(round(gbp_rate, 2))
        print("Total Sent:", ts_p, "GBP")
        worksheet_2.write("C5", ts_p, format3)
        gbp_rate = (rate['bpi']['GBP']['rate_float']) * BTC2F(data['final_balance'])
        fb_p = str(round(gbp_rate, 2))
        print("Final Balance:", fb_p, "GBP\n")
        worksheet_2.write("C6", fb_p, format3)

        # United States Dollar
        print("United States Dollar\n")
        usd_rate = (rate['bpi']['USD']['rate_float']) * BTC2F(data['total_received'])
        tr_d = str(round(usd_rate, 2))
        print("Total Received:", tr_d, "USD")
        worksheet_2.write("D4", tr_d, format3)
        usd_rate = (rate['bpi']['USD']['rate_float']) * BTC2F(data['total_sent'])
        ts_d = str(round(usd_rate, 2))
        print("Total Sent:", ts_d, "USD")
        worksheet_2.write("D5", ts_d, format3)
        usd_rate = (rate['bpi']['USD']['rate_float']) * BTC2F(data['final_balance'])
        fb_d = str(round(usd_rate, 2))
        print("Final Balance:", fb_d, "USD\n")
        worksheet_2.write("D6", fb_d, format3)

        # Euro
        print("Euro\n")
        eur_rate = (rate['bpi']['EUR']['rate_float']) * BTC2F(data['total_received'])
        tr_e = str(round(eur_rate, 2))
        print("Total Received:", tr_e, "EUR")
        worksheet_2.write("E4", tr_e, format3)
        eur_rate = (rate['bpi']['EUR']['rate_float']) * BTC2F(data['total_sent'])
        ts_e = str(round(eur_rate, 2))
        print("Total Sent:", ts_e, "EUR")
        worksheet_2.write("E5", ts_e, format3)
        eur_rate = (rate['bpi']['EUR']['rate_float']) * BTC2F(data['final_balance'])
        fb_e = str(round(eur_rate, 2))
        print("Final Balance:", fb_e, "EUR")
        worksheet_2.write("E6", fb_e, format3)

    else:
        print("\nCurrency converter not requested.")

    # Optional recent transaction activity timestamps
    # Timestamps encoded in UNIX 10-digit
    recents_time = input("\nWould you like to view recent activity timestamps? ('y' or 'n'):")
    if recents_time == 'y':
        print("\n---------- Recent Transaction Activity (Timestamps): ----------\n")
        for timestamp in data["txs"]:
            time = UNIX10(timestamp["time"])
            print(time)
            worksheet_3.write(row1, col1, str(time))
            row1 += 1
    else:
        print("\nTimestamps not requested.")

    # Optional recent transaction activity transaction identifiers
    # SHA256 hash values
    recents_hash = input("\nWould you like to view recent activity transaction identifiers? ('y' or 'n'):")
    if recents_hash == 'y':
        print("\n---------- Recent Transaction Activity (SHA256 Hash): ----------\n")
        for transaction in data["txs"]:
            hash = (transaction["hash"])
            print(hash)
            worksheet_4.write(row2, col2, str(hash))
            row2 += 1
    else:
        print("\nTransaction identifiers not requested.")

    # Optional ShapeShift lookup
    # Summary of ShapeShift data
    ss_lookup = input("\nWould you like to run a ShapeShift lookup? ('y' or 'n'):")
    if ss_lookup == 'y':
        print("\n---------- ShapeShift Summary: ----------\n")
        ss_data = requests.get("https://shapeshift.io/txStat/" + input_address).json()

        if "no_deposits" in ss_data['status']:
            print("Status: No deposits received via ShapeShift.")
            worksheet_5.write("B3", "Status:", format2) + worksheet_5.write("C3", "No deposits received via ShapeShift.", format3)

        elif "received" in ss_data['status']:
            print("Status: Deposit received via ShapeShift, but not processed as of yet.")
            worksheet_5.write("B3", "Status:", format2) + worksheet_5.write("C3", "Deposit received via ShapeShift, "
                                                                                 "but not processed as of yet.", format3)

        elif "failed" in ss_data['status']:
            print("Status:", ss_data['status'])
            worksheet_5.write("B3", "Status:", format2) + worksheet_5.write("C3", ss_data['status'], format3)

        elif "error" in ss_data['status']:
            print("Status: This address is NOT a ShapeShift deposit address.")
            worksheet_5.write("B3", "Status:", format2) + worksheet_5.write("C3", "This address is NOT a ShapeShift"
                                                                                  " deposit address.", format3)

        elif "complete" in ss_data['status']:
            print("Status: Deposit received via ShapeShift and processed.\n")
            worksheet_5.write("B3", "Status:", format2) + worksheet_5.write("C3", "Deposit received via "
                                                                                 "ShapeShift and processed.", format3)

            print("Withdrawal Address:", ss_data['withdraw'])
            worksheet_5.write("B5", "Withdrawal Address:", format2) + worksheet_5.write("C5", ss_data['withdraw'], format3)
            print("Amount Deposited:", ss_data['incomingCoin'])
            worksheet_5.write("B6", "Amount Deposited:", format2) + worksheet_5.write("C6", ss_data['incomingCoin'], format3)
            print("Coin Type Deposited:", ss_data['incomingType'])
            worksheet_5.write("B7", "Coin Type Deposited:", format2) + worksheet_5.write("C7", ss_data['incomingType'], format3)
            print("Amount Sent To Withdrawal Address:", ss_data['outgoingCoin'])
            worksheet_5.write("B8", "Amount Sent To Withdrawal Address:", format2) + worksheet_5.write("C8", ss_data['outgoingCoin'], format3)
            print("Coin Type Withdrawal:", ss_data['outgoingType'])
            worksheet_5.write("B9", "Coin Type Withdrawal:", format2) + worksheet_5.write("C9", ss_data['outgoingType'], format3)
            print("Transaction ID Of Coin Sent To Withdrawal Address:", ss_data['transaction'])
            worksheet_5.write("B10", "Transaction ID Of Coin Sent To Withdrawal Address:", format2) + \
            worksheet_5.write("C10", ss_data['transaction'], format3)

    else:
        print("\nShapeShift lookup not requested.")

    workbook.close()

    # Optional additional search
    new_search = input("\nWould you like to run a new search? ('y' or 'n'):")
    if new_search == 'y':
        main()
    else:
        print("\nTriage concluded, see script folder directory for report(s).")

if __name__ == "__main__":
    main()