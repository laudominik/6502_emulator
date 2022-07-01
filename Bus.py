from CPU import CPU


# data bus
# RAM [0x0, 0x7FFF]
# ROM [0x8000 + 0xFFFF]


class Bus:

    def __init__(self, debug = False):
        self.ram = [0 for x in range(0,0xFFFF + 1)]
        self.cpu = CPU(self, debug)
        self.cpu.reset()

    def read(self, address):

        return self.ram[address]

    def write(self, address, value) -> None:

        self.ram[address] = value


    def load_file(self, filename):

        with open(filename, "rb") as f:
            byte = f.read(0x8000)

        for i in range(len(byte)):
            self.ram[i + 0x8000] = byte[i]

        self.cpu.reset()

    def dump(self):

        to_dump = dict()
        tmp = self.cpu.__dict__

        to_dump.update({x: tmp[x] for x in self.cpu.__dict__
                        if x != 'bus' and
                        x != 'instruction' and
                        x != 'lookup' and
                        x != 'STATUS'
                        })
        to_dump["ram"] = self.ram

        return to_dump







