
import argparse
import re
import toml
import os
import pprint
from pathlib import Path

from typing import MutableMapping, Any
import sys

from tx_engine import Wallet, create_wallet_from_pem_bytes

# Specify the directory path
# path = r'/app/data'
# set directory path to the environment variable or default to /app/data
if 'DATA_PATH' in os.environ:
    path = os.environ['DATA_PATH']
else:
    path = '/app/data'


# -------------------------------------------------------------------
#  Helper function for checking address format using regex
def address_regex_type(arg_value, pat=re.compile(r"[a-zA-Z1-9]{27,35}$")):
    if not pat.match(arg_value):
        raise argparse.ArgumentTypeError("invalid value")
    return arg_value


# -------------------------------------------------------------------
# Helper function for creating toml file
def write_to_file(filename, data_dict, is_toml=True):
    file = open(os.path.join(path, filename), "w")
    if is_toml:
        toml.dump(data_dict, file)
    else:
        file.write(data_dict)
    file.close()


# -------------------------------------------------------------------
# Helper function for writing to stdout
def write_to_stdout(data_dict, is_toml=True):
    print('\n')
    if is_toml:
        toml.dump(data_dict, sys.stdout)
    else:
        print(data_dict)
    print('\n')


# -------------------------------------------------------------------
# Helper function for reading toml file
def read_toml_file(filename):
    ret = {}
    the_file = Path(os.path.join(path, filename))
    if the_file.is_file():
        with open(the_file, 'r') as file:
            ret = toml.load(file)
    else:
        print(f"File: {the_file} not found, exiting...\n")
        exit(1)
    return ret


# -------------------------------------------------------------------
# Helper function for reading pem files
def read_pem_file(filename):
    ret: str = ""
    the_file = Path(os.path.join(path, filename))
    if the_file.is_file():
        with open(the_file, 'r') as file:
            ret = file.read()
    else:
        print(f"File: {the_file} not found, exiting...\n")
        exit(1)
    return ret


# -------------------------------------------------------------------
# Helper function to convert type to key_type
def network_to_key_type(network: str) -> str:
    match network:
        case "testnet":
            return "BSV_Testnet"

        case "mainnet":
            return "BSV_Mainnet"

        case "regtest":
            return "BSV_Testnet"

        case "mock":
            return "BSV_Testnet"

        case _:
            print(f"Invalid network type: {network}")
            exit(1)


# -------------------------------------------------------------------
# Helper function to build a tx_engine interface config for a network.
#
#   testnet / mainnet -> WhatsOnChain (woc) REST interface
#   regtest           -> local node over JSON-RPC (rpc); connection
#                        details come from the RPC_USER / RPC_PASSWORD /
#                        RPC_HOST environment variables, defaulting to the
#                        docker regtest node (bitcoin / bitcoin / node1:18332)
#   mock              -> in-memory mock interface (unit tests)
#
# regtest follows testnet consensus rules, so the interface network_type is
# reported as "testnet" (the woc/rpc interfaces map that to "test" internally).
def build_interface_config(network: str) -> MutableMapping[str, Any]:
    if network in ("testnet", "mainnet"):
        return {"interface_type": "woc", "network_type": network}
    if network == "mock":
        return {"interface_type": "mock", "network_type": "testnet"}
    if network == "regtest":
        return {
            "interface_type": "rpc",
            "network_type": "testnet",
            "user": os.environ.get("RPC_USER", "bitcoin"),
            "password": os.environ.get("RPC_PASSWORD", "bitcoin"),
            "address": os.environ.get("RPC_HOST", "node1:18332"),
        }
    print(f"Invalid network type: {network}")
    exit(1)


#  -------------------------------------------------------------------
# Helper function to add the interface routing to a generated param file.
# Only non-secret routing info (interface_type + network_type) is persisted;
# RPC credentials are injected from the environment at broadcast time
# (see transaction.broadcast_tx).
def add_interface_to_config(config: MutableMapping[str, Any], network: str) -> None:
    iface = build_interface_config(network)
    config['interface'] = {
        'interface_type': iface['interface_type'],
        'network_type': iface['network_type'],
    }


# -------------------------------------------------------------------
def print_config(config: MutableMapping[str, Any]) -> None:
    print('<----------------------------------------------------------->')
    print("Config:")
    pprint.pprint(config)
    print('<------------------------------------------------------------>\n')


def print_amounts(amt_total_out: int, amt_total_in: int, fee: int, ret_amt: int) -> None:
    print('\n------------------------------------------------------------------------------------')
    print("Amounts:" + "\n\tAmount In: \t" + str(amt_total_in) + "\n\tAmount Out: \t" + str(amt_total_out) + "\n\tFee: \t\t" + str(fee) + "\n\tChange: \t" + str(ret_amt))
    print('------------------------------------------------------------------------------------\n')


# -------------------------------------------------------------------
# Helper function to load private key from file
def load_key_from_file(filename: str, toml: bool, key_type: str) -> tuple[str, str]:
    try:
        if toml:
            key_info = read_toml_file(filename)
            ret = key_info['key_info']['private_key'], key_info['key_info']['bitcoin_address']
        # else deal with pem format
        else:
            key_str = read_pem_file(filename)
            key_as_bytes = key_str.encode()
            key_wallet = create_wallet_from_pem_bytes(key_as_bytes, network=key_type)
            address = key_wallet.get_address()
            private_key = key_wallet.to_wif()

            ret = (private_key, address)
        return ret
    except FileNotFoundError:
        print(f"Error: File {filename} not found.")
    except KeyError as e:
        print(f"Error: Missing key {e} in the file {filename}.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}.  Check filetype and contents.")
    exit(1)


# -------------------------------------------------------------------
# Helper function to list keys
def list_keys(network):

    list_of_keys_from_keyfile = []
    list_of_keys_from_pemfile = []

    print(f"Looking for keys in {path} directory...")
    for file in os.listdir(path=path):
        print(f"Checking file: {file}")
        if file.endswith(".key"):
            data_dict = read_toml_file(file)
            if 'key_info' in data_dict:

                # create a "Wallet" object and check the network matches
                key = Wallet(data_dict["key_info"]["private_key"])
                key_network = key.get_network()
                if key_network == "BSV_Mainnet":
                    network_type = "mainnet"
                elif key_network == "BSV_Testnet":
                    network_type = "testnet"
                else:
                    print(f"Error: Invalid network type: {key_network}")
                    exit(1)

                if network == 'regtest':
                    network = 'testnet'
                if network_type == network:
                    list_of_keys_from_keyfile.append((file, data_dict["key_info"]["bitcoin_address"]))

    for file in os.listdir(path=path):
        if file.endswith(".pem"):
            key_type = network_to_key_type(network)
            key = load_key_from_file(file, False, key_type)
            list_of_keys_from_pemfile.append((file, key[1]))

    return list_of_keys_from_keyfile, list_of_keys_from_pemfile


# -------------------------------------------------------------------
# Helper function to print all keys
def print_keys(network):
    key_list, pem_list = list_keys(network=network)
    print('\n------------------------------------------------------------------------------------')
    print('WIF format keys ( .key ) in the data directory:')
    for key in key_list:
        print(f'\n    * {key[0]}')
        print(f'      -> bitcoin address: {key[1]}')
    print('------------------------------------------------------------------------------------\n')

    print('\n------------------------------------------------------------------------------------')
    print('\nPem format keys ( .pem ) in the data directory:')
    for key in pem_list:
        print(f'\n    * {key[0]}')
        print(f'      -> bitcoin address: {key[1]}')
    print('------------------------------------------------------------------------------------\n')
    return
