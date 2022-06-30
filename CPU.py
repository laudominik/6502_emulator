from Instruction import Instruction

from init_lookup import init_lookup
from opcodes import NOP
from addr_modes import IMP, REL


class CPU:

    def __init__(self, bus, debug = False):

        self.A = 0x00
        self.X = 0x00
        self.Y = 0x00
        self.SP = 0xFF
        self.PC = 0x0000
        self.S = 0x00  # status register
        self.cycles = 0
        self.bus = bus
        self.instruction: Instruction = None

        self.debug = debug

        self.arg = None

        self.addr = None
        self.lookup = []

        init_lookup(self)


    # helper bits for the S register

    STATUS_BITS = {
        'C': 1,  # CARRY
        'Z': 2,  # ZERO
        'I': 4,  # DISABLE INTERRUPTS
        'D': 8,  # DECIMAL
        'B': 16,  # BREAK
        'U': 32,  # UNUSED
        'V': 64,  # OVERFLOW
        'N': 128  # NEGATIVE
    }

    def reset(self):
        lo = self.read(0xFFFC)
        hi = self.read(0xFFFD)

        self.PC = (hi * 256) | lo
        self.A = 0x00
        self.X = 0x00
        self.Y = 0x00
        self.SP = 0xFF
        self.STATUS = CPU.STATUS_BITS['U']
        self.arg = None


        self.instruction = Instruction(IMP, 9, NOP)
        self.cycles = 1
        self.PC -= 1

    def status_set(self, bit, val: bool or int):

        if val:
            self.S |= bit
        else:
            self.S &= ~bit

    def status_get(self, bit):
        return 1 if (self.S & bit) > 0 else 0

    def read(self, address):

        return self.bus.read(address)

    def write(self, address, value) -> None:
        self.bus.write(address, value)

    def tick(self):

        if self.cycles == 0:

            # read instruction from memory

            op = self.read(self.PC)

            self.instruction = self.lookup[op]

            out = f"{hex(self.PC)} {self.instruction.disassemble()}"

            self.instruction.addrmode(self)

            if self.instruction.addrmode != IMP:
                if self.instruction.addrmode == REL:
                    out += f" {hex(self.arg)}"
                else:
                    out += f" {hex(self.addr)}"

            if self.debug: print(out)

            self.cycles += 1

        elif self.cycles < self.instruction.cycles:

            # emulate clock cycles

            self.cycles += 1

        else:
            # execute

            self.instruction.callback(self)
            self.cycles = 0



