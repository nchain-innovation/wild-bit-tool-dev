from useful import load_key_from_file, network_to_key_type
from tx_engine import interface_factory


class utxoCommand:

    def __init__(self,
                 key=None,
                 tx_hash=None,
                 network='testnet'):
        self.key = key
        self.network = network
        self.key_type = network_to_key_type(network)
        self.tx_hash = tx_hash

    # get the address from the key file
    def load_key_from_file(self):
        key = load_key_from_file(self.key, True, self.key_type)
        self.address = key[1]
        return

    # get balance of a bitcoin address
    def get_utxo(self):
        if self.key is None:
            print("Error: No key provided.")
            return

        # TODO: fix the regtest config

        config = {
            "interface_type": "woc",
            "network_type": self.network,
        }

        interface = interface_factory.set_config(config)

        key = load_key_from_file(self.key, True, self.key_type)
        address = key[1]
        unspent = interface.get_utxo(address)
        print(f'UTXO details for {address}')
        print("-" * 40)  # Separator for readability
        for element in unspent:
            print(f'block\t{element["height"]}\ntx_hash:tx_pos {element["tx_hash"]}:{element["tx_pos"]}\nvalue\t{element["value"]}')
            print("-" * 40)  # Separator for readability

    def get_tx_hash(self) -> str:
        if self.tx_hash is None:
            raise ValueError("No tx_hash supplied to download a full transaction")

        config = {
            "interface_type": "woc",
            "network_type": self.network,
        }
        interface = interface_factory.set_config(config)
        raw_tx = interface.get_raw_transaction(self.tx_hash)
        return raw_tx

    def run(self) -> str | None:
        if self.tx_hash is not None:
            return self.get_tx_hash()
        else:
            self.get_utxo()
            return None
