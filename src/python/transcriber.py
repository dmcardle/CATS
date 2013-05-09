#!/usr/bin/env python2.7

from music import Note
from audioFiles import *

import sys # for command-line arguments
from collections import deque

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

        smoothAudio = Transcriber.smooth( self.data )

        (Pxx, freqs, bins, im) = pylab.specgram( smoothAudio, Fs=self.rate,
            NFFT=2**12, noverlap=2**8, sides='onesided', scale_by_freq=True)


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


        def findPeaks( sample, minPeakVal=None):
            peakPos = []
            peakVal = []
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

                    if lastSlopeNeg != None and (not lastSlopeNeg) and thisSlopeNeg:
                        if minPeakVal != None and sample[i] >= minPeakVal:
                            peakPos.append(i)
                            peakVal.append(sample[i+1])

                    lastSlopeNeg = thisSlopeNeg
           
            # TODO some sort of statistical analysis of the significance of the
            # peaks found. For now, I'll just have a magic number representing
            # the minimum peak value.
            
            return (peakPos, peakVal)


        # TODO find the optimal value of minPeakVal based on the spectrogram
        # determine thresholding value
        thresh = np.mean( Pxx )

        FREQ_THRESH = 10 
        lastNotes = [] 
        prevF0NoteNamesSciPitchQueue = deque(maxlen=5)
        def recentlySaw( noteNameSciPitch ):
            #print prevF0NoteNamesSciPitchQueue
            for prevF0NoteNames in prevF0NoteNamesSciPitchQueue:
                if noteNameSciPitch in prevF0NoteNames:
                    return True
            return False

        for t in range(0, numSpectra):

            print "-----------------------"

            # extract a block from the spectrogram
            sample = Pxx[:, t]
            sample = Transcriber.smooth( sample )

            #print "SHAPE OF sample:", sample.shape

            # find the peaks in this profile (peaks represent notes)
            (peakPos, peakVal) = findPeaks(sample, minPeakVal=thresh)

            # determine which notes found are new (don't exist in the last
            # notes list)
            newPeaks = []

            noteNames = []

            def freqsAreSameNote( f1, oct1, f2, oct2):
                # scale freqs
                f1 = f1 / 2**oct1
                f2 = f2 / 2**oct2
                return abs(f1-f2) < FREQ_THRESH


            prevF0NoteNames = []
            # Go through notes backwards, from high to low.
            # Variable i represents peak number.
            for i in reversed(range(len(peakPos))):

                # Variable pos represents at which y-value in spectrogram this
                # peak was found. Variable intensity contains the intensity at
                # that peak; how much energy at that frequency.
                pos = peakPos[i]
                intensity = peakVal[i]


                f = freqs[pos]
                if 20 <= f <= 20000: # if it is audible to a human...

                    (noteName, octave, sciPitchNoteName) = Note.getNoteName( f )
                    noteNames.append(sciPitchNoteName)
                     
                    # attempt to find fundamental frequency of this note
                    f0 = None
                    f0Pos = None
                    for j in range( i ):
                        otherFreq = freqs[ peakPos[j] ]
                        otherIntensity = peakVal[j]
                        (otherNoteName, otherOctave, otherSciPitch) = Note.getNoteName( otherFreq )

                        if freqsAreSameNote( f, octave, otherFreq, otherOctave) \
                           and intensity <= 0.5*otherIntensity \
                           and 20 <= otherFreq <= 20000:

                            # compute frequency of f moved down some number of
                            # octaves
                            f0 = f / 2.0**(octave-otherOctave)
                            f0Pos = j
                            break


                    if f0 != None :

                        (f0NoteName, f0Octave, f0SciPitch) = Note.getNoteName(f0)
                        print "f0 = %f" % f0
                        print "recently saw %s? %s" % (f0SciPitch, recentlySaw(f0SciPitch))

                        # if we found an f0 and we haven't already handled it
                        if (f0SciPitch not in prevF0NoteNames) \
                            and (not recentlySaw( f0SciPitch )) \
                            and (f0SciPitch not in lastNotes):
                            prevF0NoteNames.append(f0SciPitch)

                            #print "%s @ %.2fHz" % (f0SciPitch, f0)
                    
                            # Annotate the spectrogram. Note that circles plotted actually
                            # appear as horizontal lines thanks to our logarithmic y scale.
                            time = (1.0*t / numSpectra) * numSeconds;
                            circle = plt.Circle( (time, f), 0.01, color='w')
                            fig.gca().add_artist(circle)

                            xPos = 1.0*t / numSpectra
                            yPos = f / freqs[-1]       # y position = f0 / max freq

                            plt.text( xPos, yPos, f0SciPitch, transform=fig.gca().transAxes)


                    # determine if this note is a harmonic... 
                    thisNoteIsHarmonic = False

            lastNotes = noteNames

            # save the F0s encountered in this time slice
            prevF0NoteNamesSciPitchQueue.append( prevF0NoteNames )




        # ------------------------
        # END [identify runs of notes]
        # ------------------------

        pylab.show()

        


if __name__ == '__main__':

    # Determine which file to read
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        transcriber = Transcriber(filename)
        transcriber.detectNotes()
    else:
        print "Specify a .wav file!"

