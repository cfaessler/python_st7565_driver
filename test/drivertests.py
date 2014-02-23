from __future__ import print_function
import unittest

from devices import StreamPrinterDevice
from driver import ST7565


class ListStream(object):
    def __init__(self):
        self.buffer = []

    def write(self, data):
        self.buffer.append(data)

    def get_buffer(self):
        #TODO: Is there a better way to do this? maybe within the print function (no line-end)?
        for byte in self.buffer:
            if byte == '':
                self.buffer.remove(byte)

        return self.buffer


class DriverTest(unittest.TestCase):
    def setUp(self):
        self.stream = ListStream()
        self.device = StreamPrinterDevice(self.stream)
        self.driver = ST7565(self.device, power_control=0x03, voltage_regulator=0x07)

    def test_init(self):
        #Format '[A0 Pin] [Data Byte]'
        init_sequence = [
            '0 01000000',  # Display start line 0
            '0 10100001',  # ADC reverse
            '0 11000000',  # Normal COM0~COM63
            '0 10100110',  # Display normal
            '0 10100010',  # Set bias 1/9
            '0 00101011',  # Booster off, Regulator, Follower on
            '0 00100111',  # Contrast
            '0 10000001',  # Contrast
            '0 00010110',  # Contrast
            '0 10101100',  # No Indicator
            '0 00000000',  # No Indicator
            '0 10101111',  # Display on
        ]

        self.driver.init()
        print("Data in stream was:")

        self.assertEqual(self.stream.get_buffer(), init_sequence, "Init sequence not as it should be!")

    def test_write_data(self):
        self.stream.buffer = []
        self.driver.set_page(2)
        self.driver.set_column(12)
        self.driver.write_data(0x42)

        test_sequence = [
            '0 10110010',
            '0 00010000',
            '0 00001100',
            '1 01000010'
        ]

        self.assertEqual(self.stream.get_buffer(), test_sequence,
                         "writing byte value 0x42 to page 2 column 12 was not successful")

    def test_write_page(self):
        self.stream.buffer = []
        page_pattern = [0x42] * 128
        self.driver.write_page(page_pattern, 2)

        string_pattern = ['1 01000010'] * 128
        test_sequence = [
            '0 10110010',
            '0 00010000',
            '0 00000000'
        ]
        test_sequence.extend(string_pattern)
        buf = self.stream.get_buffer()
        self.assertListEqual(buf, test_sequence, "shit happened")