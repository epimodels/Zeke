from setuptools import find_packages
from setuptools import setup


setup(
    description='Zeke',
    install_requires=[
        'Django',
        'matplotlib',
    ],
    long_description=open('README.rst').read(),
    name='zeke',
    packages=find_packages(),
    test_suite='zeke.tests.TestSuite',
)
