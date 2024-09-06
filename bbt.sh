#!/bin/bash

# Wrapper script for running the image locally (Linux/Mac)

# Image name
IMAGE_NAME="nchain/rnd-prototyping-wildbittool:v1.0"


# RegTest only: network name
NETWORK_NAME="regtest_network"

# Data directory required -if doesn't exist, create it
if [ ! -d "./data" ]; then
  mkdir ./data
fi

DATA_PATH=/app/data

# Function to handle Docker run command
run_docker() {
  local volume_mount="./data:$DATA_PATH"
  local network_option=""
  
  # Check for network parameters
  if [[ "$@" == *"-n"* ]] || [[ "$@" == *"--network"* ]]; then
    if [[ "$@" == *"--network regtest"* ]]; then
      network_option="--network $NETWORK_NAME"
    fi
  fi
  
  # Run Docker command with conditional options
  docker run -it --rm $network_option -v $volume_mount -e DATA_PATH=$DATA_PATH $IMAGE_NAME "$@"
}

# Execute Docker run command with all passed arguments
run_docker "$@"