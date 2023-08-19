import unittest
from ed_utils.decorators import number

from layer_store import SequenceLayerStore
from layers import black, lighten, rainbow, invert

class TestSeqLayer(unittest.TestCase):

    @number("3.1")
    def test_no_layer(self):
        s = SequenceLayerStore()
        for color in [
            (255, 255, 255),
            (0, 0, 0),
            (255, 0, 255),
        ]:
            self.assertEqual(s.get_color(color, 0, 1, 1), color)

    @number("3.2")
    def test_layers(self):
        s = SequenceLayerStore()
        s.add(black)
        # Light comes after black.
        s.add(lighten)
        self.assertEqual(s.get_color((100, 100, 100), 0, 20, 40), (40, 40, 40))
        s.erase(lighten)
        s.add(rainbow)
        # Rainbow comes before black.
        self.assertEqual(s.get_color((20, 20, 20), 7, 0, 0), (0, 0, 0))

    @number("3.3")
    def test_erase(self):
        s = SequenceLayerStore()
        s.add(black)
        s.add(lighten)
        s.erase(lighten)
        self.assertEqual(s.get_color((25, 25, 25), 7, 0, 0), (0, 0, 0))

    @number("3.4")
    def test_special(self):
        s = SequenceLayerStore()
        s.add(invert)
        s.add(lighten)
        s.add(rainbow)
        s.add(black)
        self.assertEqual(s.get_color((100, 100, 100), 0, 0, 0), (215, 215, 215))
        s.special() # Ordering: Black, Invert, Lighten, Rainbow.
                    # Remove: Invert
        self.assertEqual(s.get_color((100, 100, 100), 7, 0, 0), (40, 40, 40))
        s.special() # Ordering: Black, Lighten, Rainbow.
                    # Remove: Lighten
        self.assertEqual(s.get_color((100, 100, 100), 7, 0, 0), (0, 0, 0))
        s.special() # Ordering: Black, Rainbow.
                    # Remove: Black
        self.assertEqual(s.get_color((100, 100, 100), 7, 0, 0), (91, 214, 104))

    @number("3.5")
    def test_example(self):
        s = SequenceLayerStore()
        s.add(rainbow)
        s.add(invert)
        self.assertEqual(s.get_color((100, 100, 100), 7, 0, 0), (255-91, 255-214, 255-104))
        s.add(black)
        self.assertEqual(s.get_color((100, 100, 100), 7, 0, 0), (255, 255, 255))
        s.special() # Ordering: Black, Invert, Rainbow.
                    # Remove: Invert
        self.assertEqual(s.get_color((100, 100, 100), 7, 0, 0), (0, 0, 0))
        s.add(black)
        self.assertEqual(s.get_color((100, 100, 100), 7, 0, 0), (0, 0, 0))
        s.erase(black)
        self.assertEqual(s.get_color((100, 100, 100), 7, 0, 0), (91, 214, 104))
