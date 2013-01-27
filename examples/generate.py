"""
This program will be used to generate audio test files. These test files will
be read in by the sheet music writer.
"""
import math
import re

class Note:
    """This class will be used for finding the frequency associated with a note
    name"""
    
    A0_FREQUENCY = 27.5

    def __init__(self):
        pass 

    def getFreq( noteName ):
        """Parse the noteName param according to Scientific Pitch Notation and give the frequency"""

        # find octave and note name
        octaveNum = re.findall("\d+", noteName)
        noteName = re.findall("(A|B|C|D|E|F|G)(#|b|)", noteName) 

        # calculate half steps from our base A0 frequency
        
        # determine frequency based on number of half steps

        return 0

def writeAudioFile(melody):
    for noteName in melody:
        freq = Note.getFreq(noteName)

if __name__ == '__main__':
    # baker street melody
    bakerStreetMelody = ['A', 'F', 'E', 'D', 'C', 'D']

