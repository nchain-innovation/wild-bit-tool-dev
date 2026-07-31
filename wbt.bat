@echo off

@REM Wrapper script for running the image locally (Windows)

set "IMAGE_NAME=nchain/rnd-prototyping-wildbittool"

@REM Data directory required - if doesn't exist, create it
if not exist "data" (
    mkdir "data"
)

@REM Run the image.
@REM RPC_USER / RPC_PASSWORD / RPC_HOST are forwarded from the host env when
@REM set; otherwise the regtest RPC interface uses its docker-node defaults.
docker run -it --rm -v "%cd%\data:/app/data" -e RPC_USER -e RPC_PASSWORD -e RPC_HOST %IMAGE_NAME% %*
