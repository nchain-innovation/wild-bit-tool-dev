#!/bin/bash

# Wrapper script for running the image locally (Linux/Mac)

# Local image name
IMAGE_NAME="wildbittool"

# RegTest only: network name
NETWORK_NAME="regtest_network"

# Dev mode (ON/OFF)
DEV_MODE="ON"

# Data directory required -if doesn't exist, create it
if [ ! -d "./data" ]; then
  mkdir ./data
fi

DATA_PATH=/app/data

# Function to handle Docker run command based on DEV_MODE and network parameters
run_docker() {
  local volume_mount="./data:$DATA_PATH"
  local network_option=""
  local src_volume=""
  
  # Adjust volume mount for DEV_MODE ON
  if [ "$DEV_MODE" == "ON" ]; then
    src_volume="-v ./src:/app/src"
  fi
  
  # Check for network parameters
  if [[ "$@" == *"-n"* ]] || [[ "$@" == *"--network"* ]]; then
    if [[ "$@" == *"--network regtest"* ]]; then
      network_option="--network $NETWORK_NAME"
    fi
  fi
  
  # Print the command before running it
  # echo "docker run -it --rm ${network_option} -v ${volume_mount} ${src_volume} -e DATA_PATH=$DATA_PATH $IMAGE_NAME \"$@\""
  
  # Execute the Docker command.
  # RPC_USER / RPC_PASSWORD / RPC_HOST are forwarded from the host env only
  # when set (docker '-e VAR' with no value); otherwise the regtest RPC
  # interface falls back to its docker-node defaults (bitcoin/bitcoin/node1:18332).
  docker run -it --rm ${network_option} -v "${volume_mount}" ${src_volume} -e DATA_PATH="$DATA_PATH" -e RPC_USER -e RPC_PASSWORD -e RPC_HOST $IMAGE_NAME "$@"
}

# Echo DEV_MODE status
echo "Dev mode is $DEV_MODE"

# Execute Docker run command with all passed arguments
run_docker "$@"