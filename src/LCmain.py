#!/usr/bin/env python
'''
LCmain processes data from LCpage

LCmain calls on programs from LCsim to process data inputted via web form
into LCpage. It returns a file listing Day, Amplitude, Error, and Phase
in a .cur file to the web.

@package LCsim
@author blairlm

'''
# -----------------------------
# Standard library dependencies
# -----------------------------
import argparse
import cgitb
import os
import sys
from subprocess import Popen

# -------------------
# Third-party imports
# -------------------
import LCsim
import numpy as np
# -------------
# Main Function
# -------------

def LCmain_date(args):
    
    number = 0
    
    os.umask(0000)
    
    try: 
        outfile = open('../storage3/{}/info.txt'.format(args.name),'w')
    except IOError:
        print "[LC Main]File {} could not be opened!".format('info.txt')
        sys.exit(1)
    outfile.write('File             Period  Amp  Phase offset\n')
    
    try:
        alength = len(args.a)
    except:
        alength = 1
    try:
        phaselength = len(args.phase)
    except:
        phaselength = 1

    for j in range(alength):
        
            for l in range(phaselength):
                
                if alength > 1:
                    amp = args.a[j]
                else:
                    amp = args.a
                if phaselength > 1:
                    phase = args.phase[l]
                else:
                    phase = args.phase
                
                
                #Create inputs for LCsim_model if not provided
                if args.d == 'True':
                    args.d = True
                if args.e == '':
                    args.e = .01
                if args.o == 'None':
                    args.o = LCsim.obs_create()
                if args.max == '':
                    if args.min == '':
                        args.max = -float(amp)
                    else:
                        args.max = float(args.min) - float(amp)
                if args.z == '':
                    args.z = 0
                if args.flux == 'True':
                    args.flux = True
                elif args.flux == True:
                    pass
                else:
                    args.flux = None
                
                period = ''
                
                #Create initial model    
                main_model = LCsim.LCsim_model(args.templatefile, amp, args.d, args.e,
                                              args.o, period, phase, args.max, args.z, args.flux)
                
                
                for i in range(int(args.n)):
                    
                    #Set output file type        
                    file = args.f+'{num:05d}'.format(num=i+number)+'.cur'
                    
                    if args.z != 0:
                        emax = float(args.z)
                    else:
                        emax = phase*period
                        while emax < main_model[0,3]:
                            emax = emax + period
                    
                    outfile.write("{} {:.3f} {:.4f} {:.4f} {:.3f}\n".format(file,period,amp,phase,emax))
                    
                    #Add Gaussian noise based on error
                    model, noise_norm = LCsim.gaussian_noise(main_model, args.poisson, args.flux)
                        
                    #Create Gaussian noise based on sigma
                    if args.s != '':
                        model, noise = LCsim.sigma_noise(model, args.s)
                        noise_norm = noise + noise_norm   
                    
                    #Save model to file
                    np.set_printoptions(suppress=True)
                    LCsim.save_model(model,file,args.name)
                    
                    if args.i == 'True':
                        #Save the noise data to file if desired
                        LCsim.save_noise(noise_norm,args.name,i+number)
                        
                number = int(args.n) + number
    #Print link to lightcurve data
    outfile.close()

    tar = Popen(["tar -czf ../storage3/{}/download/{}.tar.gz ../storage3/{}/download/*".format(args.name, args.f, args.name)], shell=True)
    tar.wait()


