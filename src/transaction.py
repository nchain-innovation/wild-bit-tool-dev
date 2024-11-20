# from tx_engine.tx.bsv_factory import bsv_factory
from tx_engine import interface_factory, Tx, TxIn, TxOut, p2pkh_script,Script, address_to_public_key_hash
from tx_engine.engine.op_codes import OP_DROP, OP_RETURN, OP_FALSE
from typing import Union
from tx_engine.interface.mock_interface import MockInterface
from tx_engine.interface.woc_interface import WoCInterface
from tx_engine.interface.rpc_interface import RPCInterface

# from tx_engine.tx.tx import TxIn, TxOut, Tx

# from tx_engine.tx.tx_sign import sign_input_bsv
# from tx_engine.tx.tx_fetcher import tx_fetcher
# from tx_engine.engine.standard_scripts import p2pkh_script
# from tx_engine.engine.helper import decode_base58
# from tx_engine.engine.script import Script
# from tx_engine.engine.op_codes import (OP_RETURN, OP_FALSE)


# from tx_engine.engine.keys import (PrivateKey)
from tx_engine import Wallet

from useful import read_file, print_amounts, set_regtest_config




# -------------------------------------------------------------------
# -------------------------------------------------------------------

# Build the transaction from the toml file
def build_tx(filename:str) -> str:

    config = read_file(filename)

    params = config['interface']

    interface = interface_factory.set_config(params)

    vouts = []
    vins = []
    amt_total_out:int = 0

    # Validate that 'transactionoutput' key exists
    if "transactionoutput" not in config:
        raise KeyError("transactionoutput")

    for outs in config["transactionoutput"]:
        if not outs["op_return"]:
            payment_addr: str = outs["public_key"]
            amt:int = outs["amount"]
            # locking_script = p2pkh_script(decode_base58(payment_addr))
            locking_script = p2pkh_script(address_to_public_key_hash(payment_addr))
            vouts.append(TxOut(amount=amt,script_pubkey=locking_script))
            amt_total_out += amt
        else:
            data_to_add = outs["data_to_encode"]
            op_return_script = Script([OP_FALSE, OP_RETURN, data_to_add.encode()])
            vouts.append(TxOut(amount=0,script_pubkey=op_return_script))

    # Validate that 'transactionoutput' key exists
    if "transactioninput" not in config:
        raise KeyError("transactioninput")
    
    amt_total_in:int = 0
    for ins in config["transactioninput"]:
        # vins.append(TxIn(prev_tx=bytes.fromhex(ins["tx_hash"]), prev_index=ins["tx_pos"]))
        vins.append(TxIn(prev_tx=ins["tx_hash"], prev_index=ins["tx_pos"]))
        amt_total_in += ins["amount"]

    ret_amt:int = 0
    fee:int = config["tx_info"]["tx_default_fee"]
    
    # determine any change to be paid
    if config["tx_info"]["create_change_output"]:
        if amt_total_in >  amt_total_out + fee:

            if "change_output_public_key" not in config["tx_info"]:
                raise KeyError("change_output_public_key")
            
            change_addr: str = config["tx_info"]["change_output_public_key"]
            
            # Check if the change_output_public_key is set to <sender address>
            if change_addr == "<sender address>":
                raise ValueError("Invalid change_output_public_key: <sender address> is not a real address.")

            
            amt_to_pay:int = amt_total_out + fee
            ret_amt:int = amt_total_in - amt_to_pay
            if ret_amt > 300:
                # locking_script = p2pkh_script(decode_base58(change_addr)) 
                locking_script = p2pkh_script(address_to_public_key_hash(change_addr)) 
                vouts.append(TxOut(amount=ret_amt, script_pubkey=locking_script))

    
    print_amounts(amt_total_out, amt_total_in, fee, ret_amt)
    
    # tx_fetcher.set_client(bsv_client)
    tx = Tx(version=1,
                tx_ins=vins,
                tx_outs=vouts,
                locktime=0,
                testnet=interface.is_testnet())
    
    for i in range(len(tx.tx_ins)):
        wif_key:str = config["transactioninput"][i]["private_key_for_signing"]
        bitcoin_priv_key:PrivateKey = PrivateKey(wif=wif_key,network="test")
        retval = sign_input_bsv(tx, i, bitcoin_priv_key)
        if not retval:
            raise ValueError("Failed to sign & verify signature before transmission @ index " + str(i))

    return tx.serialize().hex()


# -------------------------------------------------------------------
# Broadcast the transaction
def broadcast_tx(tx_hex: str, filename:str) -> str: 
    params = read_file(filename)

    config = params['bsv_client']

    if config['type'] == 'regtest':
        set_regtest_config(config)

    bsv_client = bsv_factory.set_config(config)


    # send it
    response = bsv_client.broadcast_tx(tx_hex)
    if response.status_code != 200:
        print(f'Error -> {response.content}')
        raise ValueError(response.content)
    else:
        print(f'{response.content}')
        return response.content

