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
        self.addr = None

        # OPCODES -> INSTRUCTION
        # decode table

        self.lookup = {

            #   opcd              addrmode  c  callback
            0x00: Instruction(self.IMP, 7, self.BRK),
            0x01: Instruction(self.IZX, 6, self.ORA),



            0x05: Instruction(self.ZPG, 3, self.ORA),  # OK
            0x06: Instruction(self.ZPG, 5, self.ASL),  # OK

            0x08: Instruction(self.IMP, 3, self.PHP),  # OK (to check eventually)
            0x09: Instruction(self.IMM, 2, self.ORA),  # OK
            0x0a: Instruction(self.IMP, 2, self.ASL),  # OK


            0x0d: Instruction(self.ABS, 4, self.ORA),  # OK
            0x0e: Instruction(self.ABS, 6, self.ASL),  # OK

            0x10: Instruction(self.REL, 2, self.BPL),  # OK
            0x11: Instruction(self.IZY, 5, self.ORA),  # OK

            0x18: Instruction(self.IMP, 2, self.CLC),  # OK

            0x69: Instruction(self.IMM, 2, self.ADC),  # OK

            0x85: Instruction(self.ZPG, 3, self.STA),  # OK
            0x8d: Instruction(self.ABS, 4, self.STA),  # OK
            0xa2: Instruction(self.IMM, 2, self.LDX),  # OK
            0xa6: Instruction(self.ZPG, 3, self.LDX),  # OK
            0xa9: Instruction(self.IMM, 2, self.LDA),  # OK
            0xae: Instruction(self.ABS, 4, self.LDX),  # OK
            0xea: Instruction(self.IMM, 2, self.NOP),  # OK

        }

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
        self.SP = 0x00
        self.STATUS = CPU.STATUS_BITS['U']
        self.arg = None
        self.arg2 = None

        self.instruction = Instruction(self.IMP, 9, self.NOP)
        self.cycles = 1
        self.PC -= 1

    def status_set(self, bit, val: bool or int):

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

    def ZPG(self):

        address = self.read(self.PC + 1)
        self.addr = address
        self.arg = self.read(address)

        self.PC += 2

    def ZPX(self):

        address = self.read(self.PC + 1) + self.X
        address &= 0xFF

        self.addr = address
        self.arg = self.read(address)

        self.PC += 2

    def ZPY(self):
        pass

    def IZX(self):

        pass

    def IZY(self):

        pass

    def ABS(self):
        lo = self.read(self.PC + 1)
        hi = self.read(self.PC + 2)
        address = (hi * 256) | lo

        self.addr = address
        self.arg = self.read(address)
        self.PC += 3

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

    # bitwise or register A and operand

    def ORA(self):
        self.A |= self.arg
        self.status_set(CPU.STATUS_BITS['Z'], self.A == 0)
        self.status_set(CPU.STATUS_BITS['N'], self.A & 0x80)

    # arithmetic shift left

    def ASL(self):

        temp = self.A if self.instruction.addrmode == self.IMP else self.arg
        temp *= 2

        self.status_set(CPU.STATUS_BITS['C'],
                        True if temp > 255 else False)

        self.status_set(CPU.STATUS_BITS['Z'], temp % 256 == 0)
        self.status_set(CPU.STATUS_BITS['N'], temp & 0x80)

        if self.instruction.addrmode == self.IMP:
            self.A = temp & 0xFF
        else:
            self.write(self.addr, temp & 0xFF)

    # push status register to stack,
    # status register has B and U as 1
    # stack is hardcoded as addresses
    # in [$0100, $01FF]

    def PHP(self):

        self.write(0x0100 + self.SP,
                   self.S |
                   CPU.STATUS_BITS['B'] |
                   CPU.STATUS_BITS['U'])

        self.SP += 1

    def BPL(self):
        pass

    # clear the carry bit in status register

    def CLC(self):

        self.status_set(CPU.STATUS_BITS['C'], False)

    # store a in address specified

    def STA(self):
        self.write(self.addr, self.A)

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

    # load register a with the operand

    def LDA(self):

        self.A = self.arg

    # load register x with the operand

    def LDX(self):

        self.X = self.arg

    # add with carry to the accumulator

    def ADC(self):

        self.A += self.arg

        if (self.A > 0xFF):
            self.status_set(CPU.STATUS_BITS['C'], True)
        if (self.A == 256):
            self.status_set(CPU.STATUS_BITS['Z'], True)
        self.status_set(CPU.STATUS_BITS['N'], self.A & 0x80)
        self.status_set(CPU.STATUS_BITS['V'],
                        ~(self.A ^ self.arg) &
                        ((self.A - self.arg) ^ self.A) &
                        0x0080)

        self.A %= 256

    # ----------------------------
