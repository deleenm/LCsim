#!/usr/bin/python

'''
Cleaner.py identifies and deletes old directories

Detailed Description

@package slopetest
@author ndelee
@version \e \$Revision: 1.1 $
@date \e \$Date: 2014/05/29 16:36:32 $

Usage: cleaner.py -t time
'''

# -----------------------------
# Standard library dependencies
# -----------------------------
import argparse
import os
import sys

# -------------------
# Third-party imports
# -------------------
import numpy as np


# -----------------
# Class Definitions
# -----------------

# --------------------
# Function Definitions
# --------------------

# -------------
# Main Function
# -------------
def fixcurve_main(infile,outfile):


    return(0)

if __name__ == '__main__':
    #Check to make sure we have 2 arguments
    parser = argparse.ArgumentParser(description='Identifies and deletes directories older than given time in days.')
    parser.add_argument('-t',default=2.0,type=float,help='Time in days that a directory should be allowed to exist (Default 2)')


#Put this in a dictionary    
    args = vars(parser.parse_args())
    ret = fixcurve_main(args['t'])
    sys.exit(ret)

    
##
#@mainpage
 #@copydetails  slopetest
