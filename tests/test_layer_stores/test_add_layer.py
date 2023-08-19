import unittest
from ed_utils.decorators import number

from layer_store import AdditiveLayerStore
from layers import black, lighten, rainbow, invert

class TestAddLayer(unittest.TestCase):

    @number("2.1")
    def test_no_layer(self):
        s = AdditiveLayerStore()
        for color in [
            (255, 255, 255),
            (0, 0, 0),
            (255, 0, 255),
        ]:
            self.assertEqual(s.get_color(color, 0, 1, 1), color)

    @number("2.2")
    def test_layers(self):
        s = AdditiveLayerStore()
        s.add(black)
        self.assertEqual(s.get_color((20, 20, 20), 40, 0, 0), (0, 0, 0))
        # This should light the black, not the background.
        s.add(lighten)
        self.assertEqual(s.get_color((100, 100, 100), 0, 20, 40), (40, 40, 40))

    @number("2.3")
    def test_erase(self):
        s = AdditiveLayerStore()
        s.add(black)
        s.add(lighten)
        s.erase(lighten)
        self.assertEqual(s.get_color((25, 25, 25), 7, 0, 0), (65, 65, 65))

    @number("2.4")
    def test_special(self):
        s = AdditiveLayerStore()
        s.add(lighten)
        s.add(rainbow)
        s.add(black)
        self.assertEqual(s.get_color((100, 100, 100), 0, 0, 0), (0, 0, 0))
        s.special()
        self.assertEqual(s.get_color((100, 100, 100), 7, 0, 0), (131, 254, 144))
        s.erase(lighten)
        s.add(lighten)
        self.assertEqual(s.get_color((100, 100, 100), 7, 0, 0), (171, 255, 184))
        s.special()
        self.assertEqual(s.get_color((100, 100, 100), 7, 0, 0), (91, 214, 104))

    @number("2.5")
    def test_example(self):
        s = AdditiveLayerStore()
        s.add(rainbow)
        self.assertEqual(s.get_color((100, 100, 100), 7, 0, 0), (91, 214, 104))
        s.add(lighten)
        s.add(lighten)
        self.assertEqual(s.get_color((100, 100, 100), 7, 0, 0), (171, 255, 184))
        s.special()
        self.assertEqual(s.get_color((100, 100, 100), 7, 0, 0), (91, 214, 104))
        s.erase(invert)
        s.erase(black)
        s.add(invert)
        self.assertEqual(s.get_color((100, 100, 100), 7, 0, 0), (255-91, 255-214, 255-104))
