from useful import load_key_from_file
from tx_engine import Wallet


class PkeyformatCommand:

    def __init__(self,
                 pkey,
                 input_file,
                 inform,
                 from_format,
                 to_format,
                 network):
        self.private_key = pkey
        self.input_file = input_file
        self.inform = inform
        self.from_format = from_format
        self.to_format = to_format
        self.network = network

        if network == 'regtest':
            self.network = 'insandbox'
            self.key_type = 'test'
        elif network == 'mainnet':
            self.key_type = 'BSV_Mainnet'
        elif network == 'testnet':
            self.key_type = 'BSV_Testnet'
        elif network == 'mock':
            self.key_type = 'test'
        else:
            print(f"Invalid network type: {network}")
            exit(1)

    # Takes private key and formats it to the desired format
    def format_key(self, private_key):
        in_format = self.from_format
        out_format = self.to_format
        print(f'     Converting private key from {in_format} to {out_format} format')
        try:
            # convert private key to different formats
            if in_format == 'wif':
                myPrivKey = Wallet(private_key)
            elif in_format == 'hex':
                myPrivKey = Wallet.from_hexstr(self.key_type, private_key)
            elif in_format == 'int':
                myPrivKey = Wallet.from_int(self.key_type, int(private_key))

        except Exception as e:
            print(f"\nError: {e}")
            print(f"Failed to get address for private key: {private_key}, check arguments and retry")
            exit(1)

        if out_format == 'wif':
            print('\n------------------------------------------------------------------------------------')
            print('Private Key (wif) \t-> ', myPrivKey.to_wif())
            print('------------------------------------------------------------------------------------\n')

            # print( key_to_wif(myPrivKey) )
        elif out_format == 'hex':
            print('\n------------------------------------------------------------------------------------')
            print('Private Key (hex) \t-> ', myPrivKey.to_hex())
            print('------------------------------------------------------------------------------------\n')

        elif out_format == 'int':
            print('\n------------------------------------------------------------------------------------')
            print('Private Key (int) \t-> ', myPrivKey.to_int())
            print('------------------------------------------------------------------------------------\n')

        else:
            print(f"Error: Invalid format {out_format}")
            exit(1)

    def run(self):
        try:
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

            print(f'\n  -> Running bbt pkeyformat, private_key={private_key}')
            self.format_key(private_key)

        except Exception as e:
            print(f"An error occurred: {e}")

        exit(0)
