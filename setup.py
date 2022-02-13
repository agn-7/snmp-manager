import sys

from setuptools import setup, find_packages
from snmp_collector import __version__


if sys.version_info[0] < 3:
    with open('README.rst') as f:
        long_description = f.read()
else:
    with open('README.rst', encoding='utf-8') as f:
        long_description = f.read()


setup(
    version=__version__,
    description='SNMP collector through an asyncio loop',
    long_description=long_description,
    packages=find_packages(),
    keywords=[
        'snmp',
        'snmp-collector',
        'snmp-manager'
        'asyncio',
        'python3',
        'python',
        'docker',
        'docker-compose'
    ],
    download_url=f'https://github.com/agn-7/snmp-manager/archive/{__version__}.zip',
    install_requires=[
        'pyserial>=3',
        'easydict>=1',
        'pysnmp>=4',
        'async-timeout>=3'
    ],
    # classifiers=[
    #     'Programming Language :: Python :: 3.6',
    #     'Programming Language :: Python :: 3.7',
    #     'Programming Language :: Python :: 3.8',
    #     'Programming Language :: Python :: 3.9'
    # ],
)
