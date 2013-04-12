#!/usr/bin/env python2.7
"""
This program generates .wav files to be used for testing our algorithm.
"""

from music import Note
from audioFiles import writeAudioFile


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
