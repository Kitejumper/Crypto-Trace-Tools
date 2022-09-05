set /p drive1=What drive letter is assigned to your USB device?--
mkdir %drive1%:\%computername%

cd "c:\Program Files\bitcoin\daemon"

bitcoin-cli getwalletinfo > %drive1%:\%computername%\info.txt

bitcoin-cli getnettotals > %drive1%:\%computername%\nettotals.txt

bitcoin-cli getnetworkinfo > %drive1%:\%computername%\netinfo.txt

bitcoin-cli getpeerinfo > %drive1%:\%computername%\peerinfo.txt

bitcoin-cli listtransactions "*" 1000 > %drive1%:\%computername%\listTX.txt

bitcoin-cli listunspent > %drive1%:\%computername%\unspent.txt
