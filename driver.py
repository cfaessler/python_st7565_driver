DISPLAY_ON = 0b10101111
DISPLAY_OFF = 0b10101110

SET_START_LINE = 0b01000000
PAGE_ADDRESS = 0b10110000

COLUMN_ADDRESS_HIGH = 0b00010000
COLUMN_ADDRESS_LOW = 0b00000000

ADC_NORMAL = 0b10100000
ADC_REVERSE = 0b10100001

COMMON_OUTPUT_MODE = 0b11000000

DISPLAY_NORMAL = 0b10100110
DISPLAY_REVERSE = 0b10100111

BIAS_1_9 = 0b10100010

POWER_CONTROL = 0b00101000

VOLTAGE_REGULATOR = 0b00100000

CONTRAST_MODE = 0b10000001
CONTRAST_SET = 0b00000000

INDICATOR_ON = 0b10101101
INDICATOR_OFF = 0b10101100
INDICATOR_FLASHING_ON = 0b00000001
INDICATOR_FLASHING_OFF = 0b00000000


class ST7565(object):
    def __init__(self, low_level_device, power_control, voltage_regulator):
        self.device = low_level_device
        self.power_control = power_control
        self.voltage_regulator = voltage_regulator

    def init(self):
        self.write_command(SET_START_LINE | 0x00)

        #for 6:00 viewing
        self.write_command(ADC_REVERSE)

        self.write_command(COMMON_OUTPUT_MODE | 0x00)

        self.write_command(DISPLAY_NORMAL)
        self.write_command(BIAS_1_9)

        #TODO: select power mode
        self.write_command(POWER_CONTROL | self.power_control)

        #TODO: select voltage regulator
        self.write_command(VOLTAGE_REGULATOR | self.voltage_regulator)

        self.write_command(CONTRAST_MODE)
        self.write_command(CONTRAST_SET | 0b00010110)

        self.write_command(INDICATOR_OFF)
        self.write_command(INDICATOR_FLASHING_OFF)

        self.write_command(DISPLAY_ON)

    def set_column(self, column):
        self.write_command(COLUMN_ADDRESS_HIGH | ((column & 0xF0) >> 4))
        self.write_command(COLUMN_ADDRESS_LOW | column & 0x0F)

    def set_line(self, line):
        self.write_command(PAGE_ADDRESS | line)

    def set_a0(self, value):
        self.device.set_a0(value)

    def write_data(self, data):
        self.set_a0(True)
        self._send_byte(data)

    def write_command(self, data):
        self.set_a0(False)
        self._send_byte(data)

    def _send_byte(self, byte):
        self.device.write(byte)


