# vim: textwidth=80

#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""Setup file for wry."""
from setuptools import setup, find_packages
from os import path
from gitversion import rewritable_git_version

__VERSION__ = rewritable_git_version(path.dirname(path.abspath(__file__)) + '/wry/version.py')

setup(
    name='wry',
    version=__VERSION__,
    packages=find_packages(),
    author='Ahmad Jagot',
    author_email='ahmad.jagot@ocado.com',
    description='Library for managing Intel AMT.',
    long_description=open('README.md').read(),
    url='https://github.com/ocadotechnology/wry/',
    test_suite='wry.tests',
    install_requires=[
        'pywsman >= 2.5.2, < 2.6.0',
        'xmltodict >= 0.7',
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
