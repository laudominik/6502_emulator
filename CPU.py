from Instruction import Instruction
import enum


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

            0x10: Instruction(self.REL, 2, self.BPL),
            0x11: Instruction(self.IZY, 5, self.ORA),



            0x15: Instruction(self.ZPX, 4, self.ORA),
            0x16: Instruction(self.ZPX, 6, self.ASL),

            0x18: Instruction(self.IMP, 2, self.CLC),  # OK
            0x19: Instruction(self.ABY, 4, self.ORA),



            0x1d: Instruction(self.ABX, 4, self.ORA),
            0x1e: Instruction(self.ABX, 7, self.ASL),

            0x20: Instruction(self.ABS, 6, self.JSR),  # OK



            0x24: Instruction(self.ZPG, 3, self.BIT),  # OK
            0x25: Instruction(self.ZPG, 3, self.AND),  # OK
            0x26: Instruction(self.ZPG, 5, self.ROL),  # OK

            0x28: Instruction(self.IMP, 4, self.PLP),  # OK
            0x29: Instruction(self.IMM, 2, self.AND),  # OK
            0x2a: Instruction(self.IMP, 2, self.ROL),  # OK

            0x2c: Instruction(self.ABS, 4, self.BIT),
            0x2d: Instruction(self.ABS, 4, self.AND),
            0x2e: Instruction(self.ABS, 6, self.ROL),

            0x30: Instruction(self.REL, 2, self.BMI),


            0x69: Instruction(self.IMM, 2, self.ADC),  # OK

            0x85: Instruction(self.ZPG, 3, self.STA),  # OK
            0x8d: Instruction(self.ABS, 4, self.STA),  # OK

            0xa0: Instruction(self.IMM, 2, self.LDY),  # OK

            0xa2: Instruction(self.IMM, 2, self.LDX),  # OK
            0xa6: Instruction(self.ZPG, 3, self.LDX),  # OK
            0xa9: Instruction(self.IMM, 2, self.LDA),  # OK

            0xc0: Instruction(self.IMM, 2, self.CPY),




            0xc8: Instruction(self.IMP, 2, self.INY),  # OK
            0xc9: Instruction(self.IMM, 2, self.CMP),

            0xe8: Instruction(self.IMP, 2, self.INX),  # OK

            0xae: Instruction(self.ABS, 4, self.LDX),  # OK

            0xe0: Instruction(self.IMM, 2, self.CPX),

            0xea: Instruction(self.IMM, 2, self.NOP),  # OK

        }

        for key in self.lookup:
            self.lookup[key].opcode = key
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

            out = f"{hex(self.PC)} {hex(self.instruction.opcode)}"

            self.instruction.addrmode()

            if self.instruction.addrmode != self.IMP:
                out += f" {hex(self.addr)}"

            if self.debug: print(out)

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
        self.addr = self.arg
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

    def ABY(self):
        pass

    def ABX(self):
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

        self.SP -= 1

    def BPL(self):
        pass

    # clear the carry bit in status register

    def CLC(self):

        self.status_set(CPU.STATUS_BITS['C'], False)

    # store a in address specified

    def STA(self):
        self.write(self.addr, self.A)

    def JSR(self):

        self.write(0x0100 + self.SP, self.PC & 0xFF)
        self.SP -= 1

        self.write(0x0100 + self.SP, self.PC >> 8)
        self.SP -= 1

        self.PC = self.addr


    def AND(self):

        self.A &= self.arg
        self.status_set(CPU.STATUS_BITS['N'], self.A & 0x80)
        self.status_set(CPU.STATUS_BITS['Z'], self.A == 0)

    # test bits in memory

    def BIT(self):

        self.status_set(CPU.STATUS_BITS['N'],
                        self.arg >> 7)
        self.status_set(CPU.STATUS_BITS['V'], self.arg & (1 << 6))

        self.status_set(CPU.STATUS_BITS['Z'], (self.arg & self.A) == 0)

    def ROL(self):

        if self.instruction.addrmode == self.IMP:
            temp = self.A
        else:
            temp = self.arg

        temp <<= 1
        C = self.status_get(CPU.STATUS_BITS['C'])

        self.status_set(CPU.STATUS_BITS['C'], temp > 255)

        temp &= 0xFF
        temp |= C
        self.status_set(CPU.STATUS_BITS['N'], temp & 0x80)
        self.status_set(CPU.STATUS_BITS['Z'], temp == 0)

        if self.instruction.addrmode == self.IMP:
            self.A = temp
        else:
            self.write(self.addr, temp)

    # processor status is pulled from stack
    def PLP(self):

        self.SP += 1

        flagB = self.status_get(CPU.STATUS_BITS['B'])
        flagU = self.status_get(CPU.STATUS_BITS['U'])

        self.S = self.read(0x0100 + self.SP)

        self.status_set(CPU.STATUS_BITS['B'], flagB)
        self.status_set(CPU.STATUS_BITS['U'], flagU)

    def INX(self):

        self.X += 1
        self.X &= 0xFF

        self.status_set(CPU.STATUS_BITS['N'], self.X & 0x80)
        self.status_set(CPU.STATUS_BITS['Z'], self.X == 0)

    def INY(self):

        self.Y += 1
        self.Y &= 0xFF

        self.status_set(CPU.STATUS_BITS['N'], self.Y & 0x80)
        self.status_set(CPU.STATUS_BITS['Z'], self.Y == 0)

    def CMP(self):

        reg = self.A

        self.status_set(CPU.STATUS_BITS['Z'], reg == self.arg)
        self.status_set(CPU.STATUS_BITS['C'], reg >= self.arg)
        self.status_set(CPU.STATUS_BITS['N'], reg < self.arg)


    def CPX(self):

        reg = self.X

        self.status_set(CPU.STATUS_BITS['Z'], reg == self.arg)
        self.status_set(CPU.STATUS_BITS['C'], reg >= self.arg)
        self.status_set(CPU.STATUS_BITS['N'], reg < self.arg)

    def CPY(self):

        reg = self.Y

        self.status_set(CPU.STATUS_BITS['Z'], reg == self.arg)
        self.status_set(CPU.STATUS_BITS['C'], reg >= self.arg)
        self.status_set(CPU.STATUS_BITS['N'], reg < self.arg)


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

    def LDY(self):

        self.Y = self.arg

    # add with carry to the accumulator

    def ADC(self):

        prev = self.A
        self.A += self.arg
        carry = self.status_get(CPU.STATUS_BITS['C'])
        self.A += carry

        self.status_set(CPU.STATUS_BITS['C'], self.A > 0xFF)
        self.status_set(CPU.STATUS_BITS['Z'], self.A == 256)

        self.status_set(CPU.STATUS_BITS['N'], self.A & 0x80)
        self.status_set(CPU.STATUS_BITS['V'],
                        ~((prev ^ self.arg) &
                        (prev ^ self.A)) &
                        0x0080)

        self.A %= 256

    # ----------------------------
    def status_get(self, bit):
        return 1 if (self.S & bit) > 0 else 0
