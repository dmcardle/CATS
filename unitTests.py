import unittest
import generateExamples


class TestExampleGenerator(unittest.TestCase):
    def setUp(self):
        pass 
    
    def testNoteGetFreq(self):
        n = generateExamples.Note("A3", 1)

        # round frequency to integer
        f = int(n.freq + 0.5)
        self.assertEqual(f, 220)    
        
        n = generateExamples.Note("A4", 1)
        
        f = int(n.freq + 0.5)
        self.assertEqual(f, 440)

if __name__ == '__main__':
    unittest.main()
