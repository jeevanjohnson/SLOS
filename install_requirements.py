#!/usr/bin/env python

import sys
import subprocess

subprocess.run(
    f'{sys.executable} -m pip install -r requirements.txt',
    stdin = subprocess.DEVNULL,
    stderr = subprocess.DEVNULL,
    stdout = subprocess.DEVNULL
)