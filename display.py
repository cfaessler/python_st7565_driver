class Display(object):
    def __init__(self, driver):
        self.driver = driver
        self.buffer = None
        self.clear_buffer()

        self.rows = 64
        self.columns = 128

    def clear_buffer(self):
        self.buffer = [[0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                        0x00]] * 64

    def get_pixel(self, x, y):
        x_byte = int(x / 8)
        idx = 0x80 >> x % 8
        return 1 if self.buffer[y][x_byte] & idx else 0

    def set_pixel(self, x, y, value):
        x_byte = int(x / 8)
        idx = 0x80 >> x % 8
        if value == 1:
            self.buffer[y][x_byte] |= idx
        if value == 0:
            self.buffer[y][x_byte] &= (~idx)
