@echo off

@REM Wrapper script for running the image locally (Windows)

set "IMAGE_NAME=nchain/rnd-prototyping-wildbittool"

@REM Data directory required - if doesn't exist, create it
if not exist "data" (
    mkdir "data"
)

@REM Run the image
docker run -it --rm -v "%cd%\data:/app/data" %IMAGE_NAME% %*
