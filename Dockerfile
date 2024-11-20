FROM python:3.11-slim-bookworm

ENV PIP_ROOT_USER_ACTION=ignore

# Set the working directory to /app
WORKDIR /app
COPY requirements.txt .


# Install required packages and remove requirements.txt
RUN pip install --no-cache-dir -r requirements.txt && rm requirements.txt

# REMOVE THIS AFTER TESTING
# COPY tx_engine-0.6.8-cp312-cp312-macosx_10_7_x86_64.whl .
# RUN pip install --force-reinstall /app/tx_engine-0.6.8-cp312-cp312-macosx_10_7_x86_64.whl

RUN mkdir -p /app/src /app/data

# WORKDIR /app/src
COPY ./src /app/src
WORKDIR /app/src

# Entry point for the container
ENTRYPOINT [ "python3", "main.py"]
