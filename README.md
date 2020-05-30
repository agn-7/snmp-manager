# SNMP collector through an asyncio loop

## **1. Clone project**

```bash
git clone <project address>
```

## 2. Up and build docker container:
```bash
docker-compose up --build
```

## 3. Using without docker:

### Install requirements: 

```bash
pip install -r requirements.txt
```

### Config your desire configuration:

```bash
nano config/cofig.json
```

### Run:

```bash
python __main__.py
```

---
[**NOTE**]:

 - If you are a Windows user and you don't want to use docker, comment out the `uvloop` package form `requirements.txt`
 - The value of `-8555` means a problem is occurred during reading data over SNMP or in connection.