from useful import load_key_from_file, set_regtest_config, list_keys, network_to_key_type
# from tx_engine.tx.bsv_factory import (bsv_factory, BSVClient)
from tx_engine import interface_factory, WoCInterface



class BalanceCommand:

    def __init__(self,
                 address=None,
                 network='testnet', # the underlying network, i.e. testnet, mainnet, regtest
                 input_file=None,
                 inform='toml',
                 all=False,
                 key_type=None): # type of key, i.e. testnet or mainnet
        
        self.address = address
        self.network = network
        self.input_file = input_file
        self.inform = inform
        self.all = all

        self.key_type = network_to_key_type(network)



    # get balance of a bitcoin address
    def get_balance(self):
        if self.address is None:
            print("Error: No address provided.")
            return

        # TODO: fix the regtest config

        config = {
            "interface_type": "woc",
            "network_type": self.network,
        }

        # if network is running in docker, aka in-a-sandbox
        # if config['type'] == 'insandbox':
            # set_regtest_config(config)
        
        interface = interface_factory.set_config(config)
        balance = interface.get_balance(self.address)
        return balance
    
    def print_balance(self):
        balance = self.get_balance()

        if balance is not None:
            print('\n------------------------------------------------------------------------------------')
            print('PubKey: \t{}\nBalance: \t{}'.format(self.address, balance))
            print('------------------------------------------------------------------------------------\n')
        else:
            print(f"Failed to retrieve balance for address {self.address}.")


    # get the address from the key file
    def load_key_from_file(self):

        toml_ = True
        if (self.inform == 'pem'):
            toml_ = False

        key = load_key_from_file(self.input_file, toml_, self.key_type)
        # self.address = key.get_address()
        self.address = key[1] 
        return


    def run(self):
        try:
            # Get the address from the input file
            if self.input_file:
                self.load_key_from_file()

            elif self.all:
                print(f'\n  -> Running bbt balance for all key files (.key|.pem), network={self.network}')
                key_list, pem_list = list_keys(network=self.network)
                key_bunch = BunchOfBalances(key_list, pem_list, self.network)
                key_bunch.check_balances()
                exit(0)
                
        except Exception as e:
            print(f'Caught Exception: {e}')
            exit(1)

        
        print (f'\n  -> Running bbt balance, address={self.address}, network={self.network}')
        self.print_balance()
        exit(0) 

# A class to handle many keys and pems
class BunchOfBalances():
    def __init__(self, keys, pems, network):
        self.key_name_list = keys
        self.pem_name_list = pems

        self.resource_balances = []

        for key in self.key_name_list:
            resource = BalanceCommand(
                address=key[1],
                input_file=key[0],
                network=network,
                inform='toml')
            
            self.resource_balances.append(resource)
            
        for pem in self.pem_name_list:
            resource = BalanceCommand(
                address=pem[1],
                input_file=pem[0],
                network=network,
                inform='pem')
            
            self.resource_balances.append(resource)
            

    def check_balances(self):

        for resource in self.resource_balances:
            print(f'\n    * {resource.input_file}')
            resource.print_balance()

        return
    
  


