from Bus import Bus
from CPU import CPU

bus = Bus()

bus.ram[0x00] = 0xa9
bus.ram[0x01] = 0xFF
bus.ram[0x02] = 0x29
bus.ram[0x03] = 1
bus.ram[0x04] = 0x18


while 1:
    bus.cpu.cycle()

print(bus.read(0xFF))