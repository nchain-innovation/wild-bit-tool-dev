FROM python:3.11-slim-bookworm

ENV ENV PIP_ROOT_USER_ACTION=ignore

COPY ./tx-engine-package /app/tx_engine_package

WORKDIR /app/tx_engine_package
RUN pip3 install -e .


RUN mkdir /app/data
RUN mkdir /app/src

COPY ./src /app/src
WORKDIR /app/src

ENTRYPOINT [ "python3", "main.py"]
# CMD ["sleep", "infinity"]