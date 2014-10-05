#!/usr/bin/env python3
# coding: utf-8
import os
import sys
from .commands import CommandFactory


BASE_DIR_NAME = '.pww'


def main():
    base_dir = os.path.join(os.environ['HOME'], BASE_DIR_NAME)
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    command = CommandFactory(base_dir).create(sys.argv[1:])
    command()
