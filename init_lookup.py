from Instruction import Instruction


def init_lookup(self):
    # decode opcodes

    self.lookup = {
       #opcd              addrmode  c  callback
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

        0x4c: Instruction(self.ABS, 3, self.JMP),

        0x69: Instruction(self.IMM, 2, self.ADC),  # OK
        0x6a: Instruction(self.IMP, 2, self.ROR),

        0x85: Instruction(self.ZPG, 3, self.STA),  # OK
        0x8d: Instruction(self.ABS, 4, self.STA),  # OK

        0x90: Instruction(self.REL, 2, self.BCC),

        0xa0: Instruction(self.IMM, 2, self.LDY),  # OK

        0xa2: Instruction(self.IMM, 2, self.LDX),  # OK
        0xa6: Instruction(self.ZPG, 3, self.LDX),  # OK
        0xa9: Instruction(self.IMM, 2, self.LDA),  # OK

        0xc0: Instruction(self.IMM, 2, self.CPY),  # OK

        0xc8: Instruction(self.IMP, 2, self.INY),  # OK
        0xc9: Instruction(self.IMM, 2, self.CMP),  # OK

        0xe8: Instruction(self.IMP, 2, self.INX),  # OK

        0xae: Instruction(self.ABS, 4, self.LDX),  # OK

        0xe0: Instruction(self.IMM, 2, self.CPX),  # OK

        0xea: Instruction(self.IMM, 2, self.NOP),  # OK

    }

    for key in self.lookup:
        self.lookup[key].opcode = key

