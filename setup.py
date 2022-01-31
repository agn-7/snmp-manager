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
    name='snmp_manager',
    version=__version__,
    description='SNMP collector through an asyncio loop',
    long_description=long_description,
    url='https://github.com/agn-7/simple-snmp-collector',
    author='agn-7',
    author_email='benyaminjmf@gmail.com',
    license='MIT',
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
    download_url='https://github.com/agn-7/snmp-manager/archive/1.1.2.zip',
    install_requires=[
        'pyserial==3.5',
        'easydict==1.9',
        'pysnmp==4.4.12',
        'async-timeout==3.0.1'
    ],
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ],
)
