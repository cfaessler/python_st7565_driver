from __future__ import print_function
import unittest

from devices import StreamPrinterDevice
from driver import ST7565


class ListStream(object):
    def __init__(self):
        self.buffer = []

    def write(self, data):
        self.buffer.append(data)


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

        #TODO: Is there a better way to do this? maybe within the print function (no line-end)?
        for byte in self.stream.buffer:
            if byte == '':
                self.stream.buffer.remove(byte)

        #print(self.stream.buffer)
        self.assertEqual(self.stream.buffer, init_sequence, "Init sequence not as it should be!")

