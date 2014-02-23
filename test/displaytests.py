import unittest
from display import Display


class TestDisplay(unittest.TestCase):
    def setUp(self):
        self.display = Display(None)

    def test_set_pixels(self):
        self.display.clear_buffer()
        self.display.set_pixel(0, 1, 1)
        self.assertEqual(self.display.get_pixel(0, 1), 1, "pixel was not set")

        self.display.set_pixel(100, 1, 1)
        self.assertEqual(self.display.get_pixel(100, 1), 1, "pixel was not set")

        self.display.set_pixel(3, 2, 0)
        self.assertEqual(self.display.get_pixel(3, 2), 0, "pixel was not set")
