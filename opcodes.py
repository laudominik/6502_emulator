
from addr_modes import IMP

def NOP(self):
    self.PC += 1


def BRK(self):
    print("break")
    self.PC += 1


# bitwise or register A and operand

def ORA(self):
    self.A |= self.arg
    self.status_set(self.STATUS_BITS['Z'], self.A == 0)
    self.status_set(self.STATUS_BITS['N'], self.A & 0x80)


# arithmetic shift left

def ASL(self):
    temp = self.A if self.instruction.addrmode == IMP else self.arg
    temp *= 2

    self.status_set(self.STATUS_BITS['C'],
                    True if temp > 255 else False)

    self.status_set(self.STATUS_BITS['Z'], temp % 256 == 0)
    self.status_set(self.STATUS_BITS['N'], temp & 0x80)

    if self.instruction.addrmode == IMP:
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
               self.STATUS_BITS['B'] |
               self.STATUS_BITS['U'])

    self.SP -= 1


def BPL(self):
    pass


# clear the carry bit in status register

def CLC(self):
    self.status_set(self.STATUS_BITS['C'], False)


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
    self.status_set(self.STATUS_BITS['N'], self.A & 0x80)
    self.status_set(self.STATUS_BITS['Z'], self.A == 0)


# test bits in memory

def BIT(self):
    self.status_set(self.STATUS_BITS['N'],
                    self.arg >> 7)
    self.status_set(self.STATUS_BITS['V'], self.arg & (1 << 6))

    self.status_set(self.STATUS_BITS['Z'], (self.arg & self.A) == 0)


def ROL(self):
    if self.instruction.addrmode == IMP:
        temp = self.A
    else:
        temp = self.arg

    temp <<= 1
    C = self.status_get(self.STATUS_BITS['C'])

    self.status_set(self.STATUS_BITS['C'], temp > 255)

    temp &= 0xFF
    temp |= C
    self.status_set(self.STATUS_BITS['N'], temp & 0x80)
    self.status_set(self.STATUS_BITS['Z'], temp == 0)

    if self.instruction.addrmode == IMP:
        self.A = temp
    else:
        self.write(self.addr, temp)


def ROR(self):
    if self.instruction.addrmode == IMP:
        temp = self.A
    else:
        temp = self.arg

    lowest = temp % 2

    temp >>= 1
    C = self.status_get(self.STATUS_BITS['C'])

    self.status_set(self.STATUS_BITS['C'], lowest)

    temp |= (C << 7)

    self.status_set(self.STATUS_BITS['N'], temp & 0x80)
    self.status_set(self.STATUS_BITS['Z'], temp == 0)

    if self.instruction.addrmode == IMP:
        self.A = temp
    else:
        self.write(self.addr, temp)


# processor status is pulled from stack
def PLP(self):
    self.SP += 1

    flagB = self.status_get(self.STATUS_BITS['B'])
    flagU = self.status_get(self.STATUS_BITS['U'])

    self.S = self.read(0x0100 + self.SP)

    self.status_set(self.STATUS_BITS['B'], flagB)
    self.status_set(self.STATUS_BITS['U'], flagU)


def INX(self):
    self.X += 1
    self.X &= 0xFF

    self.status_set(self.STATUS_BITS['N'], self.X & 0x80)
    self.status_set(self.STATUS_BITS['Z'], self.X == 0)


def INY(self):
    self.Y += 1
    self.Y &= 0xFF

    self.status_set(self.STATUS_BITS['N'], self.Y & 0x80)
    self.status_set(self.STATUS_BITS['Z'], self.Y == 0)


def CMP(self):
    reg = self.A

    self.status_set(self.STATUS_BITS['Z'], reg == self.arg)
    self.status_set(self.STATUS_BITS['C'], reg >= self.arg)
    self.status_set(self.STATUS_BITS['N'], reg < self.arg)


def CPX(self):
    reg = self.X

    self.status_set(self.STATUS_BITS['Z'], reg == self.arg)
    self.status_set(self.STATUS_BITS['C'], reg >= self.arg)
    self.status_set(self.STATUS_BITS['N'], reg < self.arg)


def CPY(self):
    reg = self.Y

    self.status_set(self.STATUS_BITS['Z'], reg == self.arg)
    self.status_set(self.STATUS_BITS['C'], reg >= self.arg)
    self.status_set(self.STATUS_BITS['N'], reg < self.arg)


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
    self.PC = self.addr


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
    carry = self.status_get(self.STATUS_BITS['C'])
    self.A += carry

    self.status_set(self.STATUS_BITS['C'], self.A > 0xFF)
    self.status_set(self.STATUS_BITS['Z'], self.A == 256)

    self.status_set(self.STATUS_BITS['N'], self.A & 0x80)
    self.status_set(self.STATUS_BITS['V'],
                    ~((prev ^ self.arg) &
                      (prev ^ self.A)) &
                    0x0080)

    self.A %= 256


def BCC(self):
    C = self.status_get(self.STATUS_BITS['C'])
    if C == 0:
        self.PC = self.addr



