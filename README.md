# Crypto Trigger
```
$ python crypto_trigger.py -h
usage: crypto_trigger.py [-h] -c CURRENCY -f FIAT [--gt GT] [--lt LT]
                         [-i INTERVAL]
                         command

Trigger command after crypto market reach some specific condition.

positional arguments:
  command               command for the execution

optional arguments:
  -h, --help            show this help message and exit
  -c CURRENCY, --currency CURRENCY
                        Target crypto asset for the price checking
  -f FIAT, --fiat FIAT  Fiat used to check the price
  --gt GT               Greater-than condition. If price goes above of this
                        value, command will be triggered
  --lt LT               Less-than condition. If price goes below of this
                        value, command will be triggered
  -i INTERVAL, --interval INTERVAL
                        Defaults to 60 seconds between every check
```

# Examples
Execute `panic.sh` when Bitcoin price falls below $30000:
```
python crypto_trigger.py --currency BTC --fiat USDT --lt 30000 "./panic.sh"
```

Execute `buy_everything_in_the_world.sh` when Bitcoin price raise above $32000:
```
python crypto_trigger.py --currency BTC --fiat USDT --gt 32000 "./buy_everything_in_the_world.sh"
```
