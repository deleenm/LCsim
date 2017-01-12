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

# --------------------
# Function Definitions
# --------------------
'''
Save uploaded file to upload directory
'''

def gcirc(u,ra1,dc1,ra2,dc2,verb=False):
#+
# NAME:
#     GCIRC
# PURPOSE:
#     Computes rigorous great circle arc distances.
# EXPLANATION:
#     Input position can either be either radians, sexagesimal RA, Dec or
#     degrees.   All computations are double precision.
#
# CALLING SEQUENCE:
#      GCIRC, U, RA1, DC1, RA2, DC2
#
# INPUTS:
#      U    -- integer = 0,1, or 2: Describes units of inputs and output:
#              0:  everything radians
#              1:  RAx in decimal hours, DCx in decimal
#                       degrees, DIS in arc seconds
#              2:  RAx and DCx in degrees, DIS in arc seconds
#      RA1  -- Right ascension or longitude of point 1
#      DC1  -- Declination or latitude of point 1
#      RA2  -- Right ascension or longitude of point 2
#      DC2  -- Declination or latitude of point 2
#
# OUTPUTS:
#      DIS  -- Angular distance on the sky between points 1 and 2
#              See U above for units;  double precision
#
# PROCEDURE:
#      "Haversine formula" see
#      http://en.wikipedia.org/wiki/Great-circle_distance
#
# NOTES:
#       (1) If RA1,DC1 are scalars, and RA2,DC2 are vectors, then DIS is a
#       vector giving the distance of each element of RA2,DC2 to RA1,DC1.
#       Similarly, if RA1,DC1 are vectors, and RA2, DC2 are scalars, then DIS
#       is a vector giving the distance of each element of RA1, DC1 to
#       RA2, DC2.    If both RA1,DC1 and RA2,DC2 are vectors then DIS is a
#       vector giving the distance of each element of RA1,DC1 to the
#       corresponding element of RA2,DC2.    If the input vectors are not the
#       same length, then excess elements of the longer ones will be ignored.
#
#       (2) The function SPHDIST provides an alternate method of computing
#        a spherical distance.
#
#       (3) The haversine formula can give rounding errors for antipodal
#       points.
#
# PROCEDURE CALLS:
#      None
#
#   MODIFICATION HISTORY:
#      Written in Fortran by R. Hill -- SASC Technologies -- January 3, 1986
#      Translated from FORTRAN to IDL, RSH, STX, 2/6/87
#      Vector arguments allowed    W. Landsman    April 1989
#      Prints result if last argument not given.  RSH, RSTX, 3 Apr. 1998
#      Remove ISARRAY(), V5.1 version        W. Landsman   August 2000
#      Added option U=2                      W. Landsman   October 2006
#      Use double precision for U=0 as advertised R. McMahon/W.L. April 2007
#      Use havesine formula, which has less roundoff error in the
#             milliarcsecond regime      W.L. Mar 2009
#-

    d2r    = np.pi/180.0
    as2r   = np.pi/648000.0
    h2r    = np.pi/12.0

    #Convert input to double precision radians
 
    if u == 0:
        rarad1 = np.array(ra1,ndmin=1)
        rarad2 = np.array(ra2,ndmin=1)
        dcrad1 = np.array(dc1,ndmin=1)
        dcrad2 = np.array(dc2,ndmin=1)
    elif u == 1:
        rarad1 = np.array(ra1,ndmin=1)*h2r
        rarad2 = np.array(ra2,ndmin=1)*h2r
        dcrad1 = np.array(dc1,ndmin=1)*d2r
        dcrad2 = np.array(dc2,ndmin=1)*d2r      

    elif u == 2:
        rarad1 = np.array(ra1,ndmin=1)*d2r
        rarad2 = np.array(ra2,ndmin=1)*d2r
        dcrad1 = np.array(dc1,ndmin=1)*d2r
        dcrad2 = np.array(dc2,ndmin=1)*d2r 

    else:
        print 'U must be 0 (radians), 1 ( hours, degrees) or 2 (degrees)'
        sys.exit(1)

    deldec2 = (dcrad2-dcrad1)/2.0
    delra2 =  (rarad2-rarad1)/2.0
    sindis = np.sqrt( np.sin(deldec2)*np.sin(deldec2) + np.cos(dcrad1)*np.cos(dcrad2)*np.sin(delra2)*np.sin(delra2) )
    dis = 2.0*np.arcsin(sindis)

    if u != 0:
        dis = dis/as2r

    if verb == True:
        for dist in dis:
            if (u != 0) and (dist >= 0.1) and (dist <= 1000):
                fmt = '10.4f'
            else:
                fmt = '15.8E'
            if (u != 0):
                units = ' arcsec'
            else:
                units = ' radians'
                print 'Angular separation is {:{format}} {}'.format(dist,units,format=fmt)

    return(dis)

def saveFile(uFile, saveDir):
        fPath = "%s/%s" % (saveDir, uFile.filename)
        buf = uFile.file.read()
        bytes = len(buf)
        try:
            sFile = open(fPath, 'wb')
        except IOError:
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
    
    dis = gcirc(0,opsim[idx,2],opsim[idx,3],ra,dec,verb=False)
    
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
