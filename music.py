#!/usr/bin/env python2.7

import re   # regular expressions

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
        def findNotePos(noteName):
            for toneNum, nameArr in enumerate(Note.NOTE_NAMES):
                for name in nameArr:
                    if name == noteName:
                        return toneNum

        notePos = findNotePos(noteName)

        # calculate half steps from our basefrequency
        halfSteps = notePos
        if (octaveNum != ''):
            halfSteps += 12*octaveNum

        # determine frequency based on number of half steps
        freq = Note.C0_FREQUENCY * 2**(halfSteps / 12.0)

        return freq

