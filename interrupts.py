from Instruction import Instruction
from addr_modes import IMP
from opcodes import NOP


def interrupt(self):
    self.write(0x0100 + self.SP, self.PC & 0xFF)
    self.SP -= 1

    self.write(0x0100 + self.SP - 1, self.PC >> 8)
    self.SP -= 1

    self.status_set(self.STATUS_BITS['B'], 0)
    self.status_set(self.STATUS_BITS['U'], 1)
    self.status_set(self.STATUS_BITS['I'], 1)

    self.write(0x0100 + self.SP - 2, self.S)

    self.SP -= 3


def NMI(self):

    interrupt(self)

    lo = self.read(0xFFFA)
    hi = self.read(0xFFFB)

    self.PC = (hi * 256) | lo


    self.instruction = Instruction(IMP, 9, NOP)
    self.cycles = 1
    self.PC -= 1


def IRQ(self):

    if self.status_get(self.STATUS_BITS['I']): return

    interrupt(self)

    lo = self.read(0xFFFE)
    hi = self.read(0xFFFF)

    self.PC = (hi * 256) | lo

    self.instruction = Instruction(IMP, 8, NOP)
    self.cycles = 1
    self.PC -= 1


