#!/usr/local/lib/student/anaconda3/envs/LCsim/bin/python

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

    folder = '../storage3/'
    cleandays = 5
    maxsize = 100 * 1000000 #100 MB max size for storage3
    maxdeltatime =  datetime.timedelta(hours=24*cleandays)
    for directory in os.listdir(folder):
        curpath = os.path.join(folder, directory)
        file_modified = datetime.datetime.fromtimestamp(
            os.path.getmtime(curpath))

        deltatime = datetime.datetime.now() - file_modified
        if deltatime > maxdeltatime:
            shutil.rmtree(curpath)

    if getSize(folder) > maxsize:
        for directory in os.listdir(folder):
            curpath = os.path.join(folder, directory)
            shutil.rmtree(curpath)


def getSize(folder): #Returns size in bytes of a directory
    totalsize = 0
    for directorypath, directorynames, filenames in os.walk(folder):
        #print(directorypath + '\n')
        for f in filenames:
            filepath = os.path.join(directorypath, f)
            size = os.path.getsize(filepath)
            totalsize += size
    return totalsize

if __name__ == '__main__':
    ret = LCcleaner()

##
#@mainpage
#@copydetails LCcleaner.py
