from Instruction import Instruction
import enum


class CPU:

    def __init__(self, bus):

        self.A = 0x00
        self.X = 0x00
        self.Y = 0x00
        self.SP = 0x00
        self.PC = 0x0000
        self.S = 0x00  # status register
        self.cycles = 0
        self.bus = bus
        self.instruction: Instruction = None

        self.arg = None
        self.arg2 = None

        self.lookup = {

        #
        #   opcd              address   c  callback
            0x00: Instruction(self.IMP, 7, self.BRK),
            0x01: Instruction(self.IZX, 6, self.ORA),
            0x05: Instruction(self.ZP, 3, self.ORA),
            0x06: Instruction(self.ZP, 6, self.ASL),
            0x08: Instruction(self.IMP, 2, self.PHP),
            0x09: Instruction(self.IMM, 2, self.ORA),
            0x0d: Instruction(self.ABS, 4, self.ORA),
            0x0e: Instruction(self.ABS, 6, self.ASL),
            0x18: Instruction(self.IMP, 2, self.CLC),
            0x29: Instruction(self.IMM, 2, self.ADC),
            0x0a: Instruction(self.IMM, 2, self.ASL),
            0xa9: Instruction(self.IMM, 2, self.LDA),
            0xea: Instruction(self.IMM, 2, self.NOP)

        }


    STATUS_BITS = {
        'C': 1,
        'Z': 2,
        'I': 4,
        'D': 8,
        'B': 16,
        'U': 32,
        'V': 64,
        'N': 128
    }

    def reset(self):
        lo = self.read(0xFFFC)
        hi = self.read(0xFFFD)

        self.PC = (hi * 256) | lo
        self.A = 0x00
        self.X = 0x00
        self.Y = 0x00
        self.SP = 0x00
        self.STATUS = CPU.STATUS_BITS['U']
        self.arg = None
        self.arg2 = None

        self.instruction = Instruction(self.IMP, 9, self.NOP)
        self.cycles = 1
        self.PC -= 1


    def status_set(self, bit, val: bool):

        if val:
            self.S |= bit
        else:
            self.S &= ~bit

    def read(self, address):

        return self.bus.read(address)

    def tick(self):
        if self.cycles == 0:

            # read instruction from memory

            op = self.read(self.PC)

            self.instruction = self.lookup[op]
            self.instruction.addrmode()

            self.cycles += 1

        elif self.cycles < self.instruction.cycles:

            # emulate clock cycles

            self.cycles += 1

        else:
            # execute

            self.instruction.callback()
            self.cycles = 0

    def write(self, address, value) -> None:
        self.bus.write(address, value)

    # ------addressing-modes------

    def IMM(self):
        self.arg = self.read(self.PC + 1)
        self.PC += 2

    def IMP(self):
        self.PC += 1

    def ZP(self):
        pass

    def ZPX(self):
        pass

    def ZPY(self):
        pass

    def IZX(self):

        address = self.read(self.PC + 1) + self.X
        address &= 0xFF

        self.arg = self.read(address)

        self.PC += 2 # to check!!!

    def IZY(self):

        pass

    def ABS(self):
        pass

    def IND(self):
        pass

    def REL(self):
        pass

    # ----------------------------

    # --------instructions--------

    def NOP(self):
        self.PC += 1

    def BRK(self):
        print("break")
        self.PC += 1

    def ORA(self):
        self.A |= self.arg
        self.status_set(CPU.STATUS_BITS['Z'], self.A == 0)
        self.status_set(CPU.STATUS_BITS['N'], self.A & 0x80)

    def ASL(self):
        pass

    def PHP(self):
        pass

    def BPL(self):
        pass

    def CLC(self):

        self.status_set(CPU.STATUS_BITS['C'],False)


    def JSR(self):
        pass

    def AND(self):
        pass

    def BIT(self):
        pass

    def ROL(self):
        pass

    def PLP(self):
        pass

    def BMI(self):
        pass

    def SEC(self):
        pass

    def RTI(self):
        pass

    def EOR(self):
        pass

    def LSR(self):
        pass

    def PHA(self):
        pass

    def BVC(self):
        pass

    def CLI(self):
        pass

    def JMP(self):
        pass

    def LDA(self):

        self.A = self.arg

    def ADC(self):

        self.A += self.arg

        if(self.A > 0xFF):
            self.status_set(CPU.STATUS_BITS['C'],True)
        if(self.A  == 256):
            self.status_set(CPU.STATUS_BITS['Z'], True)
        self.status_set(CPU.STATUS_BITS['N'], self.A & 0x80)
        self.status_set(CPU.STATUS_BITS['V'],
                        ~(self.A ^ self.arg) &
                        ((self.A - self.arg) ^ self.A) &
                        0x0080)

        self.A %= 256

    # ----------------------------
