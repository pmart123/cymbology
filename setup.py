from os.path import exists
from setuptools import setup

setup(
    name='security_id',
    version='0.1',
    packages=['security_id'],
    url='https://github.com/pmart123/security_id',
    license='BSD',
    author='Philip Martin',
    author_email='philip.martin2007@gmail.com',
    long_description=open('README.md').read() if exists("README.md") else 'Identify and Validate Financial Security Codes',
)
