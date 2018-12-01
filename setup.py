from setuptools import setup, find_packages

with open('README') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='10gg',
    version='0.1.0',
    description='A log analysis tool for TiDB',
    long_description=readme,
    author='10gg',
    url='https://github.com/10gg/10gg',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)