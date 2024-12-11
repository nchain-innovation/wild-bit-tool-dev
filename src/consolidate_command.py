from useful import add_network_type_to_config, load_key_from_file, write_to_file, write_to_stdout
from key_functions import balance, utxo_all
from typing import Dict, Any


class ConsolidateCommand:

    def __init__(self,
                 sender_key,
                 sender,
                 network,
                 fee,
                 inform,
                 out):

        self.sender_key = sender_key
        self.sender = sender
        self.fee = fee
        self.inform = inform
        self.out = out

        if network == 'regtest':
            self.network = 'insandbox'
            self.key_type = 'test'
        elif network == 'mainnet':
            self.key_type = 'main'
        elif network == 'testnet':
            self.key_type = 'test'
        elif network == 'mock':
            self.key_type = 'test'
        else:
            print(f"Invalid network type: {network}")
            exit(1)

    def run(self):
        print(f'\n  -> Running bbt consolidate,   network={self.network}')
        data_dict: Dict[Any, Any] = {}
        # add network type to config
        add_network_type_to_config(data_dict, self.network)

        if self.sender:
            sender_address = self.sender
        else:
            sender_address = "<sender address>"

        key_for_signing = "<key for signing>"

        # get address from sender_key
        if self.sender_key:
            toml_ = True
            if (self.inform == 'pem'):
                toml_ = False

            key_for_signing, sender_address = load_key_from_file(self.sender_key, toml_, self.key_type)

        # get balance for the sender
        sender_balance = balance(sender_address, self.network)
        sender_balance = int(sender_balance['confirmed'] + sender_balance['unconfirmed'])
        # should check the balance covers the fee
        amount = sender_balance - self.fee
        if sender_balance <= amount:
            print(f"Error: not enough funds to cover fee of {self.fee}")
            exit(1)

        sender_utxo = utxo_all(sender_address, self.network)

        # create transaction inputs (vin)
        data_dict['transactioninput'] = []

        for utxo in sender_utxo:
            data_dict['transactioninput'].append({
                'tx_hash': utxo['tx_hash'],
                'tx_pos': utxo['tx_pos'],
                'amount': utxo['value'],
                'private_key_for_signing': key_for_signing
            })

        # print out number of utxo's
        print(f"Number of utxo's: {len(sender_utxo)}")
        data_dict['transactionoutput'] = []
        data_dict['transactionoutput'].append({
            'public_key': sender_address,
            'amount': amount,
            'op_return': False,
            'data_to_encode': ''
        })

        # add fee
        data_dict['tx_info'] = {}
        data_dict['tx_info']['create_change_output'] = False
        data_dict['tx_info']['tx_default_fee'] = self.fee

        # write to file or stdout; default is stdout
        if self.out:
            write_to_file(self.out, data_dict)
            print(f'Parameters generated, saved to file: {self.out}')
        else:
            write_to_stdout(data_dict)
