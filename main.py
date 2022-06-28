from Bus import Bus

bus = Bus(debug=True)

bus.load_file("a.out")

while 1:
    bus.cpu.tick()
