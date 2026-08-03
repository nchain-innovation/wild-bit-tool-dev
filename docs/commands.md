# WildBitTool — Command Guide

A quick, practical guide to every WildBitTool command. Run everything through the
wrapper script:

```bash
./wbt.sh <command> [args]        # Linux / Mac
wbt.bat  <command> [args]        # Windows
```

Get help for any command with `-h`, e.g. `./wbt.sh transaction -h`.

## A few things to know first

- **Files live in `./data`.** The wrapper mounts `./data` into the container as
  `/app/data`. Any `-out <file>` is written there, and any `-in`/`-paramfile`/
  `-sender_key` is read from there. Use plain filenames (`alice.key`), not paths.
- **Networks.** Every command takes `--network` (or `-n`):
  `testnet` (default), `mainnet`, or `regtest` (a local BSV node over JSON-RPC —
  see the [README](../README.md#regtest-local-node-over-rpc)).
- **TOML in, TOML out.** Keys and transaction parameters are TOML files you can
  read and edit by hand.

The commands, at a glance:

| Command | What it does |
|---------|--------------|
| `key` | Generate a private key / address from a seed + nonce |
| `address` | Show the address for a private key |
| `pkeyformat` | Convert a private key between WIF / hex / int |
| `balance` | Get the balance of an address or key |
| `utxo` | List the UTXOs (spendable coins) for a key |
| `tx_hash` | Fetch full raw transactions by hash |
| `transaction` | Build (and broadcast) a transaction |
| `consolidate` | Sweep many UTXOs into a single output |

---

## Key generation — `key`

Keys are derived deterministically from a **seed** and a **nonce** (the same
seed + nonce always produces the same key), so you can regenerate a key anytime.

```bash
# Create a key, print to screen
./wbt.sh key -s "my seed" -n "my nonce"

# Create a key and save it to data/alice.key
./wbt.sh key -s "my seed" -n "my nonce" -out alice.key

# Same, but for regtest / mainnet
./wbt.sh key -s "my seed" -n "my nonce" -out alice.key --network regtest
```

A saved key file (`.key`) is TOML and looks like this:

```toml
[key_info]
private_key = "cQsBnz1tudJTz2ZfXUPf8rRsMfNUqaJeVG1Vu9JQ6orRTzyt4Yjc"  # WIF
bitcoin_address = "mrz4yxJ9hHmXhTQeVLXcccZ2qKgmM4exwx"
```

Other useful forms:

```bash
# PEM output instead of TOML
./wbt.sh key -s "my seed" -n "my nonce" -out alice.pem -outform pem

# Save just the seed/nonce as a parameter file, regenerate the key later
./wbt.sh key -genparam -s "my seed" -n "my nonce" -out params.toml
./wbt.sh key -paramfile params.toml -out alice.key

# List every key file found in ./data
./wbt.sh key -l
```

| Flag | Meaning |
|------|---------|
| `-s`, `--seed` | Seed phrase |
| `-n`, `--nonce` | Nonce (number used once) |
| `-out` | Output file (in `./data`) |
| `-outform` | `toml` (default) or `pem` |
| `-genparam` | Write the seed/nonce to a parameter file instead of a key |
| `-paramfile` | Regenerate a key from a parameter file |
| `-l`, `--list` | List all keys in `./data` |
| `--network` | `testnet` (default), `mainnet`, `regtest` |

---

## Address & key format helpers

### `address` — show the address for a key

```bash
./wbt.sh address -pkey cRzuhSMWg8tE2tdLZrmvn8m56wqq6VYnBngwUjjCMT9aYYGSN8kj
./wbt.sh address -in alice.key
./wbt.sh address -in alice.pem -inform pem --network mainnet
```

Give it a WIF key directly with `-pkey`, or read it from a file with
`-in` (`-inform toml|pem`, default `toml`).

### `pkeyformat` — convert a private key

Convert a private key between **WIF**, **hex**, and **int** with `-from` / `-to`
(both default to `wif`):

```bash
./wbt.sh pkeyformat -pkey cRzuhSMWg8tE2tdLZrmvn8m56wqq6VYnBngwUjjCMT9aYYGSN8kj -to int
./wbt.sh pkeyformat -pkey 83cd8f60e7b49e...b9fc -from hex -to wif
./wbt.sh pkeyformat -in alice.key -to hex
```

---

## Getting a UTXO or a previous transaction

To spend coins you need two things: the **UTXOs** (which outputs you can spend)
and the **full previous transaction** for each one (needed to sign). WildBitTool
can fetch both.

### `utxo` — list spendable coins for a key

```bash
./wbt.sh utxo -k alice.key --network regtest
```

Output — one entry per spendable coin:

```
UTXO details for mrz4yxJ9hHmXhTQeVLXcccZ2qKgmM4exwx
----------------------------------------
block   105
tx_hash:tx_pos ecd4e889...fa7d:1        # the coin's txid and output index
value   1000000000                      # satoshis
----------------------------------------
```

### `tx_hash` — fetch full raw transactions

Given one or more transaction hashes, return the full serialised (raw hex)
transaction for each. This is the `input_tx_hash` value a transaction needs for
signing:

```bash
./wbt.sh tx_hash ecd4e889...fa7d --network regtest
./wbt.sh tx_hash <hash1> <hash2> <hash3>
```

> **You usually don't need to run these two by hand.** When you generate a
> transaction with `-genparam` plus an `-amount` and a sender, WildBitTool
> automatically picks UTXOs and downloads their previous transactions for you
> (see below). `utxo` and `tx_hash` are there for when you want to inspect or
> assemble things manually.

### `balance` — how much a key/address holds

```bash
./wbt.sh balance -a mrz4yxJ9hHmXhTQeVLXcccZ2qKgmM4exwx
./wbt.sh balance -in alice.key --network regtest
./wbt.sh balance --all                      # every key/pem in ./data
```

---

## Transaction generation — `transaction`

Building a transaction is a two-step flow:

1. **`-genparam`** — create a TOML parameter file describing the transaction.
2. **`-paramfile`** — build (and, by default, broadcast) the transaction from
   that file.

Splitting it in two lets you review or tweak the parameters before anything is
signed or sent.

### Step 1 — generate the parameters

Give it an amount, a sender (a key file), and a recipient. WildBitTool looks up
the sender's UTXOs, downloads the matching previous transactions, and writes a
ready-to-use parameter file:

```bash
./wbt.sh transaction -genparam \
    -amount 1000 \
    -sender_key alice.key \
    -recipient mnFm5CyeroVW5M6YpkKVWFR8TSvYg3gNBH \
    -out spend.toml \
    --network regtest
```

The resulting `spend.toml` is fully populated and looks like this:

```toml
[[transactioninput]]
tx_hash = "ecd4e889...fa7d"              # UTXO being spent
tx_pos = 1
amount = 1000000000
input_tx_hash = "0200000001...67000000" # full previous tx (auto-downloaded)
private_key_for_signing = "cQsBnz1t...t4Yjc"

[[transactionoutput]]
public_key = "mnFm5CyeroVW5M6YpkKVWFR8TSvYg3gNBH"
amount = 500000000
op_return = false
data_to_encode = ""

[interface]
interface_type = "rpc"                    # routing only — no credentials stored
network_type = "testnet"

[tx_info]
create_change_output = true
change_output_public_key = "mrz4yxJ9hHmXhTQeVLXcccZ2qKgmM4exwx"  # defaults to sender
tx_default_fee = 500
```

Change is paid back to the sender unless you pass `-change <address>`. The
default fee is 300 satoshis (`-fee`).

### Step 2 — build and broadcast

```bash
# Build and broadcast (broadcast is on by default)
./wbt.sh transaction -paramfile spend.toml --network regtest

# Build only, don't send — good for checking the serialised tx first
./wbt.sh transaction -paramfile spend.toml -broadcast false
```

### Adding OP_RETURN data

Attach arbitrary data with `-opreturn_data` (inline text, or a filename in
`./data`). Add `-opreturn_data_only` for a data-only output with no payment:

```bash
# Payment + OP_RETURN data
./wbt.sh transaction -genparam -amount 1000 -sender_key alice.key \
    -recipient <addr> -opreturn_data "hello chain" -out spend.toml

# Data-only OP_RETURN (fill in the input placeholders by hand afterwards)
./wbt.sh transaction -genparam -opreturn_data payload.bin -opreturn_data_only \
    -out data.toml
```

### `transaction` flags

| Flag | Meaning |
|------|---------|
| `-genparam` | Generate a parameter file |
| `-paramfile` | Build a transaction from a parameter file |
| `-out` | Where to write the generated parameters |
| `-amount` | Amount to send (satoshis) |
| `-sender_key` | Key file to sign with (sets the sender) |
| `-sender` | Sender address (if not using a key file) |
| `-recipient` | Recipient address |
| `-change` | Change address (defaults to the sender) |
| `-fee` | Fee in satoshis (default 300) |
| `-b`, `--broadcast` | `true` (default) or `false` |
| `-inform` | Sender key format: `toml` (default) or `pem` |
| `-opreturn_data` | Data (text or a filename) for an OP_RETURN |
| `-opreturn_data_only` | OP_RETURN-only output, no payment |
| `--network` | `testnet` (default), `mainnet`, `regtest` |

> On `regtest`, RPC credentials are **never** written into the parameter file —
> only the interface routing is stored, and credentials are read from the
> environment at broadcast time.

---

## Consolidating UTXOs — `consolidate`

Sweep **all** of a key's UTXOs into a single output back to the same address.
Like `transaction`, it generates a parameter file you then build and broadcast:

```bash
# Generate the consolidation parameters (all UTXOs -> one output)
./wbt.sh consolidate -sender_key alice.key -out consolidate.toml --network regtest

# Build and broadcast it
./wbt.sh transaction -paramfile consolidate.toml --network regtest
```

| Flag | Meaning |
|------|---------|
| `-sender_key` | Key file whose UTXOs are swept |
| `-sender` | Sender address (alternative to a key file) |
| `-fee` | Fee in satoshis (default 300) |
| `-inform` | Sender key format: `toml` (default) or `pem` |
| `-out` | Where to write the generated parameters |
| `--network` | `testnet` (default), `mainnet`, `regtest` |

---

## A full worked example (regtest)

```bash
# 1. Make a key
./wbt.sh key -s "my seed" -n "my nonce" -out alice.key --network regtest

# 2. Check it has funds
./wbt.sh balance -in alice.key --network regtest

# 3. (Optional) look at the raw UTXOs
./wbt.sh utxo -k alice.key --network regtest

# 4. Generate the transaction parameters (auto-fetches UTXOs + previous txns)
./wbt.sh transaction -genparam -amount 1000 -sender_key alice.key \
    -recipient <recipient-address> --network regtest -out spend.toml

# 5. Build and broadcast
./wbt.sh transaction -paramfile spend.toml --network regtest
```
