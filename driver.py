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
        assert 0 <= column < 128
        self.write_command(COLUMN_ADDRESS_HIGH | ((column & 0xF0) >> 4))
        self.write_command(COLUMN_ADDRESS_LOW | column & 0x0F)

    def set_page(self, page):
        assert 0 <= page < 8
        self.write_command(PAGE_ADDRESS | page)

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

    def write_page(self, bitmap, page):
        self.set_page(page)
        #TODO does the internal RAM address counter increment by 1 (one-bit) or by one byte?
        #TODO if per bit, then incrementing column by 8 maybe faster
        self.set_column(0)
        for val in bitmap:
            self.write_data(val)

    def write_bitmap(self, bitmap):
        # bitmap should contain 8 pages
        assert len(bitmap) == 8
        for page in range(8):
            page_start = 128 * page
            page_end = (page + 1) * 128
            self.write_page(bitmap[page_start:page_end])


