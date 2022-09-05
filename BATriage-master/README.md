# BATriage


#### Description:

BATriage is an interactive triaging tool which can be used to search a valid bitcoin address and return information on the address in fast time. Results are returned into command terminal for quick access and an .xlsx report is also generated for each bitcoin address queried, which contains retrieved data.

#### API's Utilised:

- Utilises Blockchain.info API to search for valid P2PKH/P2SH addresses
and fetch account summary data along with recent activity (50 max).

- Utilises Coindesk API to obtain up-to-date conversion rates for BTC
to standard currencies incl. GBP, USD and EUR.

- Utilises ShapeShift API to check for any cryptocurrency exchanging.

#### Artefacts Supported:

- Address
- Hash160
- Address to micro message decoding
- Total transactions count
- Total BTC received
- Total BTC sent
- Current BTC balance
- BTC to GBP, USD, EUR real-time currency converters
- Timestamps of recent transactions (50 max)
- SHA256 hash values of recent transactions (50 max)
- ShapeShift lookup, transaction ID, coin type exchanged, withdrawal address

#### Usage:

```
python BATriage.py
```
