""" This is the main function that runs the script.
    installation and launch are described in file README.
    It is a freeware program that anyone can use !
    author: @vomanc
    version 1.0
"""
import argparse
import asyncio
import pprint
import logging
from site_shodan import shodanus_main
from inter_mode import interactive_mode
from extension import banner


def init_logger():
    """ Set logger """
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(filename='shodanus.log', mode='a')
    filt = [
        '%(asctime)s', '%(levelname)s', '%(filename)s', '%(lineno)s',
        '%(name)s', '%(module)s', '%(message)s'
        ]
    forma = ' - '.join(filt)
    formatter = logging.Formatter(forma)
    handler.setFormatter(formatter)
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)


def argument_parser():
    """ Setting options for the program  """
    parser = argparse.ArgumentParser(
        prog=f'shodanus, version: {VERSION}',
        description='Script to interact with shodan.',
        add_help=True
    )
    parser.add_argument(
        '-q', '-query',
        type=str,
        required=True,
        help='Search query, example:([product:"apache"] or ["product:apache country:us"]'
    )
    parser.add_argument(
        '-i',
        action='store_true',
        help='Interactive mode for working after parsing'
    )
    parser.add_argument(
        '--tor',
        action='store_true',
        help='Use TOR (required: apt install tor)'
    )
    parser.add_argument(
        '--vv',
        action='store_true',
        help='Increase verbosity level'
    )
    parser.add_argument(
        '-o',
        type=str,
        help='Save file'
    )
    parser.add_argument(
        '-p', '-page',
        type=int,
        default=1,
        help='Number of pages to parse [default: 1]'
    )
    parser.add_argument(
        '-v', '-version',
        action='version', version=f'shodanus, version: {VERSION}',
        help='Print version number'
    )

    return parser


async def main(parser):
    """ Main function that starts the program """
    args = parser.parse_args()
    results = await shodanus_main(args)
    if results is None:
        print('[!] No results')
    elif results is False:
        print('[!] Error')
    else:
        if args.i is True:
            interactive_mode(results)
        else:
            pprint.pprint(results)


if __name__ == "__main__":
    VERSION = '1.0'
    logger = logging.getLogger('app')
    print(banner)
    init_logger()
    logger.debug('start')
    try:
        asyncio.run(main(argument_parser()))
        logger.debug('Successfully wrote')
    except Exception:
        logger.exception("Error message")
