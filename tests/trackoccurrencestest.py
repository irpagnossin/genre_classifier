import unittest
from trackoccurrences import TrackOccurrences


class TestTrackOccurrencesMinimum1(unittest.TestCase):

    def test_1(self):
        d = TrackOccurrences()
        with self.assertRaises(KeyError):
            d.get_occurrences(0)

    def test_2(self):
        d = TrackOccurrences()
        d.add(2, 4)
        self.assertEqual(d.get_occurrences(2), {0: 1})

    def test_3(self):
        d = TrackOccurrences()

        d.add(2, 4)
        self.assertEqual(d.get_occurrence(2,4), 1)

        d.add(2, 4)
        self.assertEqual(d.get_occurrence(2,4), 2)

        for i in range(10):
            d.add(2, 4)

        self.assertEqual(d.get_occurrence(2,4), 12)

    def test_4(self):
        d = TrackOccurrences()
        d.add(2, 4)
        d.add(2, 0)
        d.add(2, 0)
        self.assertEqual(d.get_occurrences(2), {0: 1, 1: 2})

    def test_5(self):
        d = TrackOccurrences()

        d.add(20, 100)
        self.assertEqual(d.get_occurrences(20), {0: 1})
        self.assertEqual(d.get_occurrence(20, 100), 1)

        d.add(20, 98)
        self.assertEqual(d.get_occurrences(20), {0: 1, 1: 1})
        self.assertEqual(d.get_occurrence(20, 98), 1)
        with self.assertRaises(KeyError):
            d.get_occurrence(20, 0)

        d.add(55, 98)
        d.add(55, 98)
        self.assertEqual(d.get_occurrences(55), {1: 2})
        self.assertEqual(d.get_occurrence(55, 98), 2)
        with self.assertRaises(KeyError):
            d.get_occurrence(55, 1)


class TestTrackOccurrencesMinimum2(unittest.TestCase):

    def test_1(self):
        d = TrackOccurrences(2)
        with self.assertRaises(KeyError):
            d.get_occurrences(0)

    def test_2(self):
        d = TrackOccurrences(2)
        d.add(2, 4)

        with self.assertRaises(KeyError):
            d.get_occurrences(2)

        with self.assertRaises(KeyError):
            d.get_occurrence(2, 4)

    def test_3(self):
        d = TrackOccurrences(2)
        d.add(2, 4)
        d.add(2, 4)
        self.assertEqual(d.get_occurrences(2), {0: 2})

    def test_4(self):
        d = TrackOccurrences(2)
        d.add(2, 1)
        d.add(2, 3)

        self.assertEqual(d.get_occurrence(2, 1), 1)
        self.assertEqual(d.get_occurrence(2, 3), 1)
        self.assertEqual(d.get_occurrences(2), {0: 1, 1: 1})

    def test_5(self):
        d = TrackOccurrences(2)

        d.add(2, 1)
        with self.assertRaises(KeyError):
            d.get_occurrence(2, 1)

        with self.assertRaises(KeyError):
            d.get_occurrences(2)

        d.add(3, 1)
        with self.assertRaises(KeyError):
            d.get_occurrence(3, 1)

        with self.assertRaises(KeyError):
            d.get_occurrences(3)

        d.add(3, 1)
        self.assertEqual(d.get_occurrence(3, 1), 2)
        self.assertEqual(d.get_occurrences(3), {0: 2})

        with self.assertRaises(KeyError):
            d.get_occurrence(2, 1)

        with self.assertRaises(KeyError):
            d.get_occurrences(2)

        d.add(2, 1)
        self.assertEqual(d.get_occurrence(2, 1), 2)
        self.assertEqual(d.get_occurrences(2), {0: 2})

    def test_6(self):
        d = TrackOccurrences(2)

        d.add(2, 1)
        d.add(3, 1)
        d.add(3, 1)
        d.add(2, 1)
        d.add(3, 2)

        self.assertEqual(d.get_occurrence(3, 1), 2)
        self.assertEqual(d.get_occurrence(3, 2), 1)
        self.assertEqual(d.get_occurrences(3), {0: 2, 1: 1})

        self.assertEqual(d.get_occurrence(2, 1), 2)
        self.assertEqual(d.get_occurrences(2), {0: 2})
        with self.assertRaises(KeyError):
            d.get_occurrence(2, 2)


class TestTrackOccurrencesMinimum10(unittest.TestCase):

    def test_1(self):
        d = TrackOccurrences(10)

        for i in range(9):
            d.add(2, 5)

        for i in range(15):
            d.add(3, 5)

        with self.assertRaises(KeyError):
            d.get_occurrence(2, 5)

        with self.assertRaises(KeyError):
            d.get_occurrences(2)

        self.assertEqual(d.get_occurrence(3, 5), 15)
        self.assertEqual(d.get_occurrences(3), {0: 15})

        d.add(2, 5)

        self.assertEqual(d.get_occurrence(2, 5), 10)
        self.assertEqual(d.get_occurrences(2), {0: 10})

        for i in range(15):
            d.add(3, 200)

        self.assertEqual(d.get_occurrence(3, 5), 15)
        self.assertEqual(d.get_occurrence(3, 200), 15)
        self.assertEqual(d.get_occurrences(3), {0: 15, 1: 15})

if __name__ == '__main__':
    unittest.main()
