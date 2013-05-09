#!/usr/bin/env python2.7

import re   # regular expressions
from math import log

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

    def __init__(self, noteName=None, durationSec=None, freq=None):
        """noteName should be scientific pitch name, e.g. A0. durationSec is
        how long the note lasts in seconds."""
        self.noteName = noteName
        
        if freq != None:
            self.freq = freq
        else:
            self.freq = self.calcFreq()

        self.duration = durationSec


    def calcFreq(self):
        """Parse the noteName according to Scientific Pitch Notation and give
        the frequency"""

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
       
    @staticmethod
    def getNoteName(freq, useFlats=True):
        """Get the note name associated with the specified frequency. If
        useFlats parameter is not set to False, the returned string will
        default to using flats as the note name convention."""
        # number of half steps from note C0
        totalHalfStepsFromC = int(round(log(freq/Note.C0_FREQUENCY) * 12.0 / log(2)))

        # which octave in Scientific Pitch Notation
        octave = int(totalHalfStepsFromC / 12.)
        
        # how many half steps from closest C below note
        halfSteps = totalHalfStepsFromC % 12
       
        noteName = Note.NOTE_NAMES[halfSteps]

        # if this note has more than one name, figure out which representation
        # to use
        if len(noteName) > 1:
            if useFlats:
                noteName = noteName[1]
            else:
                noteName = noteName[0]
        else:
            # extract the single item from the list
            noteName = noteName[0]
             
        # express in Scientific Pitch Notation
        sciPitchNoteName = '%s%d' % (noteName, octave)
    
        return (noteName, octave, sciPitchNoteName)

if __name__ == '__main__':
    print Note.getNoteName(440)
    print Note.getNoteName(220, useFlats=False)

