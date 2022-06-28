from Bus import Bus

bus = Bus()

bus.load_file("a.out")


while 1:
    bus.cpu.tick()
