from setuptools import setup


setup(
    name='simple_snmp_collector',
    version='1.0.0-rc1',
    description='SNMP collector through an asyncio loop',
    url='https://github.com/agn-7/simple-snmp-collector',
    author='agn-7',
    author_email='benyaminjmf@gmail.com',
    license='MIT',
    packages=['event_loop'],
    keywords=[
        'snmp',
        'snmp-collector',
        'asyncio',
        'python3',
        'python',
        'docker',
        'docker-compose'
    ],
    download_url='https://github.com/agn-7/simple-snmp-collector/archive/1.0.0-rc1.zip',
    install_requires=[
        'pyserial',
        'easydict',
        'pysnmp==4.4.9',
        'async-timeout'
    ]
)
