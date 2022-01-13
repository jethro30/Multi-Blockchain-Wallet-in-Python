#import subprocess
import json
from constants import *
from dotenv import load_dotenv
import os
from web3 import Web3
from eth_account import Account
from bit import wif_to_key
load_dotenv()
from bit import PrivateKeyTestnet
from bit.network import NetworkAPI
from web3.auto.gethdev import w3
from web3.middleware import geth_poa_middleware

mnemonic = os.getenv('mnemonic')

def derive_wallets(coin):
    command = f'./derive -g --mnemonic="{mnemonic}" --cols=path,address,privkey,pubkey --format=json --coin="{coin}" --numderive= 2'
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    p_status = p.wait()
    keys = json.loads(output)
    return keys
  
coins = {
    ETH: derive_wallets(ETH),
    BTCTEST: derive_wallets(BTCTEST)
}
print(coins)

INDEX = 0

#print(coins[BTCTEST][0]['privkey'])

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
#print(w3.eth.blockNumber)

#print(w3.eth.getBalance(""))

def priv_key_to_account(coin, priv_key):
    if coin == ETH:
        return Account.privateKeyToAccount(priv_key)
    elif coin == BTCTEST:
        return PrivateKeyTestnet(priv_key)


def create_tx(coin, account, to, amount):
    if coin == ETH:
        gasEstimate = w3.eth.estimateGas(
            {"from": account.address, "to": to, "value": amount}
        )
        return {
            "from": account.address,
            "to": to,
            "value": amount,
            "gasPrice": w3.eth.gasPrice,
            "gas": gasEstimate,
            "nonce": w3.eth.getTransactionCount(account.address),
            #"chainID": web3.eth.chainId
        }
    elif coin == BTCTEST:
        return PrivateKeyTestnet.prepare_transaction(account.address, [(to, amount, BTC)])

def send_tx(coin, account, to, amount):
    tx = create_tx(coin, account, to, amount)
    signed_tx = account.sign_transaction(tx)
    if coin == ETH:
        return w3.eth.sendRawTransaction(signed.rawTransaction)
    elif coin == BTCTEST:
        return NetworkAPI.broadcast_tx_testnet(signed_tx)

Account_one = priv_key_to_account(BTCTEST, coins[BTCTEST][0]['privkey'])

#print(Account_one)
#print(coins[BTCTEST][0]['address'])
print(coins[BTCTEST][1]['privkey'])

# insert private key here
key = wif_to_key(os.getenv('keys'))
key2 = wif_to_key(os.getenv('keys2'))

address_two= coins[BTCTEST][1]['address']

#send_tx(BTCTEST, Account_one, address_two, 0.002)

print(key.get_balance("btc"))
print(key.balance_as("usd"))
#print(key.get_transactions())
#print(key.get_unspents())
print(key2.get_balance("btc"))
print(key2.balance_as("usd"))
#print(key2.get_transactions())
#print(key2.get_unspents())

