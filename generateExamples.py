#!/usr/bin/env python

"""
This program will be used to generate audio test files. These test files will
be read in by the sheet music writer.
"""
import math
import re
import wave, struct


class Note:
    """This class will be used for finding the frequency associated with a note
    name"""
    
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
    
    waveWriter = wave.open(fileName, 'w')
    waveWriter.setnchannels(1)
    waveWriter.setsampwidth(4)
    waveWriter.setframerate(44100)

    numHarmonics = 4
    freqs = []
    delays = []
    durations = []

    time = 0
    for note in melody:
        print("%s = %.2fHz" %(note.noteName, note.freq))
        
        # fundamental frequency
        f0 = note.freq

        # calculate frequencies of f0 + overtones
        harmonics = [f0 * 2**(i) for i in range(numHarmonics)]

        for i in range( int(note.duration * 2 * 44100) ):

            value = 0
            for hFreq in harmonics:
                # calculate value of sine wave with frequency h at this point in time
                value += 100 * math.sin(hFreq * i * 2. * math.pi / 44100.)
           
            #print value
            
            packedValue = struct.pack('h', value)
            waveWriter.writeframes(packedValue)

        time += note.duration   

    waveWriter.close()

if __name__ == '__main__':
    # baker street melody
    bakerStreetMelody = [
        Note('A3',1/3.),
        Note('F4',1/2.),
        Note('E4',1/2.),
        Note('D4',1/6.),
        Note('C4',1/6.),
        Note('D4',1),
    ]

    writeAudioFile('examples/bakerStreet.wav', bakerStreetMelody)

