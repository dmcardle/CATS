#!/usr/bin/env python2.7

from music import Note
from audioFiles import *

import sys # for command-line arguments

import numpy as np
import matplotlib.pyplot as plt



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


    @staticmethod
    def smooth(signal):
        """Return a smoothed version of signal with length n-1, computed by
        averaging adjacent values."""

        n = len(signal)
        newSignal = np.ndarray( n-1 )
        
        for (i, val) in enumerate(signal):
            if i < len(signal) - 1:
                # avoid an integer overflow by distributing 1/2
                newSignal[i] = signal[i]/2.0 + signal[i+1]/2.0

        return np.array(newSignal)


    def detectNotes(self):
        """Detect the notes in the audio recording self.data.  Plots a
        spectrogram with detected notes labelled."""
        
        fig = pylab.figure()
        fig.suptitle('Track Detection')

        # SPECTROGRAM
        # documentation at
        # http://matplotlib.org/api/pyplot_api.html?highlight=specgram#matplotlib.pyplot.specgram
        # 
        # this call to specgram is precise with regard to frequencies, but
        # blurry in time domain
        (Pxx, freqs, bins, im) = pylab.specgram( self.data, Fs=self.rate,
            NFFT=2**11, noverlap=2**5, sides='onesided', scale_by_freq=True)

        smoothAudio = Transcriber.smooth( self.data )



        print "SHAPE OF freqs", freqs.shape

        # ------------------------
        # [BEGIN] identify runs of notes 
        # ------------------------

        # how many instantaneous spectra did we calculate
        (numBins, numSpectra) = Pxx.shape
        print "SHAPE OF Pxx:", Pxx.shape

        # how many seconds in entire audio recording
        numSeconds = float(self.data.size) / self.rate


        scaledPxx = 10 * np.log10(Pxx)




        def findPeaks( list, minPeakVal=None):
            peakPos = []
            lastSlopeNeg = None
            for i in range(0, len(sample)-1):
                # we will be comparing two points on the frequency spectrum at
                # a time
               
                # If the two points are equal, the slope is 0, so we will move
                # on to the next point. For example, if we have the list [0 1 2
                # 2 1 0], there is clearly a peak, but it is between the two 2
                # values
                if (sample[i] != sample[i+1]):
                    thisSlopeNeg = sample[i] > sample[i+1]

                    if lastSlopeNeg != None and not lastSlopeNeg and thisSlopeNeg:
                        if minPeakVal != None and sample[i] >= minPeakVal:
                            peakPos.append(i)

                    lastSlopeNeg = thisSlopeNeg
           
            # TODO some sort of statistical analysis of the significance of the
            # peaks found. For now, I'll just have a magic number representing
            # the minimum peak value.
            
            return peakPos


        # TODO find the optimal value of minPeakVal based on the spectrogram
        # determine thresholding value
        thresh = np.mean( Pxx )


        lastNotes = None

        for t in range(0, numSpectra):

            # extract a block from the spectrogram
            sample = Pxx[:, t]
            #print "SHAPE OF sample:", sample.shape

            # find the peaks in this profile (peaks represent notes)
            peakPos = findPeaks(sample, minPeakVal=thresh)

            # FIXME remove peaks that correspond to overtones of another peak


            # determine which notes found are new (don't exist in the last
            # notes list)
            newNotes = []
            newPeaks = []
            for p in peakPos:
                f = freqs[p]
                note = Note.getNoteName(f)
                if lastNotes != None and note not in lastNotes:
                    newNotes.append(note)
                    newPeaks.append(p)

            # for each of the new peaks, determine the name of the note that is being played
            for p in newPeaks:
                f = freqs[p]
                noteName = Note.getNoteName(f)

                print "%s @ %.2fHz" % (noteName, f)

                # Annotate the spectrogram. Note that circles plotted actually
                # appear as horizontal lines thanks to our logarithmic y scale.
                time = (1.0*t / numSpectra) * numSeconds;
                circle = plt.Circle( (time, f), 0.01, color='w')
                fig.gca().add_artist(circle)

                xPos = 1.0*t / numSpectra
                yPos = f / freqs[-1]

                plt.text( xPos, yPos, noteName, transform=fig.gca().transAxes)


            notes = map( lambda p : Note.getNoteName(freqs[p]), peakPos)
            lastNotes = notes



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

    # Determine which file to read
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        transcriber = Transcriber(filename)
        transcriber.detectNotes()
    else:
        print "Specify a .wav file!"

