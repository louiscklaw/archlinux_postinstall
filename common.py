#!/usr/bin/env python
# coding:utf-8

import os
import sys
import logging
import traceback
from pprint import pprint

from fabric.api import *

def send_commands(string_commands):
    for single_cmd in string_commands.split('\n'):
        sudo(single_cmd)

def send_commands_sudo_s(string_commands):
    TMP_DIR = '~/_tmp'
    run('mkdir -p {}'.format(TMP_DIR))
    with cd(TMP_DIR):
        for single_command in string_commands.split('\n'):
            sudo('{}'.format(single_command))
