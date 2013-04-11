#!/usr/bin/env python2.7

import sys # for command-line arguments

import numpy as np
from matplotlib.axes import Axes

from scipy.ndimage.filters import sobel
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

    
        # SPECTROGRAM
        # documentation at
        # http://matplotlib.org/api/pyplot_api.html?highlight=specgram#matplotlib.pyplot.specgram
        # 
        # this call to specgram is precise with regard to frequencies, but
        # blurry in time domain
        (Pxx, freqs, bins, im) = pylab.specgram( self.data, Fs=self.rate,
            NFFT=2**12, noverlap=2**8, sides='onesided', scale_by_freq=True)


        # ------------------------
        # [BEGIN] identify runs of notes 
        # ------------------------

        # how many instantaneous spectra did we calculate
        (numBins, numSpectra) = Pxx.shape

        # how many seconds in entire audio recording
        numSeconds = float(self.data.size) / self.rate
        
        # sobel edge detect
        #edges = np.zeros( Pxx.shape )
        #sobel(Pxx, output=edges)
        #pylab.imshow(edges)

        #pylab.figure()
        #pylab.pcolor( np.arange(0, self.data.size), freqs, Pxx )
       
        
        # ------------------------
        # END [identify runs of notes]
        # ------------------------

        pylab.show()

		
	def noteElimination(N, D):

		#Deletes some of the note candidates in an attempt to find the correct note intended

		#N is the array of note energies
		#D is the array of note durations

		#C is the array of candidates
		#E is the array of eliminated notes


		#initialize the variables
		sum = 0;
		i = 1;


		#calculate the minAvgNoteEnergy

		for x in range(1, len(N)):
			sum = sum + N[x]

		minAvgNoteEnergy = sum/len(N)

		#eliminate low energy notes

		for y in range(1, len(N)):
			if (N[j] < minAvgNoteEnergy):

				#note is no longer a candidate, so place in eliminated notes
				E[i] = N[y]

			else:
				C[i] = N[y] #put the note in the possible candidates
				i=i+1


		#calculate the minimum trajectory length

		D.sort()
		minTrajLen = D[1]


		#eliminate short duration notes

		for j in range(1, len(N)):
			if D[j] < minTrajLen:

				#eliminate note
				E[end+1] = N[j]

			else:
				#note is a candidate
				C[end+1] = N[j]
				i=i+1


		#finds and eliminates harmonics



		for z in range(1, len(C)):
			for a in range(z+1, len(C)):
				#If the energy of the higher note is less than half of
				#the energy of the lower note, the higher one is eliminated
				if (C[a]*.5 > C[z]):

					#keep lower note as candidate
					C[end+1] = C[a]

					#eliminate higher note
					E[end+1] = C[z]


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


