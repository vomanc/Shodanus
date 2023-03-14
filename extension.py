""" Banner, user-agents used in the script """
from random import choice
import base64


BANNER = b'CiAgICAqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioKICAgIHwgICAgIF8\
    gICAgICAgICAgICAgICBfICAgICAgICAgICAgICAgICAgICAgICAgfAogICAgfCBfX198IHxfXyAgIF9fXyAgIF9ffCB8I\
        F9fIF8gXyBfXyAgXyAgIF8gX19fICB8CiAgICB8LyBfX3wgJ18gXCAvIF8gXCAvIF9gIHwvIF9gIHwgJ18gXHwgfCB\
            8IC8gX198IHwKICAgIHxcX18gXCB8IHwgfCAoXykgfCAoX3wgfCAoX3wgfCB8IHwgfCB8X3wgXF9fIFwgfCAKI\
                CAgIHx8X19fL198IHxffFxfX18vIFxfXyxffFxfXyxffF98IHxffFxfXyxffF9fXy8gfAogICAgfCAgICA\
                    gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHYgMS4wICB8CiAgICAqKioqKioqKioqK\
                        ioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioK'
banner = base64.b64decode(BANNER).decode('utf-8')

user_agent_list = [
    "(Windows NT 10.0; rv:105.0) Gecko/20100101 Firefox/105.0",
    "(Windows NT 10.0; rv:106.0) Gecko/20100101 Firefox/106.0",
    "(Windows NT 10.0; rv:107.0) Gecko/20100101 Firefox/107.0",
    "(Windows NT 10.0; rv:108.0) Gecko/20100101 Firefox/108.0",
    "(Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/109.0",
    "(X11; Ubuntu; Linux x86_64; rv:105.0) Gecko/20100101 Firefox/105.0",
    "(X11; Ubuntu; Linux x86_64; rv:106.0) Gecko/20100101 Firefox/106.0",
    "(X11; Ubuntu; Linux x86_64; rv:107.0) Gecko/20100101 Firefox/107.0",
    "(X11; Ubuntu; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0",
    "(X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0",
    "(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106 Safari/537.36",
    "(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107 Safari/537.36",
    "(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108 Safari/537.36",
    "(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109 Safari/537.36",
    ]

JSON_HELP = '''
[*] The "user.json" file format must follow the standard json format, e.g.:
________________
[
    {"username": "myuser1", "passwd": "my_passwd"}
]

_______OR_______e.g.:

[
    {"username": "myuser1", "passwd": "my_passwd"},
    {"username": "myuser2", "passwd": "my_passwd"},
    {"username": "myuser3", "passwd": "my_passwd"}
]
________________
'''

json_headers = {
    "Accept": "application/json",
    "Content-type": "json"
}


def my_headers():
    """ Generation headers """
    user_agent = "Mozilla/5.0 " + choice(user_agent_list)
    acpt = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
    ref = "https://account.shodan.io/login?continue=http%3A%2F%2Fwww.shodan.io%2Fdashboard"
    headers_1 = {
        "Host": "account.shodan.io",
        "User-Agent": user_agent,
        "Accept": acpt,
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://account.shodan.io",
        "Connection": "keep-alive",
        "Referer": ref,
        "Cookie": "",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Sec-GPC": "1",
        "TE": "trailers",
        }

    headers_2 = {
        "Host": "www.shodan.io",
        "User-Agent": user_agent,
        "Accept": acpt,
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Content-Type": "application/x-www-form-urlencoded",
        "Connection": "keep-alive",
        "Referer": "https://www.shodan.io/search?query=",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Sec-GPC": "1",
        "TE": "trailers",
        }
    return headers_1, headers_2
