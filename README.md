# SNMP Collector Powered by Asyncio

Collecting data from SNMP Agents using `python-asyncio` method.

## Setup using docker

### Up and build docker container:
```bash
docker-compose up --build -d
```

## Without docker:

### Install requirements: 

```bash
pip install -r requirements.txt
```

### Run by downloading or cloning the repository:

```bash
python __main__.py
```

### Config your desire OID(s) and metrics: 

```bash
nano config/cofig.json
```

## Setup through `pip`

```bash
pip install simple-snmp-collector pyserial easydict pysnmp==4.4.9 async-timeout uvloop
```
### Configuration

Create a json config file with the following format:

```
[
  {
    "isEnable": true,
    "name": "snmp-model-1",
    "address": "192.168.1.120",
    "port": 161,
    "timeout": 1,
    "retries": 3,
    "version": 2,
    "sleep_time": 5,
    "community": "public",
    "metrics": [
      {
        "isEnable": true,
        "tag_name": "a-sample",
        "oid": "1.3.6.13.4.1.3.1112"
      }
    ],
    "meta_data": [{'key': 'value'}]
  }
]
``` 

### Run

```bash
python -m snmp_collector --config=<path-to-your-config-file.json>
```

---
[**NOTE**]:

 - If you are a Windows user and you don't want to use docker, comment out the `uvloop` package form `requirements.txt`
 - The value of `-8555` means a problem is occurred during reading data over SNMP or in connection.
