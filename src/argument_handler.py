import argparse
import sys

from typing import MutableMapping, Any

from key_command import KeyCommand
from balance_command import BalanceCommand
from address_command import AddressCommand
from consolidate_command import ConsolidateCommand
from transaction_command import TransactionCommand
from pkeyformat_command import PkeyformatCommand
from useful import address_regex_type



# Specify the directory path
path = r'/app/data'

# -------------------------------------------------------------------
# -------------------------------------------------------------------
class ArgumentHandler(object):

    def __init__(self):
        parser = argparse.ArgumentParser(
            prog="bbt.sh",
            description='WildBitTool',
            usage='''./wbt.sh <command> [<args>]

The most commonly used WildBitTool commands are:
   key          Generates a key from a seed and nonce
   balance      Get the balance of a bitcoin address
   address      Get the bitcoin address of a private key
   transaction  Create a transaction
   pkeyformat   Convert a private key to and from different formats
   consolidate  Consolidate UTXOs (many inputs to one output)
''')
        parser.add_argument('command', help='Subcommand to run')
        
        # parse_args defaults to [1:] for args
        # exclude the rest of the args or validation will fail
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print ('Unrecognized command')
            parser.print_help()
            exit(1)

        # use dispatch pattern to invoke method with same name
        getattr(self, args.command)()


    # -------------------------------------------------------------------
    # key: this is a sub-command
    #          - generate parameter file
    #          - generate key from parameter file
    #          - generate key from seed and nonce
    def key(self):
        parser = argparse.ArgumentParser(
            prog="bbt.sh",
            description='Generates a key from a seed and nonce',
            usage='''./bbt.sh <key> [-s <seed>] [-n <nonce>] [-out <output file>] \
                [-paramfile <parameter file>] [-genparam] \
                [-outform <toml|pem>] 
                [-l]\
                [--network <mainnet|testnet|regtest>]
            
Example commands: 
    key -s "my seed" -n "my nonce"                                  # create key from seed and nonce, output to stdout
    key -s "my seed" -n "my nonce" -out my_key.txt                  # create key from seed and nonce, output to file
    key -genparam -s "my seed" -n "my nonce"                        # generate parameters, output to stdout
    key -genparam -s "my seed" -n "my nonce" -out myparamfile.toml  # generate parameters, save to file
    key -paramfile myparamfile.toml                                 # create key from parameter file, output to stdout
    key -paramfile myparamfile.toml -out my_key.txt                 # create key from parameter file, save to file
''')
            
        
        parser.add_argument("-s", "--seed", help="seed phrase used to generate private key")
        parser.add_argument("-n", "--nonce", help="nonce: number used once, feeds into private key generation")
        parser.add_argument("-out", help="output file")
        parser.add_argument("-paramfile", help="parameter file for key generation")
        parser.add_argument("-genparam", help="generate parameters", action="store_true")
        parser.add_argument("-outform", help="output file format", choices=['toml', 'pem'], default='toml')
        parser.add_argument("-l", "--list", help="list all keys", action="store_true")
        parser.add_argument("--network", help="network: mainnet, testnet or regtest", choices=['mainnet', 'testnet', 'regtest'], default='testnet')

        
        args = parser.parse_args(sys.argv[2:])

        cmd = KeyCommand(
            seed=args.seed, 
            nonce=args.nonce, 
            output_file=args.out, 
            param_file=args.paramfile, 
            genparam=args.genparam,
            outform=args.outform,
            list_all=args.list,
            network=args.network)
        
        cmd.run()




    # -------------------------------------------------------------------
    # balance: this is a sub-command
    def balance(self):
        parser = argparse.ArgumentParser(
            prog="bbt.sh",
            description='Get the balance of a bitcoin address',
            usage="./bbt.sh balance -a <address> [-n <network>]")
        
        parser.add_argument('-a', '--address', help="bitcoin address", type=address_regex_type)
        parser.add_argument('-n', '--network', help="network: mainnet, testnet or regtest", choices=['mainnet', 'testnet', 'regtest'], default='testnet')
        parser.add_argument('-in', '--input', help="input file", dest='in_', metavar='IN')
        parser.add_argument("-inform", help="input file format", choices=['toml', 'pem'], default='toml')
        parser.add_argument("--all", help="get balance for all addresses", action="store_true")

        args = parser.parse_args(sys.argv[2:])

        cmd = BalanceCommand(
            address=args.address, 
            network=args.network, 
            input_file=args.in_, 
            inform=args.inform,
            all=args.all)
    
        cmd.run()




    # -------------------------------------------------------------------
    # address: this is a sub-command
    def address(self):
        parser = argparse.ArgumentParser(
            prog="bbt.sh",
            description='Get the bitcoin address of a WIF format key',
            usage='''./bbt.sh  address \
                        [-pkey <private_key>] \
                        [-n <network>] \
                        [-in <input file>] \
                        [-inform <toml|pem>] 
Example commands:
    address -pkey cRzuhSMWg8tE2tdLZrmvn8m56wqq6VYnBngwUjjCMT9aYYGSN8kj 
    address -in alice.key
    address -in alice.pem -inform pem
    address -in alice.pem -inform pem --network mainnet  \
''')
        
        parser.add_argument('-pkey', '--private_key', help="private key")
        parser.add_argument('-n', '--network', help="network: mainnet or testnet", choices=['mainnet', 'testnet'], default='testnet')
        parser.add_argument('-in', '--input', help="input file", dest='in_', metavar='IN')
        parser.add_argument("-inform", help="input file format", choices=['toml', 'pem'], default='toml')  
        
        args = parser.parse_args(sys.argv[2:])

        cmd = AddressCommand(
            private_key=args.private_key,
            network=args.network,
            input_file=args.in_,
            inform=args.inform
        )
        cmd.run()


    # -------------------------------------------------------------------
    # transaction: this is a sub-command
    #          - input file (toml)
    #          - broadcast transaction (true or false)
    #          - network (mainnet or testnet)
    def transaction(self):
        parser = argparse.ArgumentParser(
            prog="bbt.sh",
            description='Create a transaction',
            usage='''./bbt.sh <transaction> \
                [-paramfile] \
                [-genparam] \
                [-out <output file>] \
                [-broadcast <true|false>] \
                [-n <network>] \
                [-amount <amount>] \
                [-sender <sender address>] \
                [-sender_key <sender key file>] \
                [-inform <toml|pem>] \
                [-recipient <recipient address>] \
                [-fee <fee>] \
                [-change <change address>] \
                [-pem <private key in pem format>]

Example commands:
    transaction -genparam
    transaction -genparam -out my_transaction.toml
    transaction -paramfile my_transaction.toml 
    transaction -paramfile my_transaction.toml -broadcast false -n testnet
''')
            
        parser.add_argument("-paramfile", help="input parameter file for transaction creation")
        parser.add_argument("-genparam", help="generate parameters", action="store_true")
        parser.add_argument("-out", help="output file", dest='out', metavar='OUTFILE')
        parser.add_argument("-b", "--broadcast", help="broadcast transaction (default true)", choices=['true', 'false'], default='true')
        parser.add_argument('-n', '--network', help="network: mainnet, testnet or regtest", choices=['mainnet', 'testnet', 'regtest'], default='testnet')
        parser.add_argument("-a", "--amount", help="amount to send", type=int)
        parser.add_argument("-sender", help="address to send from")
        parser.add_argument("-sender_key", help="file containing key to sign transaction")
        parser.add_argument("-inform", help="input file format for sender key", choices=['toml', 'pem'], default='toml')
        parser.add_argument("-fee", help="fee (default 300)", default=300, type=int)
        parser.add_argument("-recipient", help="recipient address")
        parser.add_argument("-change", help="change address")
        

        args = parser.parse_args(sys.argv[2:])

        # Custom validation for mutually exclusive arguments
        if not args.paramfile and not args.genparam:
            parser.error("Either -paramfile or -genparam must be specified.")

        # Custom logic to warn if --broadcast is used with -genparam
        if args.genparam and args.broadcast != 'true':
            print("Warning: --broadcast has no effect when used with -genparam", file=sys.stderr)


        cmd = TransactionCommand(
            paramfile=args.paramfile,
            genparam=args.genparam,
            out=args.out,
            broadcast=args.broadcast,
            network=args.network,
            amount=args.amount,
            sender=args.sender,
            sender_key=args.sender_key,
            inform=args.inform,
            fee=args.fee,
            recipient=args.recipient,
            change=args.change
        )

        cmd.run()


    # -------------------------------------------------------------------    
    # consolidate: this is a sub-command
    def consolidate(self):
        parser = argparse.ArgumentParser(
            prog="bbt.sh",
            description='Consolidate UTXO',
            usage="./bbt.sh <consolidate> \
                [-sender_key <sender key file>] \
                [-fee <fee>] \
                [-inform <toml|pem>] \
                [-out <output file>] \
                [-n <network>]")

        parser.add_argument("-sender_key", help="file containing key to sign transaction")
        parser.add_argument("-sender", help="address to send from")
        parser.add_argument("-n", "--network", help="network: mainnet or testnet", choices=['mainnet', 'testnet'], default='testnet')
        parser.add_argument("-fee", help="fee (default 300)", default=300, type=int)
        parser.add_argument("-inform", help="input file format for sender key", choices=['toml', 'pem'], default='toml')
        parser.add_argument("-out", help="output file", dest='out', metavar='OUTFILE')
        

        args = parser.parse_args(sys.argv[2:])

        cmd = ConsolidateCommand(
            sender_key=args.sender_key,
            sender=args.sender,
            network=args.network,
            fee=args.fee,
            inform=args.inform,
            out=args.out
        )

        cmd.run()



    # -------------------------------------------------------------------
    # pkeyformat: this is a sub-command
    def pkeyformat(self):
        parser = argparse.ArgumentParser(
            prog="bbt.sh",
            description='Convert a private key to different formats',
            usage='''./bbt.sh  pkeyformat \
                        [-pkey <private_key>] \
                        [-in <input file>] \
                        [--inform <toml|pem>] \
                        [-from <wif|hex|int>] \
                        [-to <wif|hex|int>]
                        
                        
                        
Example commands:
    pkeyformat -pkey cRzuhSMWg8tE2tdLZrmvn8m56wqq6VYnBngwUjjCMT9aYYGSN8kj 
    pkeyformat -pkey cRzuhSMWg8tE2tdLZrmvn8m56wqq6VYnBngwUjjCMT9aYYGSN8kj -to int
    pkeyformat -pkey 59616176374971377858165786258601335398869230661003382236873763496247842879996 -from int -to hex
    pkeyformat -pkey 83cd8f60e7b49e13194fb2113e23236764325a3d3fac8fba9239854a1588b9fc -from hex -to wif
    pkeyformat -in alice.key
    pkeyformat -in alice.pem -inform pem
    pkeyformat -in alice.pem -inform pem --network mainnet 
''')
        
        parser.add_argument('-pkey', '--private_key', help="private key")
        parser.add_argument('-in', '--input', help="input file", dest='in_', metavar='IN')
        parser.add_argument("-inform", help="input private key format", choices=['toml', 'pem'], default='toml')
        parser.add_argument("-from", help="input private key format",  dest='from_', metavar='FROM', choices=['wif', 'hex', 'int'], default='wif')
        parser.add_argument("-to", help="output private key format", choices=['wif', 'hex', 'int'], default='wif')
        parser.add_argument('-n', '--network', help="network: mainnet or testnet", choices=['mainnet', 'testnet'], default='testnet')
        
        args = parser.parse_args(sys.argv[2:])

        # if args.pkey and not args.from:
        #     self.parser.error("--from is re")

        cmd = PkeyformatCommand(
            pkey=args.private_key,
            input_file=args.in_,
            inform=args.inform,
            from_format=args.from_,
            to_format=args.to,
            network=args.network
        )

        cmd.run()

