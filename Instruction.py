class Instruction:

    def __init__(self, addrmode, cycles, callback):

        self.addrmode = addrmode
        self.cycles = cycles
        self.callback = callback


