from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='PluteosX-sybil-sanctum',
    version='1.2.1',
    packages=find_packages(),
    install_requires=required,
)
