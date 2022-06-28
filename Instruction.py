class Instruction:

    def __init__(self, addrmode, cycles, callback, opcode = 0x0):

        self.addrmode = addrmode
        self.cycles = cycles
        self.callback = callback
        self.opcode = opcode

