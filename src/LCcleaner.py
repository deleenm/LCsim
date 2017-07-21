#!/usr/bin/env python

'''
Cleaner.py identifies and deletes old directories

Detailed Description

@package LCsim
@author ndelee

Usage: LCcleaner.py -t time
'''

# -----------------------------
# Standard library dependencies
# -----------------------------
import os
import shutil
import sys
import time

# -------------------
# Third-party imports
# -------------------
import numpy as np
import os
import datetime
# -------------
# Main Function
# -------------

def LCcleaner():
    time.sleep(5)
    folder = '../storage3/'
    for dirpath, dirnames, filenames in os.walk(folder):
        for file in filenames:
            curpath = os.path.join(dirpath, file)
            file_modified = datetime.datetime.fromtimestamp(os.path.getmtime(curpath))
            if datetime.datetime.now() - file_modified > datetime.timedelta(hours=24*5):
                os.remove(curpath)

if __name__ == '__main__':
    ret = LCcleaner()

##
#@mainpage 
#@copydetails LCcleaner.py
