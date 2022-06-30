from Instruction import Instruction
import opcodes as opc
import addr_modes as amd

def init_lookup(self):
    # decode opcodes

    self.lookup = {
       #opcd              addrmode  c  callback
        0x00: Instruction(amd.IMP, 7, opc.BRK),
        0x01: Instruction(amd.IZX, 6, opc.ORA),



        0x05: Instruction(amd.ZPG, 3, opc.ORA),  # OK
        0x06: Instruction(amd.ZPG, 5, opc.ASL),  # OK

        0x08: Instruction(amd.IMP, 3, opc.PHP),  # OK (to check eventually)
        0x09: Instruction(amd.IMM, 2, opc.ORA),  # OK
        0x0a: Instruction(amd.IMP, 2, opc.ASL),  # OK

        0x0d: Instruction(amd.ABS, 4, opc.ORA),  # OK
        0x0e: Instruction(amd.ABS, 6, opc.ASL),  # OK

        0x10: Instruction(amd.REL, 2, opc.BPL),
        0x11: Instruction(amd.IZY, 5, opc.ORA),

        0x15: Instruction(amd.ZPX, 4, opc.ORA),
        0x16: Instruction(amd.ZPX, 6, opc.ASL),

        0x18: Instruction(amd.IMP, 2, opc.CLC),  # OK
        0x19: Instruction(amd.ABY, 4, opc.ORA),

        0x1d: Instruction(amd.ABX, 4, opc.ORA),
        0x1e: Instruction(amd.ABX, 7, opc.ASL),

        0x20: Instruction(amd.ABS, 6, opc.JSR),  # OK

        0x24: Instruction(amd.ZPG, 3, opc.BIT),  # OK
        0x25: Instruction(amd.ZPG, 3, opc.AND),  # OK
        0x26: Instruction(amd.ZPG, 5, opc.ROL),  # OK

        0x28: Instruction(amd.IMP, 4, opc.PLP),  # OK
        0x29: Instruction(amd.IMM, 2, opc.AND),  # OK
        0x2a: Instruction(amd.IMP, 2, opc.ROL),  # OK

        0x2c: Instruction(amd.ABS, 4, opc.BIT),  # OK ?
        0x2d: Instruction(amd.ABS, 4, opc.AND),  # OK
        0x2e: Instruction(amd.ABS, 6, opc.ROL),

        0x30: Instruction(amd.REL, 2, opc.BMI),

        0x4c: Instruction(amd.ABS, 3, opc.JMP),

        0x69: Instruction(amd.IMM, 2, opc.ADC),  # OK
        0x6a: Instruction(amd.IMP, 2, opc.ROR),

        0x85: Instruction(amd.ZPG, 3, opc.STA),  # OK
        0x8d: Instruction(amd.ABS, 4, opc.STA),  # OK

        0x90: Instruction(amd.REL, 2, opc.BCC),  # OK

        0xa0: Instruction(amd.IMM, 2, opc.LDY),  # OK

        0xa2: Instruction(amd.IMM, 2, opc.LDX),  # OK
        0xa6: Instruction(amd.ZPG, 3, opc.LDX),  # OK
        0xa9: Instruction(amd.IMM, 2, opc.LDA),  # OK


        0xb0: Instruction(amd.REL, 2, opc.BCS),  # OK

        0xc0: Instruction(amd.IMM, 2, opc.CPY),  # OK

        0xc8: Instruction(amd.IMP, 2, opc.INY),  # OK
        0xc9: Instruction(amd.IMM, 2, opc.CMP),  # OK

        0xe8: Instruction(amd.IMP, 2, opc.INX),  # OK

        0xae: Instruction(amd.ABS, 4, opc.LDX),  # OK

        0xd0: Instruction(amd.REL, 2, opc.BNE),  # OK

        0xe0: Instruction(amd.IMM, 2, opc.CPX),  # OK

        0xea: Instruction(amd.IMM, 2, opc.NOP),  # OK

        0xf0: Instruction(amd.REL, 2, opc.BEQ),  # OK


    }

    for key in self.lookup:
        self.lookup[key].opcode = key

