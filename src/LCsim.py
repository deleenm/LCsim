#!/usr/bin/env python
'''
LCsim creates a model lightcurve from specified data

LCsim is designed to create a model lightcurve with desired noise from a
specified template, observation times, errors, and period. It can be run
from the command line, but it also contains the necessary functions for
the other codes in the LCsim package to create a web-based tool that 
accomplishes the same tasks for multiple runs.

@package LCsim
@author blairlm

@verbatim
Usage: LCsim.py Templatefile
period
Templatefile   Template lightcurve file
@endverbatim

'''

# -----------------------------
# Standard library dependencies
# -----------------------------
import argparse
from collections import defaultdict
import os
import sys

# -------------------
# Third-party imports
# -------------------
import numpy as np
from scipy import interpolate

# --------------------
# Function Definitions
# --------------------
def fixcurve_main(infile,outfile):
    '''
    fixcurve.py takes template lightcurves and makes sure they run from 0 to 1.0 
    in phase
    '''
    #Make a dictionary for each phase
    curves = defaultdict(list)

    phase,mag = np.genfromtxt(infile,usecols=[0,1],unpack=True)

    if len(phase) < 2.0:
        print "Your lightcurve file must have more than 2 points!"
        return(1)

    wrongindex1 = ((phase < -1.0).nonzero())[0]
    wrongindex2 = ((phase > 1.0).nonzero())[0]
    if len(wrongindex1) > 0 or len(wrongindex2) > 0:
        print "Your lightcurve phases must be between -1.0 and 1.0! (inclusive)"
        return(1)

    badindex = ((phase < 0.0).nonzero())[0]
    
    phase[badindex] = phase[badindex] + 1
#test
    #Check for multiple values for the same phase
    for i in range(len(phase)):
        curves[phase[i]].append(mag[i])

    #Average any phase points that happen more than once.
    for key in curves.keys():
        curves[key] = np.mean(curves[key]) 

    #Make sure both phase 0 and 1 exists. If they don't use highest
    #and lowest phase point to interpolate.

    if 0 in curves and 1 not in curves:
        curves[1] = curves[0]
    if 1 in curves and 0 not in curves:
        curves[0] = curves[1]
    if 1 not in curves and 0 not in curves:
        small_phase = [max(curves.keys()),min(curves.keys())+1]
        small_mag = [curves[max(curves.keys())],curves[min(curves.keys())]] 
        new_mag = interpolate.interp1d(small_phase,small_mag)
        curves[0] = new_mag(1.0)
        curves[1] = new_mag(1.0)

    out = open(outfile,'w')
    
    for key in sorted(curves.keys()):
        out.write("{:.3f} {}\n".format(key,curves[key]))
    
    out.close()              
    return(out)

def gaussian_noise(model, poisson, flux):
    '''
    Add Gaussian noise relative to error size to the model lightcurve
    '''
    l = model.shape[0]
    
    #Grab l samples from a Gaussian distribution 
    #with a mean of 0 and a sigma of 1
    noise = np.random.randn(l,1)
    
    #Adjust noise to size of error bar
    noise_norm = np.multiply(noise,model[:,2])[:,0]
    
    if poisson == 'True':
        noise_norm = poisson_noise(model, noise_norm, flux)
    
    #Apply noise to model
    newmag = model[:,1] + noise_norm[:]
    model[:,1] = newmag
    
    return(model, noise_norm)

# model = LCsim_model(args.templatefile, args.a, args.e, args.o, args.p, args.phase)
def LCsim_model(templatefile, amp, date, error, obsfilename, period, phase_offset, max, zero_time, flux):
    '''
    Create a model lightcurve from the given template file
    '''
    
    #Create arrays from inputs
    if type(templatefile) is str:
        template = np.genfromtxt(templatefile)
    else:
        template = templatefile
    if flux is True:
        template[:,1] = -template[:,1]
        
    if type(obsfilename) == str:
        time_err=np.genfromtxt(obsfilename)
    else:
        time_err = obsfilename
        
    if time_err.shape[0] == time_err.size:
        time = time_err
        err = np.zeros((time.size,1))+float(error)
    else:
        try:
            time = time_err[:,0]
            err = time_err[:,2]
        except:
            time = time_err[:,0]
            err = time_err[:,1]       

    
    if date is True:
        min = np.min(time)
        phase = time - min
        min2 = np.min(template[:,0])
        template[:,0] = template[:,0] - min2
    else:
        #Convert time to phase
        phase = ((time-float(zero_time))/float(period))-np.floor((time-float(zero_time))/float(period))  
    
    #Interpolate template
    mlc = interpolate.interp1d(template[:,0], template[:,1], kind='linear')
    
    #Create array with phase, mag, and error in each row
    if date is True:
        l = phase.shape[0]
        for i in range(l):
            if phase[i] > np.max(template[:,0]):
                phase[i] = np.nan
                err[i] = np.nan
        phase=phase[~np.isnan(phase)]
        err=err[~np.isnan(err)]
    err = np.transpose(err)
    if date is True:
        time = phase + min
    model=np.transpose(np.row_stack([phase[:],mlc(phase[:]),err[:],time[:]]))
    
    #Multiply by amplitude
    model[:,1] = model[:,1]*float(amp)
    
    #Add phase offset 
    x = model[:,0] + float(phase_offset)
    subset_x = x > 1
    x[subset_x] -= 1
    model[:,0] = x
    
    #Reorder array
    model = model[model[:,3].argsort()]
    
    #Account for y offset
    if flux is True:
        model[:,1] = model[:,1]+float(amp)-float(max)
        model[:,1] = -model[:,1]
    else:
        model[:,1] = model[:,1]+(float(amp)+float(max))
    
    
    
    return(model)
    
