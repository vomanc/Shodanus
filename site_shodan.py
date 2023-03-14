""" get shodan.io """
import re
import json
import asyncio
import aiofiles
import aiohttp
from aiohttp_socks import ProxyConnector, ProxyConnectionError
from crawler import MyBeautifulSoup
import extension


DOMAIN = 'https://www.shodan.io'
headers_1, headers_2 = extension.my_headers()


async def access_login_page(response):
    """ Login page access check """
    if 'banned you temporarily from accessing this website' in response:
        print('[!] This website has banned you temporarily from accessing')
        print('[*] It is recommended to change your IP address\n', '_'*20)
    elif 'You do not have access to account.shodan.io' in response \
        or 'Checking if the site connection is secure' in response:
        print('[*] The IP address is blocked, it is recommended to change the Tor chain\n', '_'*20)
    else:
        print('[!] Unknown error')


async def check_access(response, username):
    """ Account login verification """
    if 'Invalid username or password' in response:
        print(f'[!] Error: Invalid username or password for {username.upper()}')
        resp = False
    elif 'Too many login attempts' in response:
        print('[!] Error: Too many login attempts')
        resp = False
    elif '<title>Access denied</title>' in response:
        print('[!] Access denied')
        resp = False
    else:
        resp = True
    return resp


async def save_results(file_name, data):
    """ For save data in file """
    async with aiofiles.open(file_name, 'w') as file:
        await file.write(json.dumps(data))
        print('[+] The result is saved in a file')


async def read_file(file_name):
    """ Read file """
    async with aiofiles.open(file_name) as file:
        try:
            return json.loads(await file.read())
        except json.decoder.JSONDecodeError:
            print(extension.JSON_HELP)
            return False


async def data_set(token, username, passwd):
    """ Data for shodan.io authorization"""
    data = {
        "username": username,
        "password": passwd,
        "grant_type": "password",
        "continue": "http://www.shodan.io/dashboard",
        "csrf_token": token
        }
    return data


async def ip_check(session):
    """ Check current IP for TOR """
    headers = {
        "Accept": "application/json",
        "Content-type": "json"
        }
    url = 'https://api.myip.com'

    async with session.get(url, headers=headers) as response:
        if response.status == 200:
            resp = await response.text()
            print('[*] Your IP:', json.loads(resp)['ip'], '| RS:', response.status)
        else:
            print('[-] Request status:', response.status, '| Check the connection !')


async def search_shodan(session, url, verb_level, page):
    """ Search by [--query] in shodan  """
    print('[*] Searching ...')
    async with session.get(
        url, headers=headers_2, allow_redirects=True) as response:
        response = await response.text()
        if 'Daily search usage limit reached. Please wait a bit before doing' in \
            response:
            await session.close()
            print('[!] Daily search usage limit reached. Changing account ...')
            return False

        data = MyBeautifulSoup(response)
        await data.page_results()
        await data.pagination_url()

        if data.total_results is not False:
            if verb_level is False:
                await data.general_information()
                print(data.total_results)
            else:
                await data.only_hosts()

            if  data.next_page_num > page:
                return data.all_results
            await search_shodan(session, DOMAIN + data.pagination, verb_level, page)
            return data.all_results
        return data.all_results


async def verbose_level_info(session, url):
    """ Get host page and crawle info """
    try:
        async with session.get(
            DOMAIN + url, headers=headers_2,
            allow_redirects=True) as response:
            data = MyBeautifulSoup(await response.text())
            return await data.detail_info(url.replace('/host/', ''))
    except RuntimeError:
        print('[*] Daily limit reached while searching !')
        return 'Limit reached'


async def shodan(user, query, tor_proxy, verb_level, page):
    """Authorization and check login"""
    if tor_proxy is True:
        tor_proxy = ProxyConnector.from_url('socks5://127.0.0.1:9050')
        print('[+] Tor Network is used !')
    else:
        tor_proxy = None

    url = 'https://account.shodan.io'
    token = ''

    async with aiohttp.ClientSession(connector=tor_proxy) as session:
        async with session.get(url, headers=headers_1, allow_redirects=True) as response:
            response = await response.text()
            try:
                token = re.findall(r'(csrf_token" value=")(.*)"', response)[0][-1]
                print('[*] Authorization attempt ...')
            except IndexError:
                await access_login_page(response)
                await ip_check(session)
                await session.close()
                return 'Blocked'

        async with session.post(url + '/login', headers=headers_1, allow_redirects=True,
                                data=await data_set(token, user['username'], user['passwd'])
                                ) as response:
            response = await response.text()
            access = await check_access(response, user['username'])
            if access is False:
                await session.close()
                return False
            async with session.get(url, headers=headers_1) as res:
                res = await res.text()
                if user['username'] in res:
                    print('[+] Successful authorization')

        url_for_search = f'{DOMAIN}/search?query={query}'
        results = await search_shodan(session, url_for_search, verb_level, page)

        if verb_level is True and results is not False:
            tasks = []
            loop = asyncio.get_event_loop()
            for url in results:
                tasks.append(loop.create_task(verbose_level_info(session, url)))
            results = await asyncio.gather(*tasks)

        await session.close()
        return results


async def shodanus_main(args):
    """ Main function for run crawler in shodan """
    users = await read_file('users.json')
    if users is False:
        return False
    if len(users) < 1:
        return '[-] You have not added any user !'
    for user in users:
        try:
            session = await shodan(user, args.q, args.tor, args.vv, page=args.p)
        except ProxyConnectionError:
            print('[!] Tor Connection Error')

        if session == 'Blocked':
            break
        if session is False:
            continue
        if args.o is not None:
            await save_results(args.o, session)
            if args.i is True:
                return session
            return True
        return session
