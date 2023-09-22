# Shodanus version 1.0
## Description:
    This program is designed for crawling from the shodan.io website

## Features:
    * It is possible to add many accounts, if the limit of one account ends, another one is used
    * It is possible to use the Tor network, it is not enabled by default, for this you need to add a key [--tor].
    * To work with large results, you can save to the file [-o results.json], or view after finishing with the key [-i],
    you can also use these keys at the same time. Interactive mode has its own help:
        [a: all results], [{1}: info for index 1], [h: help], [q: quit]
        [c: components], [s: all hostname],
        [{0} p: {host index} {open ports}], [{1} v: {host index} {vulnerabilities lsit}]

    * Еhe site only allows free accounts to receive 2 pages of results, so in this case it is useless to specify [-p > 2],
    the program will only receive 2 pages.
___
### Installation method 1:
	sudo apt install python3.11-venv
    git clone https://github.com/vomanc/Shodanus.git
    cd Shodanus
	python3 -m venv env
	source env/bin/activate
	python3 -m pip install --upgrade pip
	pip3 install -r requirements.txt
    python3 shodanus.py -q product:apache
___
### Installation method 2:
    git clone https://github.com/vomanc/Shodanus.git
    cd Shodanus
	pip3 install -r requirements.txt
    python3 shodanus.py -q product:apache
___
### Add accounts in users.json:
	[
    {"username": "my_account", "passwd": "my_password"},
    {"username": "my_account", "passwd": "my_password"}
    ]
___
### Option [--tor] requires the Tor package:
	sudo apt update && sudo apt install tor
___
### Examples running:
	python3 shodanus.py -q product:apache
	python3 shodanus.py -q product:apache -i --vv -p 2 --tor
	python3 shodanus.py -q product:apache -i --vv -o results.json -p 5 --tor
___
## Author: @vomanc
___
### Tech Stack

* __python3__
* __asyncio__
* __aiohttp__
* __tor__
___
### Donation
![Bitcoin](https://www.blockchain.com/explorer/_next/static/media/bitcoin.df7c9480.svg) BTC
* bc1q8ymcf78f4qwjlyj9v7q3ujtqm8nm9e3rms3rcq

![Ethereum](https://www.blockchain.com/explorer/_next/static/media/ethereum.57ab686e.svg) ETH
* 0x015a50222160E7EF9d0ED030BA232025234D0f82

![Tether](https://www.blockchain.com/explorer/_next/static/media/usdt.dd7e4bef.svg) USDT
* 0x015a50222160E7EF9d0ED030BA232025234D0f82
---
![WebMoney](https://www.webmoney.ru/favicon-32x32.png)
### WebMoney
* WMZ: Z826298065674
* WME: E786709266824
