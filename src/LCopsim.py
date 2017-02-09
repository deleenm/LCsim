#!/usr/bin/env python
'''
LCpage feeds form data to the LCsim package
'''

import cgi 
import cgitb
import os 
from subprocess import Popen, PIPE
import sys
from time import time, gmtime, strftime
import numpy as np
import sqlite3
import argparse
from astropy.coordinates import SkyCoord
import astropy.units as u

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
        
#Connect to database
tic_con = sqlite3.connect('/home/student/research/OpSim/minion_1016_sqlite.db')

#Create Cursor
ticcurs = tic_con.cursor()
#Build SQL query
ticcmd = 'SELECT fieldID,fieldRA,fieldDec FROM field'
    
tic_con.row_factory = sqlite3.Row
ticcurs.execute(ticcmd)
#Fetch all the rows
ticres = ticcurs.fetchall()

LSSTFieldID = list()
LSSTFieldRA = list()
LSSTFieldDec = list()

for star in ticres:
#build lists
    LSSTFieldID.append(star[0])
    LSSTFieldRA.append(star[1])
    LSSTFieldDec.append(star[2])
        
print "Number of Fields: {}".format(len(LSSTFieldID))
LSSTFieldID_arr = np.array(LSSTFieldID)
LSSTFieldRA_arr =  np.array(LSSTFieldRA)
LSSTFieldDec_arr = np.array(LSSTFieldDec)
print(LSSTFieldID_arr)
print(LSSTFieldRA_arr)
print(LSSTFieldDec_arr)

ticcurs.close()

def LCopsim_main(ra,dec,filtr):
        
    Target = SkyCoord(ra*u.deg,dec*u.deg, frame='icrs')
    
    Hexagon_compare = SkyCoord(LSSTFieldRA_arr*u.deg, LSSTFieldDec_arr*u.deg, frame='icrs')
    Hexagon_minID = np.argmin(SkyCoord.separation(Target,Hexagon_compare))
    print(Hexagon_minID)
  
    tic_con2 = sqlite3.connect('/home/student/research/OpSim/minion_1016_sqlite.db')
    ticcurs2 = tic_con.cursor()
    ticcmd2 = 'SELECT filter,expMJD FROM summary GROUP BY fieldID'
    tic_con2.row_factory = sqlite3.Row
    ticcurs2.execute(ticcmd2)
    ticres2 = ticcurs2.fetchall()

    LSSTFieldFilter = list()
    LSSTFieldDate = list()
    
    for star in ticres2:
        LSSTFieldFilter.append(star[0])
        LSSTFieldDate.append(star[1])
        
        LSSTFieldFilter_arr = np.array(LSSTFieldFilter)
        LSSTFieldDate_arr =  np.array(LSSTFieldDate)

    ticcurs2.close()
    
    print(LSSTFieldFilter_arr[Hexagon_minID])
    print(LSSTFieldDate_arr[Hexagon_minID])

    form = cgi.FieldStorage()
    
    if form.getvalue('ra'):
        ra = form.getvalue('ra')
        ra = float(ra)*np.pi/180
    else:
        print 'You must specify a Right Ascension. Please go back.'
        sys.exit(0)
    
    if form.getvalue('dec'):
        dec = form.getvalue('dec')
        dec = float(dec)*np.pi/180
    else:
        print 'You must specify a declination. Please go back.'
        sys.exit(0)
    
    if dec > 0:
        print 'The LSST is a Southern Hemisphere survey, so there are less observations the higher the declination.<br>'
    if dec > .305432:
        print 'There are fewer observations above 35 degrees, so the closest observation may be more than a degree away or more.<br>'
  
    filtr = form.getvalue('filtr')

#    Target = SkyCoord(ra*u.rad,dec*u.rad, frame='icrs')
    
#    for i in LSSTFieldRA_arr and LSSTFieldDec_arr:
#        Hexagon_compare = SkyCoord(LSSTFieldRA_arr[i]*u.deg, LSSTFieldDec_arr[i]*u.deg, frame='ircs')
#        Hexagon_min = min(SkyCoord.separation(Target,Hexagon_compare))
#        print(Hexagon_min.ra)
#        print(Hexagon_min.dec)
        
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Simulates observation dates for LSST in a particular filter')
    parser.add_argument('ra',type=float,help='Right ascension of target')
    parser.add_argument('dec', type=float,help='Declination of target')
    parser.add_argument('filtr', type=str,help='Filter used to view target')

    #Put this in a dictionary
    args = vars(parser.parse_args())
    LCopsim_main(args['ra'],args['dec'],args['filtr'])
    
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
