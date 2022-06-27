from Bus import Bus
from CPU import CPU

bus = Bus()

bus.ram[0xFFFC] = 0x00
bus.ram[0xFFFD] = 0x80
bus.cpu.reset()


bus.ram[0x0000] = 17


#LDA 255
bus.ram[0x8000] = 0xa9
bus.ram[0x8001] = 0xFF

#ADC 1
bus.ram[0x8002] = 0x29
bus.ram[0x8003] = 1

#CLC
bus.ram[0x8004] = 0x18

#ORA $05 X

bus.ram[0x8005] = 0x01
bus.ram[0x8006] = 0x00









while 1:
    bus.cpu.tick()
