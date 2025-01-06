import argparse
import sys
import os
from pathlib import Path

from key_command import KeyCommand
from balance_command import BalanceCommand
from address_command import AddressCommand
from consolidate_command import ConsolidateCommand
from transaction_command import TransactionCommand
from pkeyformat_command import PkeyformatCommand
from utxo_command import utxoCommand
from useful import address_regex_type

# Specify the directory path
# path = r'/app/data'
# set directory path to the environment variable or default to /app/data
if 'DATA_PATH' in os.environ:
    path = os.environ['DATA_PATH']
else:
    path = '/app/data'


# -------------------------------------------------------------------
# -------------------------------------------------------------------
class ArgumentHandler(object):

    def __init__(self):
        parser = argparse.ArgumentParser(
            prog="wbt.sh",
            description='WildBitTool',
            usage='''./wbt.sh <command> [<args>]

The most commonly used WildBitTool commands are:
   key          Generates a key from a seed and nonce
   balance      Get the balance of a bitcoin address
   address      Get the bitcoin address of a private key
   utxo         Get a list of utxo for a given private key (toml)
   tx_hash      Return full transactions for a given list of tx hashes
   transaction  Create a transaction
   pkeyformat   Convert a private key to and from different formats
   consolidate  Consolidate UTXOs (many inputs to one output)
''')
        parser.add_argument('command', help='Subcommand to run')
        # parse_args defaults to [1:] for args
        # exclude the rest of the args or validation will fail
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print('Unrecognized command')
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
            prog="wbt.sh",
            description='Generates a key from a seed and nonce',
            usage='''./wbt.sh <key> [-s <seed>] [-n <nonce>] [-out <output file>] \
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
            prog="wbt.sh",
            description='Get the balance of a bitcoin address',
            usage="./wbt.sh balance -a <address> [-n <network>]")
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
            prog="wbt.sh",
            description='Get the bitcoin address of a WIF format key',
            usage='''./wbt.sh  address \
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
    # balance: this is a sub-command
    def utxo(self):
        parser = argparse.ArgumentParser(
            prog="wbt_dev.sh",
            description='Get a list of UTXO for a given WIF key',
            usage="./wbt_dev.sh utxo -key <key file> [-n <network>]")
        parser.add_argument('-k', '--key', help="bitcoin WIF key file")
        parser.add_argument('-n', '--network', help="network: mainnet, testnet or regtest", choices=['mainnet', 'testnet', 'regtest'], default='testnet')

        args = parser.parse_args(sys.argv[2:])
        cmd = utxoCommand(
            key=args.key,
            network=args.network)
        cmd.run()

# -------------------------------------------------------------------
    # balance: this is a sub-command
    def tx_hash(self):
        parser = argparse.ArgumentParser(
            description='Get full transaction data for a list of transaction hashes',
            usage="./wbt_dev.sh tx_hash tx_hash1 [tx_hash2 tx_hash3]")

        parser.add_argument(
            'hashes',
            metavar='tx_hash',
            type=str,
            nargs="+"
        )
        parser.add_argument('-n', '--network', help="network: mainnet, testnet or regtest", choices=['mainnet', 'testnet', 'regtest'], default='testnet')
        args = parser.parse_args(sys.argv[2:])
        for tx in args.hashes:
            cmd = utxoCommand(
                tx_hash=tx,
                network=args.network)
            print("-" * 40)
            print(f'{cmd.run()}')
            print("-" * 40)

    # -------------------------------------------------------------------
    # transaction: this is a sub-command
    #          - input file (toml)
    #          - broadcast transaction (true or false)
    #          - network (mainnet or testnet)
    def transaction(self):
        parser = argparse.ArgumentParser(
            prog="wbt.sh",
            description='Create a transaction',
            usage='''./wbt.sh <transaction> \
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
                [-pem <private key in pem format>] \
                [-op_return_data <File Path or Data on commandline] \
                [-op_return_data_only]

Example commands:
    transaction -genparam s
    transaction -genparam -out my_transaction.toml
    transaction -paramfile my_transaction.toml
    transaction -paramfile my_transaction.toml -broadcast false -n testnet
    transaction -paramfile -locking_script "LOCKING SCRIPT"
    transaction -paramfile -opreturn_only
    transaction -paramfile -out my_transaction.toml -auto_utxo
''')
        parser.add_argument("-paramfile", help="input parameter file for transaction creation")
        parser.add_argument("-genparam", help="generate parameters", action="store_true")
        parser.add_argument("-out", help="output file", dest='out', metavar='OUTFILE')
        parser.add_argument("-b", "--broadcast", help="broadcast transaction (default true)", choices=['true', 'false'], default='true')
        parser.add_argument('-n', '--network', help="network: mainnet, testnet or regtest", choices=['mainnet', 'testnet', 'regtest'], default='testnet')
        parser.add_argument("-a", "--amount", help="amount to send", type=int)
        parser.add_argument("-auto_utxo", help="given the amount,select the utxo for input and download the transactions", type=bool)
        parser.add_argument("-sender", help="address to send from")
        parser.add_argument("-sender_key", help="file containing key to sign transaction")
        parser.add_argument("-inform", help="input file format for sender key", choices=['toml', 'pem'], default='toml')
        parser.add_argument("-fee", help="fee (default 300)", default=300, type=int)
        parser.add_argument("-recipient", help="recipient address")
        parser.add_argument("-change", help="change address")
        parser.add_argument("-opreturn_data", metavar='<DATA_OR_FILE>', help="data to add using an opreturn and p2pkh")
        parser.add_argument("-opreturn_data_only", help="op_return only or attach to a p2pkh", action="store_true")
        args = parser.parse_args(sys.argv[2:])

        # Custom validation for mutually exclusive arguments
        if not args.paramfile and not args.genparam:
            parser.error("Either -paramfile or -genparam must be specified.")

        # Custom logic to warn if --broadcast is used with -genparam
        if args.genparam and args.broadcast != 'true':
            print("Warning: --broadcast has no effect when used with -genparam", file=sys.stderr)

        # process the data it its there.
        data_val_or_file: str = ""
        data_val_is_file: bool = False

        if args.opreturn_data:
            the_file = Path(os.path.join(path, args.opreturn_data))
            if os.path.isfile(the_file):
                data_val_or_file = args.opreturn_data
                data_val_is_file = True
            else:
                data_val_or_file = args.opreturn_data

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

        if data_val_or_file is not None:
            cmd.op_return_data = data_val_or_file
            if args.opreturn_data_only:
                cmd.op_return_data_only = args.opreturn_data_only
            if data_val_is_file is True:
                cmd.op_return_data_is_file = data_val_is_file
        cmd.run()

    # -------------------------------------------------------------------
    # consolidate: this is a sub-command
    def consolidate(self):
        parser = argparse.ArgumentParser(
            prog="wbt.sh",
            description='Consolidate UTXO',
            usage="./wbt.sh <consolidate> \
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
            prog="wbt.sh",
            description='Convert a private key to different formats',
            usage='''./wbt.sh  pkeyformat \
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
        parser.add_argument("-from", help="input private key format", dest='from_', metavar='FROM', choices=['wif', 'hex', 'int'], default='wif')
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
