#!/usr/local/lib/student/anaconda3/envs/LCsim/bin/python
#'''
#LCopsim.py querys an SQLite database to give filters and epochs in LSST for a
#hello


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
    #check for Right Ascension
    if(cra != None):
        ra = cra
    elif form.getvalue('ra'):
        ra = form.getvalue('ra')
        ra = float(ra)
    else:
        print('You must specify a Right Ascension. Please go back.')
        sys.exit(0)
    #check for declination
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
            print('<div style="color:red"><b>The LSST is a Southern Hemisphere survey, so there are less observations the higher the declination.</b></div><br>')
        if dec > 35:
            print('<div style="color:red"><b>There are fewer observations above 35 degrees, so the closest observation may be more than a degree away or more.</b></div><br>')

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
        print("<tr><th colspan='2'> Field:{} RA: {:.3f} Dec: {:.3f} Dist: {:.3f}</th></tr>".format(fieldId,fieldRa,fieldDec,fieldSep))
        print("<tr><th>Filter</th><th>MJD</th></tr>")

        if len(LSSTFieldFilter_arr) == 0:
            print("<tr><td colspan='2' style='color:red' align='center'><b>No Observations in this Field</b></td></tr>")

        else:
            for i in range(len(LSSTFieldFilter_arr)):
                print("<tr><td>{}</td><td>{}</td></tr>".format(LSSTFieldFilter_arr[i],LSSTFieldDate_arr[i]))

        print("</table><br><br><br>")

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
        print("Content-type: text/html")
        print()
        print('''<!doctype html>
            <html>
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1">
                    <title>LCsim</title>

                    <!-- Latest compiled and minified CSS -->
                    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
                    <!-- custom stlesheet import -->
                    <link rel="stylesheet" href="../html/css/style.css">
                    <!-- jQuery library -->
                    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>

                    <!-- Latest compiled JavaScript -->
                    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>

                    <script src ="js/errorHandlers.js"></script>

                    <style type="text/css">


                    [data-error-type="errormessage"]{color: red;}

                    </style>
                </head>

    <body>
      <nav class="navbar navbar-default navbar-fixed-top">
    	<div class="container-fluid">
    		<div class="navbar-header">
    			<button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#myNavbar">
    				<span class="icon-bar"></span>
    				<span class="icon-bar"></span>
    				<span class="icon-bar"></span>
    			</button>
    			<a class="navbar-brand" href="#">LCSim</a>
    		</div>
    		<div class="collapse navbar-collapse" id="myNavbar">
    			<ul class="nav navbar-nav">
    				<li><a href="../html/index.html">Home</a></li>
    				<li class="dropdown">
    					<a class="dropdown-toggle" data-toggle="dropdown" href="#">Simple Models <span class="caret"></span></a>
    					<ul class="dropdown-menu">
    						<li><a href="../html/index.html">Mag</a></li>
    						<li><a href="../html/flux.html">Flux</a></li>
    					</ul>
    				</li>
    				<li class="dropdown">
    					<a class="dropdown-toggle" data-toggle="dropdown" href="#">Variable Models <span class="caret"></span></a>
    					<ul class="dropdown-menu">
    						<li><a href="../html/range.html">Mag</a></li>
    						<li><a href="../html/fluxrange.html">Flux</a></li>
    					</ul>
    				</li>
    				<li class="active"><a href="../html/opsim.html">Opsim</a></li>
    				<li><a href="../html/about.html">About</a></li>
    			</ul>

    		</div>
    	</div>
    	</nav>
    	<br><br>
      <div class="container">
    		<div class="row">
    			<div class=" col-lg-12 col-sm-12 col-md-12 col-xs-12">
    				<div align="center" class="banner">
    					<img src="../html/images/LCsim_banner.png" alt="LCsim banner" width="75%">
    				</div>

    			</div>
    		</div>
    	</div>

          <div class="container" style="border-top: 1px solid #DCDCDC ">
        <br><br>
        <div class="row">
        <div class="col-lg-2 col-md-3 col-sm-6 col-xs-6 center-block">
            <button type="button" class="btn btn-success">Download CSV</button>
        </div>
        </div>
        <br>
        <div class="row">
            <div class= "col-lg-6 col-md-6 col-sm-12 col-xs-12 center-block">
                <div style="height: 420px; overflow: auto;">


        ''')

    #Run LCopsim
    ret = LCopsim_main(args['r'],args['d'],args['f'],args['o'],args['s'])
    sys.exit(ret)

    if args['s'] == False:
        print("</div> </div> </div> </div> </body> </html>")
