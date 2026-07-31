# WildBitTool

Welcome to WildBitTool.  This is an evolving tool kit.

### Functionality

- Create a new bitcoin address

## Prerequisites

- Read-access to the dockerhub **nchain/rnd-prototyping-wildbittool** - request to be added to the group **rndprototypingro**
- Docker installed on your machine

Optional:

- Read-access to the wildbittool-dev Github repository

## How to Run

Try running the help command:

`./wbt.sh -h`

## Networks

WildBitTool selects a blockchain interface from the `--network` flag:

| `--network` | Interface | Notes |
|-------------|-----------|-------|
| `testnet` (default) | WhatsOnChain | Public BSV testnet |
| `mainnet` | WhatsOnChain | Public BSV mainnet |
| `regtest` | JSON-RPC | Local BSV node (see below) |

### Regtest (local node over RPC)

`--network regtest` talks to a local BSV node over JSON-RPC. `wbt.sh` attaches
the container to the `regtest_network` Docker network so the node hostname
resolves. Connection details are read from environment variables, defaulting to
the standard docker regtest node:

| Variable | Default | Meaning |
|----------|---------|---------|
| `RPC_USER` | `bitcoin` | RPC username |
| `RPC_PASSWORD` | `bitcoin` | RPC password |
| `RPC_HOST` | `node1:18332` | `host:port` of the node |

`wbt.sh`/`wbt.bat` forward these variables into the container only when set, so
the defaults work out of the box against the docker node. To point at a
different node:

```bash
export RPC_HOST=127.0.0.1:18332
export RPC_USER=myuser
export RPC_PASSWORD=mypass
./wbt.sh balance -a <address> --network regtest
```

Typical regtest workflow (against a running node):

```bash
./wbt.sh key -s "my seed" -n "my nonce" --network regtest -out alice.key
./wbt.sh balance -in alice.key --network regtest
./wbt.sh transaction -genparam -amount 1000 -sender_key alice.key \
    -recipient <addr> --network regtest -out tx.toml
./wbt.sh transaction -paramfile tx.toml --network regtest
```

> RPC credentials are **never** written into generated parameter files — only
> the interface routing (`interface_type`, `network_type`) is persisted, and
> credentials are re-read from the environment at broadcast time.

## Digging Deeper

When you run a command docker will check if you have the image locally.  If you do not then it will first pull the latest image from Docker Hub.

Docker will then run the image passing in your command line parameters, execute the code, and return any output.

## Developers Guide

### Clone the Code

git clone git@github.com:nchain-innovation/wildbittool-dev.git

### Build It

To build the docker image locally, please exectue the command below.
```bash
./build.sh
```


---

## Tests

To run the unit tests:

```
cd tests
python3 run_all.py
```

To get test coverage reports:

```
python3 -m coverage run -m run_all
python3 -m coverage report  | grep "/wild-bit-tool-dev/src"
```

---

