#!/bin/bash

IMAGE_NAME="wildjos/rnd-prototyping"

docker tag wildbittool $IMAGE_NAME
docker image push $IMAGE_NAME

