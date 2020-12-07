"""CPU functionality."""

import sys

# op-codes
LDI = 0b10000010  # 130
PRN = 0b01000111  # 71
HLT = 0b00000001  # 1


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.reg[7] = 0xF4
        self.PC = 0
        self.FL = 0
        self.ram = [0] * 256
        self.halted = False

    def load(self, filename):
        """Load a program into memory."""

        try:
            with open(filename) as f:
                address = 0
                for line in f:
                    line_split = line.split("#")
                    try:
                        binary_num = int(line_split[0], 2)
                        # print(binary_num)
                        self.ram[address] = binary_num
                        address += 1
                    except:
                        print("failed to make binary")
        except FileNotFoundError:
            print("File not found ...")

        """
        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010,  # LDI R0,8
            0b00000000,
            0b00001000,  # integer 8 to be stored
            0b01000111,  # PRN R0
            0b00000000,
            0b00000001,  # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1
        """

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(
            f"TRACE: %02X | %02X %02X %02X |"
            % (
                self.PC,
                # self.fl,
                # self.ie,
                self.ram_read(self.PC),
                self.ram_read(self.PC + 1),
                self.ram_read(self.PC + 2),
            ),
            end="",
        )

        for i in range(8):
            print(" %02X" % self.reg[i], end="")

        print()

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    def run(self):
        """Run the CPU."""
        while not self.halted:
            op = self.ram_read(self.PC)
            if op == LDI:
                self.reg[self.ram_read(self.PC + 1)] = self.ram_read(self.PC + 2)
                print("LDI success")
                self.PC += 3
            elif op == PRN:
                key = self.reg[self.PC + 1]
                print(f"value is {self.reg[key]}")
                self.PC += 2
            elif op == HLT:
                print("Program Halted")
                self.halted = True
                # sys.exit(0)
            else:
                print("Error: not a valid instruction")
                break
