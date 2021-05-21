from datetime import datetime

import argparse
import requests
import time
import os


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

    opened = False

    os.system('clear')
    while True:
        print('=' * 80)
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        execute_it = False

        # price retrieval from binance
        symbol = f'{currency}{fiat}'
        response = requests.get(f'https://api.binance.com/api/v3/ticker/bookTicker?symbol={symbol}')
        bid = response.json()['bidPrice']
        ask = response.json()['askPrice']
        price = round((float(bid) + float(ask)) / 2.0, 2)

        if less_than is not None:
            if price < less_than and opened:
                execute_it = True
                opened = False
            if price > less_than and not opened:
                opened = True

        elif greater_than is not None:
            if price > greater_than and opened:
                execute_it = True
                opened = False
            if price < greater_than and not opened:
                opened = True

        welcome_msg = f'- Listening to {fiat} price of {currency}.\n'
        if less_than is not None:
            welcome_msg += f'- If price falls below {less_than}, '
        elif greater_than is not None:
            welcome_msg += f'- If price grow above {greater_than}, '
        welcome_msg += f'command "{command}" will be executed.\n'
        if not opened and not execute_it:
            if less_than is not None:
                welcome_msg += f'- Price currently is lesser than {less_than} so doing nothing. ' \
                               f'Previously need to reach higher values, above {less_than}'
            elif greater_than is not None:
                welcome_msg += f'- Price currently is greater than {greater_than} so doing nothing. ' \
                               f'Previously need to reach lower values, below {greater_than}'

        print(f'[{now}]')
        print(welcome_msg)
        print(f'Current price: {price}')

        if execute_it:
            os.system(command)

        print(f'Waiting {interval} seconds to refetch ...')
        time.sleep(interval)


if __name__ == '__main__':
    main()
