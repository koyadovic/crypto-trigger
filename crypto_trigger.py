import argparse
import os
import sys
import time
from datetime import datetime

import requests


parser = argparse.ArgumentParser(description='Trigger command after crypto market reach some specific condition.')
parser.add_argument('-c', '--currency', type=str, required=True, help='Target crypto asset for the price checking')
parser.add_argument('-f', '--fiat', type=str, required=True, help='Fiat used to check the price')
parser.add_argument('--gt', type=float, help='Greater-than condition. '
                                             'If price goes above of this value, command will be triggered')
parser.add_argument('--lt', type=float, help='Less-than condition. '
                                             'If price goes below of this value, command will be triggered')
parser.add_argument('-i', '--interval', type=int, required=False, default=60,
                    help='Defaults to 60 seconds between every check')
parser.add_argument('command', help='command for the execution')


def main():
    args = parser.parse_args()
    if (args.gt is None and args.lt is None) or (args.gt is not None and args.lt is not None):
        raise Exception('Must specify a --gt or --lt parameter')

    command = args.command
    less_than = args.lt
    greater_than = args.gt
    currency = args.currency
    fiat = args.fiat
    interval = args.interval

    welcome_msg = f'Listening to {fiat} price of {currency}.'
    if less_than is not None:
        welcome_msg += f' If price falls below {less_than}, '
    if greater_than is not None:
        welcome_msg += f' If price grow above {greater_than}, '

    welcome_msg += f'command "{command}" will be executed'

    opened = False

    while True:
        os.system('clear')

        now = datetime.utcnow()

        symbol = f'{currency}{fiat}'
        response = requests.get(f'https://api.binance.com/api/v3/ticker/bookTicker?symbol={symbol}')
        bid = response.json()['bidPrice']
        ask = response.json()['askPrice']

        price = round((float(bid) + float(ask)) / 2.0, 2)
        print(f'[{now}]')
        print(welcome_msg)
        print(f'Current price: {price}')
        if less_than is not None:
            if price < less_than and opened:
                os.system(command)
                opened = False
            if price > less_than and not opened:
                opened = True

        if greater_than is not None:
            if price > greater_than and opened:
                os.system(command)
                opened = False
            if price < less_than and not opened:
                opened = True

        time.sleep(interval)


if __name__ == '__main__':
    main()
