import numpy
import scipy
import pylab # (matplotlib)

from music import Note

class AudioFileReader:
    def __init__(self):
        self.audioData = []

    def readAudioFile(self, path):
        pass


class Transcriber:
    """Takes an audio file in and creates a list of measures"""
    def __init__(self):
        self.measures = []

    def detectNotes( iSpec ):
        """Detect notes in the instantaneous spectrum, iSpec"""

if __name__ == '__main__':
    transcriber = Transcriber()

