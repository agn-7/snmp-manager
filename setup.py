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
    long_description=long_description,
    packages=find_packages(),
    download_url=f'https://github.com/agn-7/snmp-manager/archive/{__version__}.zip',
)
