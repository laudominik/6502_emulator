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
    address = self.read(self.PC + 1) + self.Y
    address &= 0xFF

    self.addr = address
    self.arg = self.read(address)

    self.PC += 2


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
    lo = self.read(self.PC + 1)
    hi = self.read(self.PC + 2)
    address = (hi * 256) | lo

    self.addr = address + self.Y
    self.arg = self.read(self.addr)
    self.PC += 3


def ABX(self):
    lo = self.read(self.PC + 1)
    hi = self.read(self.PC + 2)
    address = (hi * 256) | lo

    self.addr = address + self.X
    self.arg = self.read(self.addr)
    self.PC += 3


def REL(self):
    self.arg = self.read(self.PC + 1)
    self.PC += 2

    if self.arg & 0x80:

        self.addr = self.PC - ((~(self.arg - 1)) & 0xFF)
    else:
        self.addr = self.PC + self.arg