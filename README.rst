
SNMP Collector Powered by Asyncio
=================================

Collecting data from SNMP Agents using ``python-asyncio`` method.

Setup using docker
^^^^^^^^^^^^^^^^^^

Up and build docker container:

.. code-block:: bash

   docker-compose up --build -d

Setup Without docker:
^^^^^^^^^^^^^^^^^^^^^

Install requirements: 

.. code-block:: bash

   pip install -r requirements.txt

Run by downloading or cloning the repository:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   python __main__.py

Config your desire OID(s) and metrics:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   nano config/cofig.json

Setup through ``pip``
-------------------------

.. code-block:: bash

   pip install simple-snmp-collector pyserial easydict pysnmp==4.4.9 async-timeout uvloop

Configuration
^^^^^^^^^^^^^

Create a json config file with the following format:

.. code-block::

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

Run
^^^

.. code-block:: bash

   python -m snmp_collector --config=<path-to-your-config-file.json>

----

[\ **NOTE**\ ]:


* If you are a Windows user and you don't want to use docker, comment out the ``uvloop`` package form ``requirements.txt``
* The value of ``-8555`` means a problem is occurred during reading data over SNMP or in connection.
