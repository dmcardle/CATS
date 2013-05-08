import unittest
from music import Note
import transcriber

"""This is where all unit tests go."""

class TestExampleGenerator(unittest.TestCase):
    def setUp(self):
        pass 
    
    def testNoteGetFreq(self):
        n = Note("A3", 1)

        # round frequency to integer
        f = int(n.freq + 0.5)
        self.assertEqual(f, 220)    
        
        n = Note("A4", 1)
        
        f = int(n.freq + 0.5)
        self.assertEqual(f, 440)
		
    def testNoteElim(self):
        t = transcriber.Transcriber()
        e = t.noteElimination([220, 440, 450, 500, 550], [.5, 1, .7, .8, .4])
        self.assertEqual(e, [440])

if __name__ == '__main__':
    unittest.main()
