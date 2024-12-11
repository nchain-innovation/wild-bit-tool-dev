from useful import network_to_key_type, load_key_from_file
from transaction import build_tx, broadcast_tx

from useful import write_to_file, write_to_stdout, add_interface_to_config
# from key_functions import set_regtest_config

from tx_engine import interface_factory
from typing import Any, Dict


class TransactionCommand:
    def __init__(self, paramfile=None,
                 genparam=False,
                 out=None,
                 broadcast='true',
                 network='testnet',
                 amount=None,
                 sender=None,
                 sender_key=None,
                 inform='toml',
                 fee=300,
                 recipient=None,
                 change=None):

        self.paramfile = paramfile
        self.genparam = genparam
        self.out = out
        self.broadcast = broadcast
        self.network = network
        self.amount = amount
        self.sender = sender
        self.sender_key = sender_key
        self.inform = inform
        self.fee = fee
        self.recipient = recipient
        self.change = change
        self.key_type = network_to_key_type(self.network)

        # if network is running in docker, aka in-a-sandbox
        if network == 'regtest':
            print("JAS: NOT IMPLEMENTED YET")
            raise NotImplementedError

        if self.network == "mock":
            config = {
                "interface_type": "mock",
                "network_type": self.network
            }
        else:
            config = {
                "interface_type": "woc",
                "network_type": self.network,
            }

        self.interface = interface_factory.set_config(config)

    # --------------------------------------------------------------
    # Create transaction from input file
    def create_transaction(self):
        print(f'\n  -> Running bbt transaction,   input file={self.paramfile}, network={self.network}')

        # print("JAS: DEBUG: config: ", self.config)
        tx = None

        # Build transaction
        try:
            tx = build_tx(self.paramfile)
        except KeyError as e:
            print(f"Error: Missing key: {e} in the parameter file:  '{self.paramfile}'. Please check the file and try again.")
            exit(1)
        except ValueError as e:
            print(f"Error: {e} Please check the parameter file: '{self.paramfile}' and try again.")
            exit(1)

        print(f'Serialised Transaction: \n\n{tx}')

        # Ready to broadcast transaction
        if self.broadcast == 'true':
            print('\nBroadcasting transaction')
            broadcast_tx(tx, self.paramfile)
        else:
            print('\nNot broadcasting transaction')

    # --------------------------------------------------------------
    # Get UTXO's for an amount
    def utxo_amount(self, address, amount):
        unspent = self.interface.get_utxo(address)
        sum = 0
        vin = []
        i = 0
        while sum < amount:
            sum += unspent[i]['value']
            vin.append(unspent[i])
            i += 1

        return vin

    # --------------------------------------------------------------
    def find_inputs(self, data_dict):
        key_for_signing = "<key for signing>"
        if self.sender_key:
            toml_ = True
            if (self.inform == 'pem'):
                toml_ = False

            key_type = network_to_key_type(self.network)
            key_for_signing, sender_address = load_key_from_file(self.sender_key, toml_, key_type)
            # print(f"JAS: DEBUG: key_for_signing: {key_for_signing}, sender_address: {sender_address}")
            self.sender = sender_address

        elif self.sender:
            sender_address = self.sender

        # get balance for the sender
        # sb = self.bsv_client.get_balance(sender_address)
        sb = self.interface.get_balance(sender_address)
        sender_balance = int(sb['confirmed']) + int(sb['unconfirmed'])

        # check if sender has enough balance to send amount
        amount_and_fee = int(self.amount) + int(self.fee)
        if sender_balance < amount_and_fee:
            print(f'Error: sender balance: {sender_balance} is less than amount + fee: {amount_and_fee}')
            exit(1)

        # get utxo for sender
        sender_utxo = self.utxo_amount(sender_address, amount_and_fee)

        # create transaction inputs (vin)
        data_dict['transactioninput'] = []

        for utxo in sender_utxo:
            data_dict['transactioninput'].append({
                'tx_hash': utxo['tx_hash'],
                'tx_pos': utxo['tx_pos'],
                'amount': utxo['value'],
                'private_key_for_signing': key_for_signing
            })

    # --------------------------------------------------------------
    # Generate transaction parameters
    def generate_parameters(self):
        print('Generating parameters')
        data_dict: Dict[Any, Any] = {}
        # add network type to config
        # add_network_type_to_config(data_dict, self.network)
        add_interface_to_config(data_dict, self.network)
        # print("JAS: DEBUG: data_dict: ", data_dict)

        if self.sender:
            sender_address = self.sender
        else:
            sender_address = "<sender address>"

        # find UTXO's for sender
        if self.amount and (self.sender or self.sender_key):
            self.find_inputs(data_dict)

        # if receiver is specified, create transaction outputs (vout)
        if self.recipient:
            data_dict['transactionoutput'] = []
            data_dict['transactionoutput'].append({
                'public_key': self.recipient,
                'amount': self.amount,
                'op_return': False,
                'data_to_encode': ''
            })

        # if change address is specified, create change output
        if self.change:
            data_dict['tx_info'] = {}
            data_dict['tx_info']['create_change_output'] = True
            data_dict['tx_info']['change_output_public_key'] = self.change

        # else pay change back to sender
        else:
            data_dict['tx_info'] = {}
            data_dict['tx_info']['create_change_output'] = True
            data_dict['tx_info']['change_output_public_key'] = sender_address

        # add fee
        data_dict['tx_info']['tx_default_fee'] = self.fee

        # write to file or stdout; default is stdout
        if self.out:
            write_to_file(self.out, data_dict)
            print(f'Parameters generated, saved to file: {self.out}')
        else:
            write_to_stdout(data_dict)

    # --------------------------------------------------------------
    # Run the command
    def run(self):
        # if parameter file is provided, use this to create transaction
        if self.paramfile:
            self.create_transaction()

        # generate parameter file from command line parameters
        elif self.genparam:
            self.generate_parameters()

        else:
            print('Error: input file or parameters required to generate transaction')
            print('Use -h or --help for help')
            exit(1)
