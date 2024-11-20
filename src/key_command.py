from useful import write_to_file, write_to_stdout, read_file, print_keys
from key_functions import generate_key
import os

# set directory path to the environment variable or default to /app/data
if 'DATA_PATH' in os.environ:
    path = os.environ['DATA_PATH']
else:
    path = '/app/data'


class KeyCommand:
    def __init__(self, 
                 seed=None, 
                 nonce=None, 
                 output_file=None, 
                 param_file=None, 
                 genparam=None,
                 outform='toml', 
                 list_all=None,
                 network='testnet'):
        
        self.seed = seed
        self.nonce = nonce
        self.output_file = output_file
        self.param_file = param_file
        self.genparam = genparam
        self.outform = outform
        self.list_all = list_all
        self.network = network
        
    # generate parameters from seed and nonce
    def generate_parameters(self):
        # check if seed and nonce are provided
        if self.seed and self.nonce:
            data_dict = {
                "key_input": {
                    "seed": self.seed,
                    "nonce": self.nonce
                }
            }
        else:
            print('Error: seed and nonce required to generate parameters')
            exit(1)

        if self.output_file:
            if self.outform != "toml":
                print(f"Error: {self.outform} format not supported for parameter file, use 'toml'. Exiting...\n")
                exit(1)
            else:
                write_to_file(self.output_file, data_dict, True)
        else:
            toml = False
            if self.outform == "toml":
                toml = True
            write_to_stdout(data_dict, toml)
        return


    # generate key from seed and nonce
    def generate_key(self):

        # check if a parameter file is provided
        if self.param_file:

            # read parameter file
            data_dict = read_file(self.param_file)

            if 'key_input' in data_dict:
                # check if seed and nonce are provided
                if 'seed' in data_dict['key_input'] and 'nonce' in data_dict['key_input']:
                    self.seed = data_dict['key_input']['seed']
                    self.nonce = data_dict['key_input']['nonce']
                else:
                    print(f'Error: seed and nonce required to generate key, not found in {self.param_file} file. Exiting...\n')
                    exit(1)

            else:
                print(f'Error: key_input not found in {self.param_file} file. Exiting...\n')
                exit(1)

        pem = self.outform == 'pem'

        print (f'\n  -> Running bbt key, seed={self.seed}, nonce={self.nonce}, network={self.network}')
        key = generate_key(self.seed, self.nonce, network=self.network, pem=pem)

        # write to file or stdout; default is stdout
        # format is toml unless pem is specified  
        is_toml = not pem

        if self.output_file:
            print (f"writing to file {self.output_file}")
            write_to_file(self.output_file, key, is_toml)
        else:
            write_to_stdout(key, is_toml)
        return


    def run(self):
        # generate parameter file from command line parameters
        if self.genparam:
            self.generate_parameters()
            exit(0)

        # generate key from parameter file
        elif self.param_file or (self.seed and self.nonce):
            self.generate_key()
            exit(0)
       
        # list all keys
        elif self.list_all:
            print (f'\n  -> Running bbt key, list all, network={self.network}')
        
            print_keys(network=self.network)
            exit(0)

        else:
            print ("Error: seed and nonce required to generate key")
            exit(1)
