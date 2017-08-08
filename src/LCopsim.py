#!/home/deleenm/anaconda2/envs/LCsim/bin/python
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
        
def LCopsim_main(cra,cdec,cfiltr,cobsfile,csilent):
    #Connect to database
    tic_con = sqlite3.connect('../data/minion_1016_sqlite.db')

    #Create Cursor
    ticcurs = tic_con.cursor()
        
    #Build SQL query to
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
        
    LSSTFieldID_arr = np.array(LSSTFieldID)
    LSSTFieldRA_arr =  np.array(LSSTFieldRA)
    LSSTFieldDec_arr = np.array(LSSTFieldDec)

    form = cgi.FieldStorage()
    
    if(cra != None):
        ra = cra
    elif form.getvalue('ra'):
        ra = form.getvalue('ra')
        ra = float(ra)
    else:
        print('You must specify a Right Ascension. Please go back.')
        sys.exit(0)
    
    if(cdec != None):
        dec = cdec
    elif form.getvalue('dec'):
        dec = form.getvalue('dec')
        dec = float(dec)
    else:
        print('You must specify a declination. Please go back.')
        sys.exit(0)
    
    if csilent == False:   
        if dec > 0:
            print '<div style="color:red"><b>The LSST is a Southern Hemisphere survey, so there are less observations the higher the declination.</b></div><br>'
        if dec > 35:
            print '<div style="color:red"><b>There are fewer observations above 35 degrees, so the closest observation may be more than a degree away or more.</b></div><br>'
  
    if cfiltr != None:
        filtr = cfiltr
    elif form.getvalue('filter'):
        filtr = form.getvalue('filter')

    if cobsfile != None:
        obsfile = cobsfile
    elif form.getvalue('obsfile'):
        obsfile = form.getvalue('obsfile')
    else:
        obsfile = None
    
    Target = SkyCoord(ra*u.deg,dec*u.deg, frame='icrs')
    
    Hexagon_compare = SkyCoord(LSSTFieldRA_arr*u.deg, LSSTFieldDec_arr*u.deg, frame='icrs')
    separation = SkyCoord.separation(Target,Hexagon_compare)
    Hexagon_minID = np.argmin(separation)
    fieldId = str(LSSTFieldID_arr[Hexagon_minID])
    fieldRa = LSSTFieldRA_arr[Hexagon_minID]
    fieldDec = LSSTFieldDec_arr[Hexagon_minID]
    fieldSep = separation[Hexagon_minID]

    if filtr == 'all':
        ticcmd2 = 'SELECT filter,expMJD FROM summary WHERE fieldID = ?'
        ticcurs.execute(ticcmd2,(fieldId,))
    else:
        ticcmd2 = ('SELECT filter,expMJD FROM summary ' 
                  + 'WHERE fieldID = ? AND filter = ?') 
        ticcurs.execute(ticcmd2,(fieldId,filtr))

    ticres = ticcurs.fetchall()

    LSSTFieldFilter = list()
    LSSTFieldDate = list()
    
    for star in ticres:
        LSSTFieldFilter.append(star[0])
        LSSTFieldDate.append(star[1])
        
    LSSTFieldFilter_arr = np.array(LSSTFieldFilter)
    LSSTFieldDate_arr =  np.array(LSSTFieldDate)

    ticcurs.close()

    if csilent == False:
    
        print('<table align="center" border="1">')
        print("<tr><th colspan='2'>Field:{} RA: {:.3f} Dec: {:.3f} Dist: {:.3f}</th></tr>".format(fieldId,fieldRa,fieldDec,fieldSep))
        print("<tr><th>Filter</th><th>MJD</th></tr>")
    
        if len(LSSTFieldFilter_arr) == 0:
            print("<tr><td colspan='2' style='color:red' align='center'><b>No Observations in this Field</b></td></tr>")

        else:
            for i in range(len(LSSTFieldFilter_arr)):
                print("<tr><td>{}</td><td>{}</td></tr>".format(LSSTFieldFilter_arr[i],LSSTFieldDate_arr[i]))
    
        print("</table>")

    if obsfile != None:
        try:
            OBS = open(obsfile, 'w')
        except IOError:
            print("[LCopsim] File {} could not be opened!".format(obsfile))
            sys.exit(1) 

        for i in range(len(LSSTFieldFilter_arr)):
            OBS.write("{}\n".format(LSSTFieldDate_arr[i]))

        OBS.close()
        
if __name__ == '__main__':

    #Output errors to web
    cgitb.enable()
    
    parser = argparse.ArgumentParser(description='Simulates observation dates for LSST in a particular filter')
    parser.add_argument('-r',metavar="RA",type=float,help='Right ascension of target')
    parser.add_argument('-d',metavar="DEC", type=float,help='Declination of target')
    parser.add_argument('-f', metavar="FILTER1,FILTER2",type=str,help='Filter used to view target')
    parser.add_argument('-o', metavar="FILENAME",type=str,help='Filename for observation file')
    parser.add_argument('-s', action='store_true',help='Do not print webpage.')
    

    #Put this in a dictionary
    args = vars(parser.parse_args())

    if args['s'] == False:
        #Prepare webpage
        print "Content-type: text/html"
        print
        print '''<html>
        <head>
        <meta charset="UTF-8">
        <title>LCOpsim Results</title>
        <style type="text/css">
        body {
        background-color: #F4F4F4;
        }
        </style>
        </head>
    
        <body>
        <p><img src="../html/banner.jpg" width="600" height="199"  alt="" style="margin:auto;display:block"/></p>
        '''
    
    #Run LCopsim
    ret = LCopsim_main(args['r'],args['d'],args['f'],args['o'],args['s'])
    sys.exit(ret)
    
    if args['s'] == False:
        print("</body>")
