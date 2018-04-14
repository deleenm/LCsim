#!/usr/local/lib/student/anaconda3/envs/LCsim/bin/python
'''
LCgenpng plots a Template Lightcurve as a png.

LCgenpng plots a Template Lightcurve as a png. The output will have
the same name as the template file, but replaced with a png extension. 

@package LCsim
@author deleenm

@verbatim
Usage: LCgenpng.py Templatefile
Templatefile   Template lightcurve file
@endverbatim

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
from matplotlib import pyplot as pl

# --------------------
# Function Definitions
# --------------------

# -------------
# Main Function
# -------------

def LCgenpng_main(template):
    phase,mag = np.genfromtxt(template,unpack=True)
    pl.plot(phase,mag,'o')
    pl.xlabel('Phase')
    pl.ylabel('Magnitude')
    pl.gca().invert_yaxis()
    pl.savefig('test.png')
    pl.clf()

if __name__ == '__main__':    
    parser = argparse.ArgumentParser(description="Creates a model lightcurve from a given template.")
    #Input arguments
    parser.add_argument('templatefile', help="Template file")
    args = vars(parser.parse_args())
    ret = LCgenpng_main(args['templatefile'])
    sys.exit(ret)
##
#@mainpage 
#@copydetails LCgenpng.py
