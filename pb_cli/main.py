#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/9/18 12:50
# @Author  : wangzz
# @File    : main.py

import argparse
import importlib
import os

from ConfigParser import ConfigParser
from subprocess import call

SETUP_TEMPLATE = """
from setuptools import setup, find_packages

setup(
    name='{package_name}',
    version='{version}',
    packages=find_packages(),
    install_requires=['protobuf']
)
"""

MANIFEST_TEMPLATE = """
recursive-include {} *.py *.proto
"""


def generate(proto_src, language, dest, plugin, module):
    for file in proto_src:
        prefix, ext = os.path.splitext(file)
        if ext != '.proto':
            print 'This is not a proto file'
            return
        if call(['which', 'protoc']) == -1:
            print 'You must install proto compiler first'
            return

    language_out = '--{language}_out={dest}'.format(language=language,
                                                    dest=dest)
    plugin = '--plugin={}'.format(plugin)
    src_dir = os.path.dirname(proto_src[0])
    cmdline = ['protoc', '-I', src_dir, language_out, plugin]
    cmdline.extend(proto_src)
    return_code = call(cmdline)
    if return_code != 0:
        print "Python pacakge generation failed!"
        return
    absolute_path = os.path.abspath(dest)
    try:
        print absolute_path
        mod = importlib.import_module('{}_pb2'.format(dest))
        if not hasattr(mod, 'major') or not hasattr(mod, 'minor') or not hasattr(mod, 'patch'):
            print 'Please add VERSION_MAJOR, VERSION_MINOR, VERSION_PATCH to your proto file'
            return
    except ImportError as e:
        print e
        return


def generate_setup(package_name, version):
    with open('{}/__init__.py'.format(package_name), 'w') as f:
        pass

    with open('setup.py', 'w') as f:
        content = SETUP_TEMPLATE.format(package_name=package_name, version=version)
        f.write(content)
    with open('MANIFEST.in', 'w') as f:
        content = MANIFEST_TEMPLATE.format(package_name)
        f.write(content)


def generate_py():
    cfg = ConfigParser()
    cfg.read('config.ini')
    version = cfg.get('config', 'version')
    package_name = cfg.get('config', 'package_name')

    cwd = os.getcwd()
    package_dir = '{}/{}'.format(cwd, package_name)
    if not os.path.exists(package_dir):
        os.makedirs(package_dir)

    cmdline = ['protoc', '--python_out=./{}/'.format(package_name), '--plugin=rpc', '*.proto']
    cmdline = ' '.join(cmdline)
    return_code = call(cmdline, shell=True)
    if return_code != 0:
        print "Generate python pb files failed!"
        return
    generate_setup(package_name, version)


def upload():
    register_cmdline = ['python', 'setup.py', 'register', '-r', 'devpi']
    return_code = call(register_cmdline)
    if return_code != 0:
        print "Register to private devpi server failed!"
        return

    upload_cmdline = ['python', 'setup.py', 'sdist', 'upload', '-r', 'devpi']
    return_code = call(upload_cmdline)
    if return_code != 0:
        print "Upload to private devpi server failed!"
        return


def main():
    parser = argparse.ArgumentParser(description='Proto Buffer Command tool')
    parser.add_argument('-g', '--generate', action='store_true', help=u'generate pb python files')
    parser.add_argument('-u', '--upload', action='store_true', help=u'upload package to private server')
    args = parser.parse_args()
    is_generate = args.generate
    is_upload = args.upload
    if is_generate:
        generate_py()
    if is_upload:
        upload()


if __name__ == '__main__':
    main()
