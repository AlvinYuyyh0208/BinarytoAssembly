def parse_instruction(word):
    opcode = (word >> 26) & 0x0000003F
    rs = (word >> 21) & 0x0000001F
    rt = (word >> 16) & 0x0000001F
    rd = (word >> 11) & 0x0000001F
    shamt = (word >> 6) & 0x0000001F
    funct = word & 0x0000003F
    immediate = word & 0x0000FFFF
    jump_address = word & 0x3FFFFFF

    if immediate > 2 ** 15:
        signed_immediate = immediate - 2 ** 16
        return opcode, rs, rt, rd, shamt, funct, signed_immediate, jump_address

    return opcode, rs, rt, rd, shamt, funct, immediate, jump_address


def disassemble_instruction(opcode, rs, rt, rd, shamt, funct, immediate, jump_address):
    # R-type instruction
    if opcode == 0:
        if funct == 32:  # ADD
            return f"ADD $r{rd}, $r{rs}, $r{rt}"
        elif funct == 34:  # SUB
            return f"SUB $r{rd}, $r{rs}, $r{rt}"
        elif funct == 0:
            if rt == 0 and rd == 0 and shamt == 0:  # NOP
                return f"NOP"
            else:
                return f"SLL $r{rd}, $r{rt}, #{shamt}"  # SLL
        elif funct == 2:  # SRL
            return f"SRL $r{rd}, $r{rt}, #{shamt}"
        elif funct == 3:  # SRA
            return f"SRA $r{rd}, $r{rt}, #{shamt}"
        elif funct == 36:  # AND
            return f"AND $r{rd}, $r{rs}, $r{rt}"
        elif funct == 37:  # OR
            return f"OR $r{rd}, $r{rs}, $r{rt}"
        elif funct == 38:  # XOR
            return f"XOR $r{rd}, $r{rs}, $r{rt}"
        elif funct == 39:  # NOR
            return f"NOR $r{rd}, $r{rs}, $r{rt}"
        elif funct == 42:  # SLT
            return f"SLT $r{rd}, $r{rs}, $r{rt}"
        elif funct == 33:  # ADDU
            return f"ADDU $r{rd}, $r{rs}, $r{rt}"
        elif funct == 35:  # SUBU
            return f"SUBU $r{rd}, $r{rs}, $r{rt}"

    # I-type instruction

    elif opcode == 8:  # ADDI
        return f"ADDI $r{rt}, $r{rs}, #{immediate}"
    elif opcode == 9:  # ADDIU
        return f"ADDIU $r{rt}, $r{rs}, #{immediate}"
    elif opcode == 12:  # ANDI
        return f"ANDI $r{rt}, $r{rs}, #{immediate & 0xFFFF}"
    elif opcode == 13:  # ORI
        return f"ORI $r{rt}, $r{rs}, #{immediate & 0xFFFF}"
    elif opcode == 14:  # XORI
        return f"XORI $r{rt}, $r{rs}, #{immediate & 0xFFFF}"
    elif opcode == 15:  # LUI
        return f"LUI $r{rt}, #{immediate}"
    elif opcode == 35:  # LW
        return f"LW $r{rt}, #{immediate}($r{rs})"
    elif opcode == 43:  # SW
        return f"SW $r{rt}, #{immediate}($r{rs})"
    elif opcode == 4:  # BEQ
        return f"BEQ $r{rs}, $r{rt}, #{immediate * 4}"
    elif opcode == 5:  # BNE
        return f"BNE $r{rs}, $r{rt}, #{immediate}"
    elif opcode == 10:  # SLTI
        return f"SLTI $r{rt}, $r{rs}, #{immediate}"

    # J-type insturction
    elif opcode == 2:
        return f"J #{jump_address * 4}"
    elif opcode == 3:
        return f"JAL #{jump_address}"

    return "break"


def format_instruction_groups(binary_str):
    groups = [binary_str[:6], binary_str[6:11], binary_str[11:16], binary_str[16:21], binary_str[21:26],
              binary_str[26:]]
    return ' '.join(groups)


def disassemble(input_filename, output_filename):
    current_address = 496
    with open(input_filename, 'r') as infile, open(output_filename, 'w') as outfile:
        for line in infile:
            word = int(line.strip(), 2)
            opcode, rs, rt, rd, shamt, funct, immediate, jump_address = parse_instruction(word)
            instruction = disassemble_instruction(opcode, rs, rt, rd, shamt, funct, immediate, jump_address)

            binary_str = format_instruction_groups(line.strip())
            outfile.write(f"{binary_str}\t{current_address}\t{instruction}\n")
            current_address += 4
            if current_address == 700:
                return "break"


disassemble('input2.txt', 'output2.txt')