def LCmain_main(args):
    
    number = 0
    
    os.umask(0000)
    
    try: 
        outfile = open('../storage3/{}/info.txt'.format(args.name),'w')
    except IOError:
        print "[LCmain]File {} could not be opened!".format('info.txt')
        sys.exit(1)
    outfile.write('File             Period  Amp  Phase offset  Epoch of Maximum\n')
    
    try:
        alength = len(args.a)
    except:
        alength = 1
    try:
        plength = len(args.p)
    except:
        plength = 1
    try:
        phaselength = len(args.phase)
    except:
        phaselength = 1

    for j in range(alength):
        
        for k in range(plength):
        
            for l in range(phaselength):
                
                if alength > 1:
                    amp = args.a[j]
                else:
                    amp = args.a
                if plength > 1:
                    period = args.p[k]
                else:
                    period = args.p
                if phaselength > 1:
                    phase = args.phase[l]
                else:
                    phase = args.phase
                
                #Create inputs for LCsim_model if not provided
                if args.e == '':
                    args.e = .01
                if args.o == 'None':
                    args.o = LCsim.obs_create()
                if args.max == '':
                    if args.min == '':
                        args.max = -float(amp)
                    else:
                        args.max = float(args.min) - float(amp)
                if args.z == '':
                    args.z = 0
                if args.flux == 'True':
                    args.flux = True
                elif args.flux == True:
                    pass
                else:
                    args.flux = None
                
                #Create initial model    
                main_model = LCsim.LCsim_model(args.templatefile, amp, args.d, args.e,
                                              args.o, period, phase, args.max, args.z, args.flux)
                
                for i in range(int(args.n)):
                    
                    #Set output file type        
                    file = args.f+'{num:05d}'.format(num=i+number)+'.cur'
                    
                    if args.z != 0:
                        emax = float(args.z)
                    else:
                        emax = phase*period
                        while emax < main_model[0,3]:
                            emax = emax + period
                    
                    outfile.write("{} {:.3f} {:.4f} {:.4f} {:.3f}\n".format(file,period,amp,phase,emax))
                    
                    #Add Gaussian noise based on error
                    model, noise_norm = LCsim.gaussian_noise(main_model, args.poisson, args.flux)
                        
                    #Create Gaussian noise based on sigma
                    if args.s != '':
                        model, noise = LCsim.sigma_noise(model, args.s)
                        noise_norm = noise + noise_norm   
                    
                    #Save model to file
                    np.set_printoptions(suppress=True)
                    LCsim.save_model(model,file,args.name)
                    
                    if args.i == 'True':
                        #Save the noise data to file if desired
                        LCsim.save_noise(noise_norm,args.name,i+number)
                        
                number = int(args.n) + number

    #Print link to lightcurve data
    outfile.close()
    
    os.chdir('../storage3/{}'.format(args.name))
    tar = Popen(["tar -czf {}.tar.gz *".format(args.f)], shell=True)
    tar.wait()


    print "<a href='{}' type='text/plain' id='link'> Click here for lightcurve data! </a>".format('../storage3/{}/{}.tar.gz'.format(args.name, args.f))



if __name__ == '__main__':
    
    #Allow errors to output to web
    cgitb.enable()
    
    os.umask(0000)
        
    #Handle arguments from LCpage
    parser = argparse.ArgumentParser(description="Creates a model lightcurve from a given template.")
    
    #Input arguments
    parser.add_argument('templatefile', 
                        help="list template file")
    parser.add_argument('-a', metavar='AMP',
                        help='enter desired amplitude of lightcurve')
    parser.add_argument('-d', metavar='USE_DATE',
                        help='use option if template uses date instead of phase')
    parser.add_argument('-e', metavar='ERROR',
                        help="enter size of error bar in mag")
    parser.add_argument('-f', metavar='FILE', default='model', 
                        help='filename of the output file (Default: model.cur)')
    parser.add_argument('--flux', metavar='FLUX',
                        help='use if template lightcurve is given in flux/counts')
    parser.add_argument('-i', metavar='INFO_T/F',
                        help="record options used to simulate observation")
    parser.add_argument('-n', metavar='NUMBER',
                        help="number of lightcurves to make")
    parser.add_argument('--name', metavar='PATH_NAME',
                        help="pass path name for writing downloadable files")
    parser.add_argument('-o', metavar='OBSFILE',
                        help="include observation file")
    parser.add_argument("-p", metavar='PERIOD',
                        help="enter period of lightcurve in days")
    parser.add_argument('--phase', metavar='OFFSET',
                        help='enter phase offset for lightcurve')
    parser.add_argument("--poisson", metavar='POISSON', 
                        help="add Poisson noise")
    parser.add_argument('-s', metavar='SIGMA',
                        help='add Gaussian noise based on listed sigma')
    parser.add_argument('--max', metavar='MAX',
                        help='enter maximum magnitude of lightcurve')
    parser.add_argument('--min', metavar='MIN',
                        help='enter minimum magnitude of lightcurve')
    parser.add_argument('-z', metavar='DATE',
                        help='enter epoch of zero phase')
    
    #Compile arguments and run them through LCmain_main
    args = parser.parse_args()
    
    #Convert strings to arrays
    try:
        float(args.a)
        args.a = float(args.a)
    except:
        args.a = args.a.replace('[','')
        args.a = args.a.replace(']','')
        args.a = [float(s) for s in args.a.split()]
        args.a = args.a
    try:
        float(args.p)
        args.p = float(args.p)
    except:
        args.p = args.p.replace('[','')
        args.p = args.p.replace(']','')
        args.p = [float(s) for s in args.p.split()]
        args.p = args.p
    try:
        float(args.phase)
        args.phase = float(args.phase)
    except:
        args.phase = args.phase.replace('[','')
        args.phase = args.phase.replace(']','')
        args.phase = [float(s) for s in args.phase.split()]
        args.phase = args.phase
    
    if args.d == 'True':
        ret = LCmain_date(args)
        sys.exit(ret)
    else:
        ret = LCmain_main(args)
        sys.exit(ret)
##
#@mainpage 
#@copydetails LCmain.py
