import numpy
import scipy
import pylab # (matplotlib)

from music import Note
from audioFiles import *



class Transcriber:
    """Takes an audio file in and creates a list of measures"""
    def __init__(self, fileName):
        self.measures = []
        
        (rate, data) = readAudioFile(fileName)
        self.rate = rate
        self.data = data

    def detectNotes( iSpec ):
        """Detect notes in the instantaneous spectrum, iSpec"""

if __name__ == '__main__':
    transcriber = Transcriber('examples/A_minor.wav')

