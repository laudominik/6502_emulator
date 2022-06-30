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
    self.arg = self.read(self.PC + 1)
    self.PC += 2

    if self.arg & 0x80:

        self.addr = self.PC - ((~(self.arg - 1)) & 0xFF)
    else:
        self.addr = self.PC + self.arg