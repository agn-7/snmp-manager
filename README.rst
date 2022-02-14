

.. image:: https://badgen.net/pypi/v/snmp-manager/
   :target: https://pypi.org/project/snmp-manager/
   :alt: PyPi version


.. image:: https://badgen.net/pypi/license/snmp-manager/
   :target: https://pypi.com/project/snmp-manager/
   :alt: PyPi license


.. image:: https://img.shields.io/pypi/pyversions/snmp-manager.svg
   :target: https://pypi.python.org/pypi/snmp-manager/
   :alt: PyPI pyversions


.. image:: https://badgen.net/badge/icon/docker?icon=docker&label
   :target: https://https://docker.com/
   :alt: Docker


.. image:: https://codecov.io/gh/agn-7/snmp-manager/branch/master/graph/badge.svg?style=flat-square
   :target: https://codecov.io/gh/agn-7/snmp-manager
   :alt: codecov
 

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

Configure the desire OID(s) and metrics: 

.. code-block:: bash

   nano snmp_collector/config/cofig.json

Run:

.. code-block:: bash

   python snmp_collector

Setup through ``pip``
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   pip install snmp-manager

Configuration:

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

Run:

.. code-block:: bash

   python -m snmp_collector --config=<path-to-your-config-file.json>

----

[\ **NOTE**\ ]:


* The value of ``-8555`` means a problem is occurred during reading data over SNMP or in connection.
