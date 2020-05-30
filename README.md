## **1. Clone project from the Git-Server:**

```bash
git clone <project address>
```
## 2. Up and build its docker container:
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

 - If you are a Windows user you don't want to use from docker, comment out the `uvlopp` package form `requirements.txt`