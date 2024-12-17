FROM python:3.12-slim

ENV PIP_ROOT_USER_ACTION=ignore

RUN apt-get update && \
    apt-get install -y \
    easy-rsa \
    curl \
    build-essential python3-dev \
    && rm -rf /var/lib/apt/lists/*

    # Install Rust and Cargo using rustup
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

# Ensure that the "cargo" and "rustc" binaries are in the PATH
ENV PATH="/root/.cargo/bin:${PATH}"

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

# ENTRYPOINT [ "bash"]