def obs_create():
    '''
    If no observation file is provided, create one
    '''
    time = np.transpose(2456448+5*np.random.random_sample((50,)))
    return(time)
    
def poisson_noise(model,noise_norm,flux):
    '''
    Add Poisson noise to the model lightcurve
    '''
    #Apply Poisson noise to scale Gaussian noise using Poisson statistics
    mean = np.average(model[:,1])
    if flux is True:
        noise_norm[:] = noise_norm[:]*np.sqrt(model[:,1])
    else:
        noise_norm[:] = noise_norm[:]*np.sqrt(np.power(10,(model[:,1]-mean)/2.5))
    
    return(noise_norm)

def save_model(model,filename,name):
    '''
    Save the model to a file named as per filename
    '''
    
    os.umask(0000)
    
    #Open a file to store results
    try: 
        outfile = open('../storage3/{}/{}'.format(name,filename),'w')
        #outfile = open('/hd1/LCsim/storage3/{}/{}'.format(name,filename),'w')
    except IOError:
        print "[LCsm] File {} could not be opened!".format(filename)
        sys.exit(1)
    
    for line in model:
        outfile.write("{:13.5f} {:.3f} {:.4f} {:.4f}\n".format(line[3],line[1],line[2],line[0]))
    
    #Close outfile
    outfile.close()

def save_noise(noise,name,j):
    '''
    Save the model to a file named as per filename
    '''
    
    os.umask(0000)
    
    #Open a file to store results
    try: 
        outfile = open('../storage3/{}/noise{num:05d}.cur'.format(name,num=j),'w')
        #outfile = open('/hd1/LCsim/storage3/{}/noise{num:05d}.cur'.format(name,num=j),'w')
    except IOError:
        print "[LCsim.py] File {} could not be opened!".format('noise.cur')
        sys.exit(1)
    
    for i in range(noise.shape[0]):
        outfile.write("{:.4f}\n".format(noise[i]))
    
    #Close outfile
    outfile.close()

def sigma_noise(model, sigma):
    '''
    Add Gaussian noise with a definied sigma to the model lightcurve
    '''
    
    l = model.shape[0]
    
    #Grab l samples from a Gaussian distribution 
    #with a mean of 0 and a given sigma
    noise = np.random.randn(l)*float(sigma)
    
    #Apply noise to model
    newmag = model[:,1] + noise[:]
    model[:,1] = newmag
    
    return(model, noise)
# -------------
# Main Function
# -------------
def LCsim_main(args):
    #Create inputs for LCsim_model if not provided
    if args.a is None:
        args.a = 1
    if args.e is None:
        args.e = .01
    if args.o is None:
        args.o = obs_create()
    if args.p is None:
        args.p = np.random.random_sample()
    if args.phase is None:
        args.phase = 0
    if args.max is None:
        if args.min is None:
            args.max = -args.a
        else:
            args.max = float(args.min) - float(args.a)
        
        
    #Create initial model    
    model = LCsim_model(args.templatefile, args.a, args.d, args.e, args.o, args.p, args.phase, args.max, args.z,False)
    
    #Add Gaussian noise based on error
    model, noise_norm = gaussian_noise(model, args.poisson,False)
        
    #Create Gaussian noise based on sigma
    if args.s is not None:
        model, noise = sigma_noise(model, args.s)   
        noise_norm = noise_norm + noise
    
    np.set_printoptions(suppress=True)
    print model
    
    #Save model to file
    save_model(model,args.f,args.name)
    
    #Output info if requested
    if args.i is True:
        print '[Phase Magnitude Error]'
        print model
        print 'Added noise'
        print noise_norm
        print 'Period'
        print args.p
        print 'Scale factor'
        print args.a
        print 'Phase offset'
        print args.phase
        print 'Mean Magnitude'
        print np.average(model[:,1])

if __name__ == '__main__':    
    parser = argparse.ArgumentParser(description="Creates a model lightcurve from a given template.")
    #Input arguments
    parser.add_argument('templatefile', 
                        help="list template file")
    parser.add_argument('-a', metavar='AMP',
                        help='enter desired amplitude of lightcurve')
    parser.add_argument('-d', action = 'store_true',
                        help='use option if template uses date instead of phase')
    parser.add_argument('-e', metavar='ERROR',
                        help="enter size of error bar in mag")
    parser.add_argument('-f', metavar='FILE',  
                        default='model.cur', 
                        help='filename of the output file (Default: model.cur)')
    parser.add_argument('-i', action = 'store_true',
                        help="record options used to simulate observation")
    parser.add_argument('--name', default='./',metavar='PATH_NAME',
                        help="pass path name for writing downloadable files")
    parser.add_argument('-o', metavar='OBSFILE',
                        help="include observation file")
    parser.add_argument("-p", metavar='PERIOD',
                        help="enter period of lightcurve in days")
    parser.add_argument('--phase',
                        help='enter phase offset for lightcurve')
    parser.add_argument("--poisson", action = 'store_true', 
                        help="add Poisson noise")
    parser.add_argument('-s', metavar='SIGMA',
                        help='add Gaussian noise based on listed sigma')
    parser.add_argument('--max', metavar='MAX',
                        help='enter maximum magnitude of lightcurve')
    parser.add_argument('--min', metavar='MIN',
                        help='enter minimum magnitude of lightcurve')
    parser.add_argument('-z',default=0, metavar='DATE',
                        help='enter epoch of zero phase')
    args = parser.parse_args()
    ret = LCsim_main(args)
    sys.exit(ret)
##
#@mainpage 
#@copydetails LCsim.py
