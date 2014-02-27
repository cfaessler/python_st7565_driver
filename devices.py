from __future__ import print_function


class StreamPrinterDevice(object):
    def __init__(self, stream):
        self.a0 = 0
        self.stream = stream

    def write(self, byte):
        print("{0:b} {1:08b}".format(self.a0, byte), file=self.stream, end='')

    def set_a0(self, value):
        self.a0 = value


class SPIDevice(object):
    def __init__(self, speed, a0_port):
        import RPi.GPIO as GPIO
        import spi

        self.a0_port = a0_port
        self.spi_device = spi.openSPI(speed=speed)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.a0_port, GPIO.OUT)

    def write(self, byte):
        self.spi_device.transfer(byte)

    def set_a0(self, value):
        if value == True:
            GPIO.output(self.a0_port, GPIO.HIGH)
        else:
            GPIO.output(self.a0_port, GPIO.LOW)



