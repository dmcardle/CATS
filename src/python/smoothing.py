#!/usr/bin/env python2.7

import numpy as np
import scipy as sp

import matplotlib
matplotlib.use('MacOSX')
import pylab

import math
from random import random
from scipy import interpolate
from numpy.random import randn

def smooth( xVals, signal, windowLen=10 ):
   
    s = np.r_[xVals[windowLen-1:0:-1],xVals,xVals[-1:windowLen:-1]]
    w = np.blackman(windowLen)
    y = np.convolve(w/w.sum(), s, mode='valid')
    return y


if __name__ == '__main__':

    # generate the corrupted y values for given x values
    xVals = np.arange(0, 4*math.pi, 0.5)
    yVals = np.sin(xVals) + randn(len(xVals)) * 0.333



    # smooth data
    yValsSmooth = smooth(xVals, yVals, 10)  


    # plot the values
    pylab.figure(1)
    pylab.title("smoothing noisy data sin(x)")
    pylab.plot(xVals, yVals, 'o-')

    print xVals
    print yValsSmooth

    xValsSmooth = sp.linspace(0, 4*math.pi, num=yValsSmooth.size)

    pylab.plot(xValsSmooth, yValsSmooth, color='red')

    pylab.show()
