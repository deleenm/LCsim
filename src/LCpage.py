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
import logging
import numpy as np

# --------------------
# Function Definitions
# --------------------

'''
Save uploaded file to upload directory
'''
def saveFile(uFile, saveDir):
        fPath = "%s/%s" % (saveDir, uFile.filename)
        buf = uFile.file.read()
        bytes = len(buf)
        try:
            sFile = open(fPath, 'wb')
        except IOError:
            print("[LCpage] File {} could not be opened!".format(fPath))
            sys.exit(1)
        sFile.write(buf)
        sFile.close()

# -------------
# Main Function
# -------------
def LCpage_main():
    
    global name, name
    start = time()
    # Create instance of FieldStorage 
    form = cgi.FieldStorage()
    
    #Ensure that template file is uploaded
    if not form['tempfile'].filename:
        print('You must include a template file. Please go back and upload one.')
        sys.exit(0)
    
    #Create directory with timestamp down to the second

    success = False
    while not success:
        try:
            name = strftime("%Y_%m_%d_%H_%M_%S", gmtime())
            if not os.path.isdir(name):
                success = True
                os.umask(0000)
            os.mkdir('storage3/{}'.format(name))
        except OSError:
            success = False

    os.mkdir('storage3/{}/upload'.format(name))
    
    #Specify upload directory
    saveDir = "./storage3/{}/upload".format(name)
    
    #Process uploads
    if form['tempfile'].filename:
        saveFile(form['tempfile'], saveDir)
        templatefile = '{}/{}'.format(saveDir, form['tempfile'].filename)
    
    if form['obsfile'].filename:
        saveFile(form['obsfile'], saveDir)
        obsfile = '{}/{}'.format(saveDir, form['obsfile'].filename)
    else:
        obsfile = None
    
    #Process regular inputs
    if form.getvalue('scalemin') and form.getvalue('scalemax') and form.getvalue('scalestep'):
        if form.getvalue('scaletype') == 'scalelin':
            a = np.linspace(float(form.getvalue('scalemin')),float(form.getvalue('scalemax')),float(form.getvalue('scalestep')))
        elif form.getvalue('scaletype') == 'scalelog':
            a = np.logspace(np.log10(float(form.getvalue('scalemin'))),np.log10(float(form.getvalue('scalemax'))),float(form.getvalue('scalestep')))
        alength = int(a.size)
    elif form.getvalue('scale'):    
        a = form.getvalue('scale')
        alength = 1
    else:
        print 'You must specify a scale factor. Please go back.'
        sys.exit(0)
    if form.getvalue('error'):
        e = form.getvalue('error')
    elif not form['obsfile'].filename:
        print 'You must specify an error value. Please go back.'
        sys.exit(0)
    else: 
        e = ''
    if form.getvalue('filename'):
        f = form.getvalue('filename')
    else:
        print 'You must specify a filename. Please go back.'
        sys.exit(0)
    n = form.getvalue('number')
    if form.getvalue('periodmin') and form.getvalue('periodmax') and form.getvalue('periodstep'):
        if form.getvalue('periodtype') == 'periodlin':
            p = np.linspace(float(form.getvalue('periodmin')),float(form.getvalue('periodmax')),float(form.getvalue('periodstep')))
        elif form.getvalue('periodtype') == 'periodlog':
            p = np.logspace(np.log10(float(form.getvalue('periodmin'))),np.log10(float(form.getvalue('periodmax'))),float(form.getvalue('periodstep')))
        plength = int(p.size)
    elif form.getvalue('period'):
        p = form.getvalue('period')
        plength = 1
    elif form.getvalue('format') =='fdate':
        plength = 1
        p = ''
    else:
        print 'You must specify a period. Please go back.'
        sys.exit(0)
    s = form.getvalue('sigma')
    
    #Process checkboxes
    if form.getvalue('info'):
        i = True
    else:
        i = None
    
    if form.getvalue('poisson'):
        poisson = True
    else:
        poisson = None
    
    #Process radio buttons
    phase = form.getvalue('phase')
    phaselength = 1
    if not form.getvalue('phase') and not form.getvalue('phasemin') and form.getvalue('format') != 'fdate':
        print 'You must specify a phase offset. Please go back.'
        sys.exit(0)
    if form.getvalue('format') == 'fphase':
        d = ''
    if form.getvalue('phasemin') and form.getvalue('phasemax') and form.getvalue('phasestep'):
        if form.getvalue('phasetype') == 'phaselin':
            phase = np.linspace(float(form.getvalue('phasemin')),float(form.getvalue('phasemax')),float(form.getvalue('phasestep')))
        elif form.getvalue('phasetype') == 'phaselog':
            phase = np.logspace(np.log10(float(form.getvalue('phasemin'))),float(np.log10(form.getvalue('phasemax'))),float(form.getvalue('phasestep')))
        phaselength = int(phase.size) 
        d = ''
    if form.getvalue('format') == 'fdate':
        d = True
        phase = 0
    if form.getvalue('date') is not None:
        z = form.getvalue('date')
    else:
        z = ''
        d = ''
    
    #Process dropdown box
    flux = ''
    if form.getvalue('magvalue'):
        if form.getvalue('mag') == 'max':
            max = form.getvalue('magvalue')
            min = ''
        elif form.getvalue('mag') == 'min':
            max = ''
            min = form.getvalue('magvalue')
    elif form.getvalue('fluxvalue'):
        flux = True
        if form.getvalue('flux') == 'max':
            max = form.getvalue('fluxvalue')
            min = ''
        elif form.getvalue('flux') == 'min':
            max = ''
            min = form.getvalue('fluxvalue')
    else:
        print 'You must specify a maximum or minimum magnitude or value. Please go back.'
        sys.exit(0)
    
    if int(n)*alength*plength*phaselength > 100000:
        print "Total lightcurves produced cannot exceed 100000. Please go back."
        sys.exit(0)
    
    #Run LCmain with form data
    prog = Popen(['./LCmain.py','{}'.format(templatefile),'-o','{}'.format(obsfile),
                   '-a','{}'.format(a),'-e','{}'.format(e),'-p','{}'.format(p),
                   '--phase','{}'.format(phase), '-s','{}'.format(s),
                   '--max','{}'.format(max), '--min','{}'.format(min),
                   '-f','{}'.format(f), '-i','{}'.format(i),
                   '--poisson','{}'.format(poisson),'-z','{}'.format(z),
                   '-d','{}'.format(d),'--name','{}'.format(name),
                   '-n','{}'.format(n),'--flux','{}'.format(flux)],
                   stdout=PIPE)
    
    prog.wait()
    
    #Output files and leave them available to download
    
    print prog.communicate()[0]
    print '''
    </body>
    </html>
    '''


    #Remove uploaded files
    os.remove('{}/{}'.format(saveDir, form['tempfile'].filename))
    if form['obsfile'].filename:
        os.remove('{}/{}'.format(saveDir, form['obsfile'].filename))
    
if __name__ == '__main__':
    
    #Output errors to web
    cgitb.enable()
    #Log file
    LOG_FILENAME = '../log/lcsim.log'
    #Formats text for the file
    logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO,format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    logging.info("Directory: "+ 'storage3/{}'.format(name)+" Template File: " + form['tempfile'].filename + " Obs File: " + form['obsfile'].filename)

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
    <p><img src="../html/banner.jpg" width="600" height="199"  alt=""/></p>
    '''


    #Run LCpage
    ret = LCpage_main()
    sys.exit(ret)
    
    pass
