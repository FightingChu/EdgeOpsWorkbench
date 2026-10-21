import unittest
from edgeops.codecs.sequence import SequenceTracker

class SequenceTests(unittest.TestCase):
    def test_duplicates_gaps_and_old_sequences(self):
        state=SequenceTracker(); state.observe('a',4)
        self.assertEqual(state.observe('a',4)['status'],'duplicate')
        self.assertEqual(state.observe('a',7)['missing'],2)
        self.assertEqual(state.observe('a',6)['status'],'old')
    def test_uint32_wrap(self):
        state=SequenceTracker(); state.observe('a',2**32-1)
        self.assertEqual(state.observe('a',0)['status'],'next')
