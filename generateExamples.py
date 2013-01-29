#!/usr/bin/env python
"""
This program generates .wav files to be used for testing our algorithm.
"""
import math
import re
import wave, struct


class Note:
    """This class will be used for finds the frequency associated with a note
    name given in scientific pitch notation."""
    
    C0_FREQUENCY = 16.352
    NOTE_NAMES = [
            ["C"],
            ["C#", "Db"],
            ["D"],
            ["D#", "Eb"],
            ["E"],
            ["F"],
            ["F#", "Gb"],
            ["G"],
            ["G#", "Ab"],
            ["A"],
            ["A#","Bb"],
            ["B"], 
        ]

    def __init__(self, noteName, durationSec):
        """noteName should be scientific pitch name, e.g. A0. durationSec is
        how long the note lasts in seconds."""
        self.noteName = noteName
        self.freq = self.calcFreq()
        self.duration = durationSec

    def calcFreq(self):
        """Parse the noteName according to Scientific Pitch Notation and give the frequency"""

        # find octave and note name
        noteName = re.findall(r"[ABCDEFG][#b]?", self.noteName) 
        noteName = noteName[0]
        
        octaveNum = re.findall(r"\d+", self.noteName)
        if len(octaveNum) > 0:
            octaveNum = int(octaveNum[0])
        else:
            octaveNum = ''
        
        # find note position
        for toneNum, nameArr in enumerate(Note.NOTE_NAMES):
            for name in nameArr:
                if name == noteName:
                    notePos = toneNum
                    break

        # calculate half steps from our basefrequency
        halfSteps = notePos
        if (octaveNum != ''):
            halfSteps += 12*octaveNum

        # determine frequency based on number of half steps
        freq = Note.C0_FREQUENCY * 2**(halfSteps / 12.0)

        return freq

def writeAudioFile(fileName, melody):
    """Given a fileName (including .wav at end) and a melody (array of Note
    objects), synthesize a wav file"""

    print "Generating audio file for '%s'" % fileName
    
    waveWriter = wave.open(fileName, 'w')
    waveWriter.setnchannels(1)
    waveWriter.setsampwidth(4)
    waveWriter.setframerate(44100)

    # how many harmonics should be calculated for each note?
    numHarmonics = 4

    for note in melody:
        print("%s = %.2fHz" %(note.noteName, note.freq))
        
        # fundamental frequency
        f0 = note.freq

        # calculate frequencies of f0 + overtones
        harmonics = [f0 * 2**(i) for i in range(numHarmonics+1)]

        for i in range( int(note.duration * 2 * 44100) ):

            # calculate the amplitude for this timestep
            value = 0
            for hFreq in harmonics:
                # calculate value of sine wave with frequency h at this point in time
                value += 100 * math.sin(hFreq * i * 2. * math.pi / 44100.)
           
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
    writeAudioFile('examples/bakerStreet.wav', bakerStreetMelody)

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
    writeAudioFile('examples/A_minor.wav', scaleAminor)
