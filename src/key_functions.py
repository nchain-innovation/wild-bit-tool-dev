import hashlib
import pprint
import os
from useful import network_to_key_type

# # Specify the directory path
# path = r'/app/data'

# set directory path to the environment variable or default to /app/data
if 'DATA_PATH' in os.environ:
    path = os.environ['DATA_PATH']
else:
    path = '/app/data'


from tx_engine.tx.bsv_factory import (bsv_factory, BSVClient)
from tx_engine.engine.keys import (PrivateKey, key_to_wif, wif_to_key)
from useful import set_regtest_config


def generate_key(nameSeed, nonce, network='testnet', pem=False):

    dk = hashlib.pbkdf2_hmac('sha256', nameSeed.encode('utf-8'), nonce.encode('utf-8'), 100000)

    key_type = network_to_key_type(network)
    myPrivKey = PrivateKey.from_int(int(dk.hex(), 16), network=key_type)
    if pem:
        return (myPrivKey.to_pem())
    else:
        return  {'key_info': 
                    {'private_key': key_to_wif(myPrivKey), 
                    'bitcoin_address': myPrivKey.address
                    }
                }


# get balance for address, network
# return balance
def balance(address, network):

    config = {"type":network}

    # if network is running in docker, aka in-a-sandbox 
    if config['type'] == 'insandbox':
        set_regtest_config(config)


    bsv_client = bsv_factory.set_config(config)

    test_balance = bsv_client.get_balance(address)
    print('\n------------------------------------------------------------------------------------')
    print('PubKey: \t{}\nBalance: \t{}'.format(address, test_balance))
    print('------------------------------------------------------------------------------------\n')
    
    return test_balance


# get utxo for address, network
# return utxo
def utxo(address, network): 

    config = {"type":network}

    # if network is running in docker, aka in-a-sandbox
    if config['type'] == 'insandbox':
        set_regtest_config(config)


    bsv_client = bsv_factory.set_config(config)

    unspent = bsv_client.get_utxo(address)
    print('\n<-------------------------------------------------------->\n')
    print(f"Unspent UTXOs: \t{unspent}")
    print('\n<-------------------------------------------------------->\n')
    print(type(unspent))
    
    pprint.pprint(unspent)
    return unspent

# get all utxo's for address, network
# return vin
def utxo_all(address, network):
    config = {"type":network}

    # if network is running in docker, aka in-a-sandbox
    if config['type'] == 'insandbox':
        set_regtest_config(config)
        
    bsv_client = bsv_factory.set_config(config)
    unspent = bsv_client.get_utxo(address)

    vin = []
    # i = 0
    for utxo in unspent:
        vin.append(utxo)

    return vin

# get uxto for a certain amount
# return utxo
def utxo_amount(address, network, amount): 

    config = {"type":network}

    # if network is running in docker, aka in-a-sandbox
    if config['type'] == 'insandbox':
        set_regtest_config(config)


    bsv_client = bsv_factory.set_config(config)
    unspent = bsv_client.get_utxo(address)

    sum = 0
    vin = []
    i = 0
    while sum < amount:
        sum += unspent[i]['value']
        vin.append(unspent[i])
        i += 1

    return vin