#!/usr/bin/env python2
"""Setuptools configuration for mod-auth-ldap3"""
from __future__ import unicode_literals

import codecs

from setuptools import setup


def get_long_description():
    """Reads the main README.rst to get the program's long description"""
    with codecs.open('README.rst', 'r', 'utf-8') as f_readme:
        return f_readme.read()


setup(
    name="mod-auth-ldap3",
    version='0.1',
    description="Shinken WebUI OpenLDAP/ActiveDirectory authentication module",
    long_description=get_long_description(),
    author="VirtualTam",
    author_email='virtualtam@flibidi.net',
    license=' AGPL-3.0',
    url='https://github.com/virtualtam/mod-auth-ldap3',
    keywords="active directory authentication ldap shinken",
    install_requires=[
        'ldap3'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Plugins',
        'License :: OSI Approved'
        ' :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: System :: Monitoring',
        'Topic :: System :: Systems Administration',
        'Topic :: System :: Systems Administration :: Authentication/Directory',
        'Topic :: System :: Systems Administration'
        ' :: Authentication/Directory :: LDAP',
    ]
)
