#!/usr/bin/env python2.7

import math
import os
import wave
import struct
import scipy.io.wavfile

import platform

import matplotlib

operatingSystem = platform.system()
if operatingSystem == 'Linux':
    matplotlib.use('GTK')
elif operatingSystem == 'Darwin':
    matplotlib.use('MacOSX')
elif operatingSystem == 'Windows':
    matplotlib.use('TkAgg')


matplotlib.use('Agg')
import pylab

def readAudioFile(fileName):
    """returns tuple (sampleRate, data)"""
    # invoke scipy to read file for us 
    (rate,data) = scipy.io.wavfile.read(fileName)
    return (rate, data)

if __name__ == '__main__':
    readAudioFile('examples/A_minor.wav')


def writeAudioFile(fileName, melody, numHarmonics=4):
    """Given a fileName (including .wav at end) and a melody (array of Note
    objects), synthesize a wav file"""

    print "Generating audio file for '%s'" % fileName
   
    if not os.path.exists('examples'):
        os.makedirs('examples')
    
    fileName = 'examples/%s' % fileName
    
    waveWriter = wave.open(fileName, 'w')
    waveWriter.setnchannels(1)
    waveWriter.setsampwidth(4)
    waveWriter.setframerate(44100)

    for note in melody:
        print("%s = %.2fHz" %(note.noteName, note.freq))
        
        # fundamental frequency
        f0 = note.freq

        # calculate frequencies of f0 + overtones
        harmonics = [f0 * 2**(i) for i in range(numHarmonics+1)]

        numAmplitudes = int(note.duration * 2 * 44100) 

        for i in range(numAmplitudes):

            # calculate the amplitude for this timestep
            value = 0
            for (hNum, hFreq) in enumerate(harmonics):
                # determine intensity of sound wave based on position in note duration
                intensity = 100 * math.sin( math.pi*i/numAmplitudes )

                # calculate value of sine wave with frequency h at this point in time
                value += intensity * math.sin(hFreq * i * 2. * math.pi / 44100.) * (1./2)**hNum
           
            # pack value into a short
            packedValue = struct.pack('h', value)

            # save the short to the .wav file
            waveWriter.writeframes(packedValue)

    waveWriter.close()
