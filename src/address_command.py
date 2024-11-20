from useful import network_to_key_type, load_key_from_file
# from tx_engine.engine.keys import wif_to_key
from tx_engine import Wallet

class AddressCommand:
    def __init__(self, private_key, network, input_file, inform):
        self.private_key = private_key
        self.network = network
        self.input_file = input_file
        self.inform = inform
        self.key_type = network_to_key_type(self.network)


    # Takes private key 
    # and writes out the public key (address)
    def private_key_to_public_key(self, private_key):
        try:
            # myPrivKey = wif_to_key(private_key, network=self.key_type)
            myPrivKey = Wallet(private_key)

            print('\n------------------------------------------------------------------------------------')
            print('Address (public key) \t-> ', myPrivKey.get_address())
            print('------------------------------------------------------------------------------------\n')
        
        except Exception as e:
            print(f"\nError: {e}")
            print(f"Failed to get address for private key: {private_key}, retry with correct private-key:network combination")
            exit(1)


    def run(self):
        # get the private key from the input file
        if self.input_file:
            toml_ = self.inform == 'toml'
            key = load_key_from_file(self.input_file, toml_, key_type=self.key_type)
            private_key = key[0]

        elif self.private_key:
            private_key = self.private_key

        else:
            print('Error: private key required to generate address')
            exit(1)

        print(f'\n  -> Running bbt address, private_key={private_key}, network={self.network}')

        self.private_key_to_public_key(private_key)

        

