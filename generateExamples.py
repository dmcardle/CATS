"""
This program will be used to generate audio test files. These test files will
be read in by the sheet music writer.
"""
import math
import re

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

    def __init__(self):
        pass 

    def getFreq(self, noteNameSciPitch ):
        """Parse the noteName param according to Scientific Pitch Notation and give the frequency"""

        # find octave and note name
        noteName = re.findall(r"[ABCDEFG][#b]?", noteNameSciPitch) 
        noteName = noteName[0]
        
        octaveNum = re.findall(r"\d+", noteNameSciPitch)
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

def writeAudioFile(melody):
    for noteName in melody:
        freq = Note.getFreq(noteName)

if __name__ == '__main__':
    # baker street melody
    bakerStreetMelody = ['A', 'F', 'E', 'D', 'C', 'D']


    n = Note()
    f = n.getFreq("A3")
    print(f)
