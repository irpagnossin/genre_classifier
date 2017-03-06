import unittest
from trackcomponents import TrackComponents

class TestTrackComponents(unittest.TestCase):

  def test_1(self):
    d = TrackComponents()
    with self.assertRaises(KeyError):
      d.get(0)

  def test_2(self):
    d = TrackComponents()
    d.add(2,4)
    self.assertEqual(d.get(2), {0:1})

  def test_3(self):
    d = TrackComponents()

    d.add(2,4)
    self.assertEqual(d.get(2,4), 1)

    d.add(2,4)
    self.assertEqual(d.get(2,4), 2)

    for i in range(10):
        d.add(2,4)

    self.assertEqual(d.get(2,4), 12)

  def test_4(self):
    d = TrackComponents()
    d.add(2,4)
    d.add(2,0)
    d.add(2,0)
    self.assertEqual(d.get(2), {0:1, 1:2})

  def test_5(self):
    d = TrackComponents()

    d.add(20,100)
    self.assertEqual(d.get(20), {0:1})
    self.assertEqual(d.get(20,100), 1)

    d.add(20,98)
    self.assertEqual(d.get(20), {0:1, 1:1})
    self.assertEqual(d.get(20,98), 1)
    with self.assertRaises(KeyError):
        d.get(20,0)

    d.add(55,98)
    d.add(55,98)
    self.assertEqual(d.get(55), {1:2})
    self.assertEqual(d.get(55,98), 2)
    with self.assertRaises(KeyError):
        d.get(55,1)


if __name__ == '__main__':
    unittest.main()
