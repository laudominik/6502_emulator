from Bus import Bus
from CPU import CPU

bus = Bus()

bus.load_file("a.out")


while 1:
    bus.cpu.tick()
