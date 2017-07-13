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
# -------------
# Main Function
# -------------

def LCcleaner():
    time.sleep(5)
    folder = '../storage3/'
    for files in os.listdir(folder):
        file_path = os.path.join(folder, files)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
        except Exception as e:
            print(e)

if __name__ == '__main__':
    ret = LCcleaner()

##
#@mainpage 
#@copydetails LCcleaner.py
