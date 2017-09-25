#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/9/18 11:49
# @Author  : wangzz
# @File    : setup.py

from setuptools import setup

install_requires = ['requirements.txt']


setup(
    name='pb_cli',
    version='0.1.0',
    description="Proto Buffer Command tool",
    keywords='',
    url='',
    author='zhizhao.wang',
    author_email='wangzz@inke.cn',
    license='MIT',
    packages=['pb_cli'],
    zip_safe=False,
    entry_points={
        'console_scripts': ['pbcli = pb_cli.main:main']
    },
    install_requires=[],
)
