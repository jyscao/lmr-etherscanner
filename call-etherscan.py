#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time, json, argparse
import requests

from contract_addrs import CONTRACT_ADDRS
from etherscan_api_keys import API_KEYS
from wallet_addresses import WALLET_ADDRS


parser = argparse.ArgumentParser()
parser.add_argument(
    "-t", "--token",
    action="store",
    dest="token",
    default="LMR",
    help=f"specify the token to check (default: LMR); accepted tickers: {', '.join(CONTRACT_ADDRS.keys())}",
)
parser.add_argument(
    "-s", "--sent",
    action="store_true",
    dest="sent",
    default=True,
    help="get sent transactions (this is the default)",
)
parser.add_argument(
    "-r", "--received",
    action="store_true",
    dest="received",
    default=False,
    help="get received transactions",
)

parsed_args = parser.parse_args()

def get_contract_addr(parsed_args):
    ticker = parsed_args.token 
    return ticker, CONTRACT_ADDRS[ticker]
TOKEN_TICKER, CONTRACT_ADDR = get_contract_addr(parsed_args)

def get_transaction_type(parsed_args):
    if parsed_args.received:
        return "to", "received"
    elif parsed_args.sent:
        return "from", "sent"
    else:
        raise Exception("this should never be reached!")
TRANSACTION_TYPE, TRANSACTION_DESC = get_transaction_type(parsed_args)

END_BLOCK = 1_000_000_000


def call_endpoint(addr: str, api_key):
    endpoint = f"https://api.etherscan.io/api?module=account&action=tokentx&contractaddress={CONTRACT_ADDR}&address={addr}&page=1&offset=100&startblock=0&endblock={END_BLOCK}&sort=desc&apikey={api_key}"
    try:
        r = requests.get(endpoint)
        if r.status_code == 200:
            result = json.loads(r.text)["result"]
            return get_out_txs(addr, result)
        else:
            print(f"request returned with {r.status_code}")
    except:
        raise Exception(f"API call failed")

def get_out_txs(addr, result_ls):
    out_txs = [res for res in result_ls if res[TRANSACTION_TYPE].lower() == addr.lower()]
    return [(format_timestamp(res["timeStamp"]), f"{int(res['value']) / (10 ** int(res['tokenDecimal']))}") for res in out_txs]

def format_timestamp(ts):
    time_display_format = "%b %d %Y, %H:%M"
    return time.strftime(time_display_format, time.localtime(int(ts)))


if __name__ == "__main__":
    n_keys = len(API_KEYS)
    for i, (person, wal_addr) in enumerate(WALLET_ADDRS.items(), start=1):
        if i % (5 * n_keys) == 0:   # etherscan API calls limit: 5 calls per sec (per key or per account?)
            time.sleep(1)
        out_vals = call_endpoint(wal_addr, API_KEYS[i % n_keys])
        print(f"{person} {TRANSACTION_DESC}:")
        for t, ov in out_vals:
            print(f"\t* {t} ➜ {ov} {TOKEN_TICKER}")
