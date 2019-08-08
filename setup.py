import codecs
import os
import re

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

def read(*parts):
    # intentionally *not* adding an encoding option to open
    return codecs.open(os.path.join(here, *parts), 'r').read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    long_description = readme.read()


classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
]


setup(
    name='bqpjson',
    version=find_version('bqpjson', '__init__.py'),
    packages=['bqpjson'],
    package_data={'bqpjson': ['*.json']},
    install_requires=['jsonschema==2.6.0'],
    setup_requires=['pytest-runner==4.5.1'],
    tests_require=['pytest-cov'],
    test_suite="tests",
    author='Carleton Coffrin',
    author_email='cjc@lanl.gov',
    classifiers=classifiers,
    description='utilities for working with bqpjson data',
    license='BSD',
    long_description=long_description,
    url='https://github.com/lanl-ansi/bqpjson',
    download_url='https://github.com/lanl-ansi/bqpjson/archive/{}.tar.gz'.format(find_version('bqpjson', '__init__.py')),
    entry_points={'console_scripts': [
        'bqp2qh = bqpjson.cli:bqp2qh',
        'bqp2qubo = bqpjson.cli:bqp2qubo',
        'bqp2mzn = bqpjson.cli:bqp2mzn',
        'bqp2hfs = bqpjson.cli:bqp2hfs',
        'spin2bool = bqpjson.cli:spin2bool'
    ]},
)

