#!/usr/bin/env python
'''
LCpage feeds form data to the LCsim package

LCpage accepts form data and transforms it into argument readable by other
programs in the LCsim package. LCmain is called as a subprocess to handle
all the data and return the finished product to a downloadable file.

@package LCsim
@author blairlm

'''
# -----------------------------
# Standard library dependencies
# -----------------------------

import cgi 
import cgitb
import os 
from subprocess import Popen, PIPE
import sys
from time import time, gmtime, strftime
import numpy as np

#--------------------------------
#Third party library dependencies
#--------------------------------

#from astropy import SkyCoord

# --------------------
# Function Definitions
# --------------------

def saveFile(ufile, saveDir):
        fpath = "%s/%s" % (saveDir, uFile.filename)
        buf = uFile.file.read()
        bytes = len(buf)
        try:
            sFile = open(fPath, 'wb')
        except I0Error:
            print "File {} could not be opened!".format(fPath)
            sys.exit(1)
        sFile.write(buf)
        sFile.close()
        
# -------------
# Main Function
# -------------

def LCopsim_main():
    
    index = np.array([-1.570795,-1.483528611,-1.396262222,-1.308995833,-1.221729444,-1.134463056,-1.047196667,
                  -0.959930278,-0.872663889,-0.7853975,-0.733037667,-0.680677833,-0.628318,-0.575958167,
                  -0.523598333,-0.4712385,-0.418878667,-0.366518833,-0.314159,-0.261799167,-0.209439333,
                  -0.1570795,-0.104719667,-0.052359833,0,0.052359833,0.104719667,0.1570795,0.209439333,
                  0.261799167,0.314159,0.366518833,0.418878667,0.4712385,0.523598333,0.575958167,0.628318,
                  0.680677833])
    
    # Create instance of FieldStorage 
    form = cgi.FieldStorage()
    
    #Create directory with timestamp down to the second
    success = False
    while not success:
        name = strftime("%Y_%m_%d_%H_%M_%S", gmtime())
        if not os.path.isdir(name):
            success = True
    os.umask(0000)
    os.mkdir('storage3/{}'.format(name))
    
    #Process regular inputs
        
    if form.getvalue('ra'):
        ra = form.getvalue('ra')
        ra = float(ra)*np.pi/360
    else:
        print 'You must specify a Right Ascension. Please go back.'
        sys.exit(0)
    
    if form.getvalue('dec'):
        dec = form.getvalue('dec')
        dec = float(dec)*np.pi/360
    else:
        print 'You must specify a declination. Please go back.'
        sys.exit(0)
    
    if dec > 0:
        print 'The LSST is a Southern Hemisphere survey, so there are less observations the higher the declination.<br>'
    if dec > .305432:
        print 'There are fewer observations above 35 degrees, so the closest observation may be more than a degree away or more.<br>'
    
    #Process dropdown box
    
    type = form.getvalue('filter')
    
    opsim = np.genfromtxt('/hd1/LCsim/opsim/opsimindex.dat')
    
    osidx = [0]*opsim.shape[0]
    
    for i in range(opsim.shape[0]):
        osidx[i] = 2*np.arcsin(np.sqrt(np.square(np.sin((opsim[i,3]-dec)/2))+np.cos(dec)*np.cos(opsim[i,3])*np.square(np.sin((ra-opsim[i,2])/2))))
    
    minimum = min(osidx)
    idx = osidx.index(minimum)
    
    val = 1
    
    while opsim[idx,3] > index[val]:
        val = val + 1
        
    osfinal = np.genfromtxt('/hd1/LCsim/opsim/opsim{:02d}.txt'.format(val-1), dtype="i4,f,f,f,S1,S7")
    
    outfile = open('/hd1/LCsim/storage3/{}/opsimobservation.txt'.format(name),'w')
    
    outfile.write('#Observation in MJD\n')
    for line in osfinal:
        if np.abs(line[3] - opsim[idx,3]) < .00001 and np.abs(line[2] - opsim[idx,2]) < .00001 and type == line[4]:
            outfile.write("{:.5f}\n".format(line[1]))
        elif np.abs(line[3] - opsim[idx,3]) < .00001 and np.abs(line[2] - opsim[idx,2]) < .00001 and type == 'all':
            outfile.write("{:.5f}\n".format(line[1]))
            
    outfile.close()
    
    os.chdir('/hd1/LCsim/storage3/{}'.format(name))
    print 'The closest point was found at an Right Ascension of {:.04f} degrees and a Declination of {:.04f} degrees, which is {:.06f} degrees away.'.format(opsim[idx,2]*360/np.pi,opsim[idx,3]*360/np.pi,float(dis)*360/np.pi)
    print '<br>'
    print "<a href='{}' type='text/plain'> Click here for observation data! </a>".format('storage3/{}/opsimobservation.txt'.format(name))
    print ' (Right-click to save)'
    
    print '''
    </body>
    </html>
    '''

    
if __name__ == '__main__':
    
    #Output errors to web
    cgitb.enable()
    
    #Prepare webpage
    print "Content-type: text/html"
    print
    print '''<html>
    <head>
    <meta charset="UTF-8">
    <title>LCsim Results</title>
    <style type="text/css">
    body {
        background-color: #F4F4F4;
    }
    </style>
    </head>
    
    <body>
    <p><img src="banner.jpg" width="600" height="199"  alt=""/></p>
    '''
    
    #Run LCopsim
    ret = LCopsim_main()
    sys.exit(ret)
    
    pass
