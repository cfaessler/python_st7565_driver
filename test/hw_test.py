from devices import SPIDevice
from driver import ST7565

device = SPIDevice(100000, 25)
driver = ST7565(device, power_control=0x03, voltage_regulator=0x07)

driver.write_data(0x42)
driver.write_data(0x42)
driver.write_data(0x42)
driver.write_data(0x42)
