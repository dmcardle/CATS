#!/usr/bin/env python2.7

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

        if type(data[0]) == np.ndarray:
            data = map(np.average, data)
        
        self.rate = rate
        self.data = data

    def detectNotes(self):
        (Pxx, freqs, bins, im) = pylab.specgram( self.data, Fs=self.rate,
            NFFT=2**11, noverlap=2**9, sides='onesided' )

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
     
     
        # smooth the spectrogram
        nPointsSmooth = 1
        
        PxxSmooth = smooth2d( Pxx, 1, nPointsSmooth ) 
        

        pylab.matshow(Pxx)

        pylab.show()
        return
        

        # how many instantaneous spectra did we calculate
        (numBins, numSpectra) = PxxSmooth.shape

        # how many seconds in entire audio recording
        numSeconds = float(self.data.size) / self.rate

        # put n points between each frequency bin

        # iSpec is instantaneous spectrum
        for x in range(numSpectra):

            iSpec = PxxSmooth[:, x]


            if x % 10 == 0:
                print "%f.2%% done" % (100.*x / numSpectra)

            # TODO REMOVE
            if x > 30:
                break

            # find list of peak indices in the instantaneous spectrum
            peakInd = argrelmax(iSpec, order=10)

            for i in np.nditer(peakInd):

                # convert position of peak in spectrum to a frequency
                # value in Hz
                f = 1.*freqsSmooth[i]
                
                #print "f = "
                #print f

                #print "freqs = "
                #print freqs.size

                # calculate time in seconds
                t = 1. *numSeconds * x / numSpectra

                #print "type of f = %s" % type(f)
                #print "type of t = %s" % type(t)


                #print "%.2fHz at %.2fs" % (f,t)

                # draw a patch
                pylab.gca().add_patch(
                    pylab.Rectangle((t,f), 0.005, 100))

        pylab.show()

if __name__ == '__main__':
    #transcriber = Transcriber('examples/GuitarSample.wav')
    #transcriber = Transcriber('examples/A_minor.wav')
    transcriber = Transcriber('examples/bakerStreet.wav')
    
    transcriber.detectNotes()
  
    # plot the waveform 
    """ 
    audio = transcriber.data
    pylab.figure()
    pylab.title("waveform")
    pylab.plot(audio)
    pylab.show() 
    """


