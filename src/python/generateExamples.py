#!/usr/bin/env python2.7
"""
This script generates .wav files to be used for testing our algorithm.
"""

from music import Note
from audioFiles import writeAudioFile

import os


if __name__ == '__main__':

    os.chdir('../../')

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
        Note('A2',1/2.),
        Note('B2',1/2.),
        Note('C3',1/2.),
        Note('D3',1/2.),
        Note('E3',1/2.),
        Note('F3',1/2.),
        Note('G3',1/2.),
        Note('A3',1/2.),
    ]
    writeAudioFile('A_minor.wav', scaleAminor)

    # C major scale
    scaleCMajor = [
        Note('C3',1/2.),
        Note('D3',1/2.),
        Note('E3',1/2.),
        Note('F3',1/2.),
        Note('G3',1/2.),
        Note('A3',1/2.),
        Note('B3',1/2.),
        Note('C4',1/2.),
    ]
    writeAudioFile('C_major.wav', scaleCMajor)
