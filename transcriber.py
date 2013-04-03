#!/usr/bin/env python2.7

import sys # for command-line arguments

import numpy as np
from scipy.signal import argrelmax
from scipy import interpolate
#from scipy.signal import find_peaks_cwt

from music import Note
from audioFiles import *


class Transcriber:
    """Takes an audio file in and creates a list of measures"""
    def __init__(self, fileName):
        self.measures = []
        
        (rate, data) = readAudioFile(fileName)

        # if there are multiple channels
        if len(data.shape) > 1:
            # select channel 0
            data = data[:,0]

        self.rate = rate
        self.data = data

    def detectNotes(self):

        def smooth2d( grid, nPointsX, nPointsY):
            """Interpolate grid, inserting `nPointsX` points in between each X
            coordinate and `nPointsY` between each Y."""
            numRow,numCol = grid.shape
            x = range(0, numCol)
            y = range(0, numRow)
            f = interpolate.interp2d(x, y, grid, kind='linear')

            xNew = np.arange(0, numCol, 1./nPointsX)
            yNew = np.arange(0, numCol, 1./nPointsY)
            gridNew = f(xNew, yNew)

            return gridNew

        def smooth( signal, nPoints ):
            xVals = range(len(signal))
            s = interpolate.InterpolatedUnivariateSpline(xVals, signal)
            xValsNew = np.linspace(0, len(signal), nPoints)
            smoothed = s(xValsNew) 
            return smoothed
    
    
        # SPECTROGRAM
        # documentation at
        # http://matplotlib.org/api/pyplot_api.html?highlight=specgram#matplotlib.pyplot.specgram
        (Pxx, freqs, bins, im) = pylab.specgram( self.data, Fs=self.rate,
            NFFT=2**12, noverlap=2**8, sides='onesided')

        # how many instantaneous spectra did we calculate
        (numBins, numSpectra) = Pxx.shape

        # how many seconds in entire audio recording
        numSeconds = float(self.data.size) / self.rate

        """
        lastFreqsAtPeaks = []
        for x in range(numSpectra):

            # iSpec is instantaneous spectrum
            iSpec = Pxx[:, x]
            
            if x % 10 == 0:
                print "%f.2%% done" % (100.*x / numSpectra)

            # TODO REMOVE
            if x > 100:
                break

            # find list of peak indices in the instantaneous spectrum
            peakInd = argrelmax(iSpec, order=10)

            # convert position of peak in spectrum to a frequency
            # value in Hz
            freqsAtPeaks = [freqs[i] for i in np.nditer(peakInd)]

            t = 1.*numSeconds*x/numSpectra

            for f in freqsAtPeaks:

                # --- select only frequencies that were
                # --- found in the last iSpec
                keep = False
                tol = 5   # define frequency tolerance
                for fOld in lastFreqsAtPeaks:
                    if fOld-tol <= f <= fOld+tol:
                        keep = True
                # ------------------------------------

                if keep:
                    # draw a patch
                    pylab.gca().add_patch(
                        pylab.Rectangle((t,f), 0.005, 100))

            lastFreqsAtPeaks = freqsAtPeaks

        """

        pylab.show()

if __name__ == '__main__':

    print sys.argv
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        transcriber = Transcriber(filename)
        transcriber.detectNotes()

    else:
        print "Specify a .wav file!"

  
    # plot the waveform 
    """ 
    audio = transcriber.data
    pylab.figure()
    pylab.title("waveform")
    pylab.plot(audio)
    pylab.show() 
    """


