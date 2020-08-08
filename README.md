# SNMP collector through an Asyncio event loop

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

### Run:

```bash
python __main__.py
```

## Configuration

### Config your desire OID(s) ane metrics: 

```bash
nano config/cofig.json
```

---
[**NOTE**]:

 - If you are a Windows user and you don't want to use docker, comment out the `uvloop` package form `requirements.txt`
 - The value of `-8555` means a problem is occurred during reading data over SNMP or in connection.
