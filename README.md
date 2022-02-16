[![PyPi version](https://badgen.net/pypi/v/snmp-manager/)](https://pypi.org/project/snmp-manager/)
[![PyPi license](https://badgen.net/pypi/license/snmp-manager/)](https://pypi.com/project/snmp-manager/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/snmp-manager.svg)](https://pypi.python.org/pypi/snmp-manager/)
[![Docker](https://badgen.net/badge/icon/docker?icon=docker&label)](https://https://docker.com/)
[![build](https://github.com/agn-7/snmp-manager/workflows/build/badge.svg)](https://github.com/agn-7/snmp-manager/actions/workflows/github-actions.yml)
[![codecov](https://codecov.io/gh/agn-7/snmp-manager/branch/master/graph/badge.svg?style=flat-square)](https://codecov.io/gh/agn-7/snmp-manager) 



# SNMP Collector Powered by Asyncio

Collecting data from SNMP Agents using `python-asyncio` method.

### Setup using docker

Up and build docker container:
```bash
docker-compose up --build -d
```

### Setup Without docker:

Install requirements: 

```bash
pip install -r requirements.txt
```

Configure the desire OID(s) and metrics: 

```bash
nano snmp_collector/config/cofig.json
```

Run:

```bash
python snmp_collector
```

### Setup through `pip`

```bash
pip install snmp-manager
```
Configuration:

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
    "gain": 1,
    "offset": 0,
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

Run:

```bash
python -m snmp_collector --config=<path-to-your-config-file.json>
```

---
[**NOTE**]:

 - The value of `-8555` means a problem is occurred during reading data over SNMP or in connection.
