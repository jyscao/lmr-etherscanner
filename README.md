# LMR Etherscanner

Prints the activities given a list of ERC20 wallet addresses, using the Etherscan REST API.



### Dependencies

* Python 3
* [requests](https://github.com/psf/requests)



### Required Data Files

The following files are expected to present at the root of the project (i.e. same directory as the `call-etherscan.py` script):

* `etherscan_api_keys.py`, containing a Python dictionary of the form:

```python
API_KEYS = {
    0: "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    1: "YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY",
    ...
}
```

* `wallet_addresses.py`, containing a Python dictionary of the form:

```python
WALLET_ADDRS = {
    "John Smith": "0x1111111111111111111111111111111111111111",
    "Jane Doe":   "0x2222222222222222222222222222222222222222",
    ...
}
```



### Run

* Simply run `./call-etherscan.py` to check all LMR tokens (the default) sent from your list of ERC20 addresses.

* Use `./call-etherscan.py -h` to see all available options, including all supported tokens.



### Adding Tokens

Simply create a new kv-pair in the dictionary defined in `contract_addrs.py`.
