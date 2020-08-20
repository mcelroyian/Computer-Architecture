"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.reg[7] = 0xF4
        self.pc = 0
        self.fl = 0
        self.hlt = 0b00000001


    def load(self):
        """Load a program into memory."""

        address = 0

        with open(sys.argv[1]) as f:
            for command in f:
                command = command.strip()
                program = command.split()

                if len(program) == 0:
                    continue

                if program[0][0] == "#":
                    continue

                try:
                    self.ram[address] = int(program[0], 2)

                
                except ValueError:
                    print(f"Invalid number: {program[0]}")
                    sys.exit(1)
                
                address += 1


        # program = []

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB": 
            pass
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True

        while running:
            ir = self.ram[self.pc]

            operand_a = self.ram_read(self.pc+1)
            operand_b = self.ram_read(self.pc+2)

            if ir == 0b10000010:

                self.reg[operand_a] = operand_b
                self.pc += 3
            elif ir == 0b01000111:
                print(self.reg[operand_a])
                self.pc += 2
            elif ir == 0b10100010:
                self.alu("MUL", operand_a, operand_b)
                self.pc += 3
            elif ir == 0b01000101:
                self.reg[7] -=1
                value = self.reg[operand_a]
                self.ram[self.reg[7]] = value
                self.pc += 2
            elif ir == 1:
                running = False

            else:
                print(self.reg)
                print(self.ram)
                print("no matches")
                running = False
                

    def ram_read(self, mdr):
        return self.ram[mdr]

    def ram_write(self, mdr, mar):
        self.ram[mar] = mdr
