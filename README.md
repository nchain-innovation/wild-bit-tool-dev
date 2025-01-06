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

