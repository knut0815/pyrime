#!/usr/bin/env python2.7

import numpy as np
import pickle
from sys import argv, exit
from os import path

import matplotlib.pylab as plt

try:
    FILE = argv[1]
except:
    print "Usage:",argv[0],"FILE_PATH"
    print "FILE_PATH: path to the file containing the Fourier parameters"
    print "The file must contain at least five columns, with the first feive being:"
    print "1: the name of the variable"
    print "2: the period of the variable"
    print "3: the amplitude of the first Fourier harmonic in the I-band"
    print "4: the amplitude of the second Fourier harmonic in the I-band"
    print "5: the epoch-independent phase difference phi31 in the I-band"
    exit()

try:
    names, periods, A1s, A2s, phi31s = np.loadtxt(FILE,
                                                  usecols=[0,1,2,3,4],
                                                  unpack=True,
                                                  dtype='|S30,<f8,<f8,<f8,<f8')
except:
    print "Error reading datafile"
    exit()

try:
    npzfile = np.load(path.dirname(__file__)+'/pyrime_const.npz')
    cut     = npzfile['cut']
    const_p = npzfile['const_p']
except:
    print "pyrime_const.npz file not found"
    exit()

try:
    clf = pickle.load( open( path.dirname(__file__)+"/pyrime_correct.pkl", "rb" ))
except:
    print "pyrime_correct.pkl not found!"
    exit()

feh_eq3 = -6.125 -4.795 * periods + 1.181 * phi31s + 7.876 * A2s
feh_final = np.zeros_like(feh_eq3)

periods_r = periods - (const_p[0] + const_p[1] *A1s + const_p[2] *A1s**2 + const_p[3] * A1s**3)

oo1 = (periods_r < cut[0] + feh_eq3*cut[1])
oo2 = np.logical_not(oo1)

feh_final[oo1] = feh_eq3[oo1] - clf.predict(A1s[oo1].reshape(-1,1)).reshape(1,-1)[0] - 1.05
feh_final[oo2] = feh_eq3[oo2]

for i in xrange(feh_final.size):
    if oo1[i] == True:
        print names[i], '{:+5.3f}'.format(feh_final[i]), "OoI"
    else:
        print names[i], '{:+5.3f}'.format(feh_final[i]), "OoII"


