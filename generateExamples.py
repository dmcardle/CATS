#!/usr/bin/env python2.7
"""
This program generates .wav files to be used for testing our algorithm.
"""
import math
import os
import wave, struct

from music import Note


def writeAudioFile(fileName, melody):
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

    # how many harmonics should be calculated for each note?
    numHarmonics = 8

    for note in melody:
        print("%s = %.2fHz" %(note.noteName, note.freq))
        
        # fundamental frequency
        f0 = note.freq

        # calculate frequencies of f0 + overtones
        harmonics = [f0 * 2**(i) for i in range(numHarmonics+1)]

        for i in range( int(note.duration * 2 * 44100) ):

            # calculate the amplitude for this timestep
            value = 0
            for (hNum, hFreq) in enumerate(harmonics):
                # calculate value of sine wave with frequency h at this point in time
                value += 100 * math.sin(hFreq * i * 2. * math.pi / 44100.) * (1./2)**hNum
           
            # pack value into a short
            packedValue = struct.pack('h', value)

            # save the short to the .wav file
            waveWriter.writeframes(packedValue)

    waveWriter.close()

if __name__ == '__main__':
    # baker street melody
    bakerStreetMelody = [
        Note('A3',1/3.),
        Note('F4',1/2.),
        Note('E4',1/2.),
        Note('D4',1/6.),
        Note('C4',1/6.),
        Note('D4',1/8.),
        Note('E4',1/8.),
        Note('D4',1.)
    ]
    writeAudioFile('bakerStreet.wav', bakerStreetMelody)

    # A minor scale
    scaleAminor = [
        Note('A1',1/2.),
        Note('B1',1/2.),
        Note('C2',1/2.),
        Note('D2',1/2.),
        Note('E2',1/2.),
        Note('F2',1/2.),
        Note('G2',1/2.),
        Note('A2',1/2.),
    ]
    writeAudioFile('A_minor.wav', scaleAminor)
