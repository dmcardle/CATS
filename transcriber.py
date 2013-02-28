#!/usr/bin/env python2.7

import numpy
import scipy

from music import Note
from audioFiles import *


class Transcriber:
    """Takes an audio file in and creates a list of measures"""
    def __init__(self, fileName):
        self.measures = []
        
        (rate, data) = readAudioFile(fileName)

        if type(data[0]) == numpy.ndarray:
            data = map( lambda x: numpy.average(x), data)
        
        self.rate = rate
        self.data = data

    def detectNotes(self):
        pylab.specgram( self.data, NFFT=2**11, noverlap=2**9 )
        pylab.show()

if __name__ == '__main__':
    #transcriber = Transcriber('examples/GuitarSample.wav')
    transcriber = Transcriber('examples/A_minor.wav')
    
    transcriber.detectNotes()
  
    # plot the waveform 
    """ 
    audio = transcriber.data
    pylab.figure()
    pylab.title("waveform")
    pylab.plot(audio)
    pylab.show() 
    """
