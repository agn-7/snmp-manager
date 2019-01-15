#### **1. Install Git:**

```bash
sudo apt-get update
sudo apt-get install git
```

#### **2. Clone project from the Git-Server:**

```bash
git clone http://192.168.1.130:81/infravision/ivms/snmp_collector

```
#### 3. Up and build its docker container:
```bash
docker-compose up --build
```