""" This script to work in interactive mode """
import pprint


HELP_TEXT = '''Examples:
        [a: all results], [{1}: info for index 1], [h: help], [q: quit] \t
        [c: components], [s: all hostname],
        [{0} p: {host index} {open ports}], [{1} v: {host index} {vulnerabilities lsit}]
        '''


def get_key(results, k=False, print_type=False):
    """ Output of basic commands """
    for i, item in enumerate(results):
        if k is not False and print_type is False:
            print(f'{i})', item[k], '\n', '_'*10)
        elif k is not False and print_type is True:
            try:
                pprint.pprint(item[k])
            except KeyError:
                print('[-] Run parser with key: --vv')
                break
        else:
            print('Index:', i)
            pprint.pprint(item)
            print('_'*10)


def if_key_is_num(inp, results):
    """ Output for verbose mode """
    if len(inp) >= 3 and ' ' in inp:
        inp, k = inp.split(' ')
        if k in {'p', 'v'}:
            k = {
                "p": "ports",
                "v": "vuln",
                }.get(k, False)
        else:
            inp = k = False
    else:
        k = False

    try:
        if inp is not False:
            inp = int(inp)
    except ValueError:
        inp = False

    if inp is not False and k is False:
        try:
            pprint.pprint(results[inp])
        except IndexError:
            print(f'[!] Last record index is {len(results) - 1}')
    elif inp is not False and k == 'ports' or k == 'vuln':
        if results[inp][k] == 'None':
            print(results[inp][k])
        else:
            pprint.pprint([i.replace('\n', '') for i in results[inp][k]])
    else:
        print('[!] No such key !')
        print(HELP_TEXT)


def interactive_mode(results):
    """ Main function processing the result of parsing """
    def query(inp):
        # Command filter
        if inp == 'a':
            get_key(results, print_type=True)
        elif inp == 's':
            get_key(results, 'hostname')
        elif inp == 'c':
            get_key(results, 'components')
        elif inp == 'h':
            print(HELP_TEXT)
        else:
            try:
                if_key_is_num(inp, results)
            except IndexError:
                print(f'[!] Last record index is {len(results) - 1}')
            except KeyError:
                print('[!] Run parser with key [--vv] to use this')
    print(HELP_TEXT)
    while True:
        try:
            inp = input('> ')
            if inp == 'q':
                break
            query(inp)
        except KeyboardInterrupt:
            break
