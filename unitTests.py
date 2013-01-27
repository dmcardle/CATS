import unittest
import generateExamples


class TestExampleGenerator(unittest.TestCase):
    def setUp(self):
        pass 
    
    def testNoteGetFreq(self):
        n = generateExamples.Note()

        # round frequency to integer
        f = int( n.getFreq("A3") + 0.5)

        self.assertEqual(f, 220)    

if __name__ == '__main__':
    unittest.main()
