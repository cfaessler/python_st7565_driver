from __future__ import print_function


class StreamPrinterDevice(object):
    def __init__(self, stream):
        self.a0 = 0
        self.stream = stream

    def write(self, byte):
        print("{0:b} {1:08b}".format(self.a0, byte), file=self.stream, end='')

    def set_a0(self, value):
        self.a0 = value
