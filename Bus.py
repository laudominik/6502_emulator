from CPU import CPU
from ctypes import c_uint16 as Word
from ctypes import c_uint8 as Byte

# data bus
# RAM [0x0, 0x7FFF]
# ROM [0x8000 + 0xFFFF]
class Bus:

    def __init__(self):
        self.ram = [0 for x in range(0,0xFFFF + 1)]
        self.cpu = CPU(self)
        self.cpu.setup()

    def read(self, address):

        return self.ram[address]

    def write(self, address, value) -> None:

        self.ram[address.value] = value







