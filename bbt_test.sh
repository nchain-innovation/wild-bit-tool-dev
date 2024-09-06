#!/bin/bash

# Wrapper script for running the image locally (Linux/Mac)

# IMAGE_NAME="nchain/rnd-prototyping-wildbittool"

# Local image name
IMAGE_NAME="wildbittool_test"

# RegTest only: network name
NETWORK_NAME="regtest_network"

# Dev mode (ON/OFF)
DEV_MODE="ON"

# Data directory required -if doesn't exist, create it
if [ ! -d "./data" ]; then
  mkdir ./data
fi

DATA_PATH=/app/data

echo "DEBUG: $@"
# User command
if [ $DEV_MODE == "OFF" ]; then
  echo "Dev mode is OFF"
  docker run -it -v ./data:/app/data --rm $IMAGE_NAME "$@"


else
  echo "Dev mode is ON"
  # if the parameters contain -n or --network then check for the network name == 'regtest'
  if [[ "$@" == *"-n"* ]] || [[ "$@" == *"--network"* ]]; then
    # check if the network name is 'regtest'
    if [[ "$@" == *"--network regtest"* ]]; then
      # sleep 10
      # docker run -it --network $NETWORK_NAME -v ./src:/app/src -v ./data:$DATA_PATH $IMAGE_NAME 
      echo "Running in regtest network"
      docker run -it --network $NETWORK_NAME -v ./src:/app/src -v ./data:$DATA_PATH -e DATA_PATH=$DATA_PATH $IMAGE_NAME "$@"
      
    else
      echo "JAS: Running in default network"
      docker run -it --rm -v ./src:/app/src -v ./data:$DATA_PATH -e DATA_PATH=$DATA_PATH $IMAGE_NAME "$@" 
    fi
  else
    echo "JAS: Also..Running in default network"
    docker run -it --rm -v ./src:/app/src -v ./data:$DATA_PATH -e DATA_PATH=$DATA_PATH $IMAGE_NAME "$@"
  fi
fi

