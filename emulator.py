
def instructions_from_file(filename):
    with open(filename, "rb") as file:
        while True:
            bytes = file.read(2)
            if bytes:
                yield int.from_bytes(bytes, byteorder="little")
            else:
                break
def parse_int(instructionPointer):
    int = program[instructionPointer]
    if 0 <= int <= 32767:
        return int
    elif int >= 32776:
        raise NotImplementedError(f"Integer {instructionPointer} is not a valid memory address")
    else:
         return registers[int - 32768]

program = []
registers = [0, 0, 0, 0, 0, 0, 0, 0]
stack = []
buffer = ""
instructionPointer = 0
for instruction in instructions_from_file("/home/srdecny/Documents/Synacor/challenge.bin"):
    program.append(instruction)

while True:
    instruction = program[instructionPointer]
    # print(f"Executing {instructionPointer}: {instruction}")

    if instruction == 0:
        break
    
    # set
    elif instruction == 1:
        a = parse_int(instructionPointer + 1)
        a = parse_int(instructionPointer + 2)
        instructionPointer += 3

    # push on stack
    elif instruction == 2:
        stack.append(parse_int(instructionPointer + 1))
        instructionPointer += 2

    # pop from stack
    elif instruction == 3:
        parse_int(instructionPointer + 1)
        instructionPointer += 2
    # equals
    elif instruction == 4:
        a = parse_int(instructionPointer + 1)
        a = 1 if parse_int(instructionPointer + 2) == parse_int(instructionPointer + 3) else 0
        instructionPointer += 4

    # greater than
    elif instruction == 5:
        a = parse_int(instructionPointer + 1)
        a = 1 if parse_int(instructionPointer + 2) > parse_int(instructionPointer + 3) else 0
        instructionPointer += 4

    # jump
    elif instruction == 6:
        instructionPointer = parse_int(instructionPointer + 1)
    
    # jump nonzero
    elif instruction == 7:
        if parse_int(instructionPointer + 1) != 0:
            instructionPointer = parse_int(instructionPointer + 2)
        else:
            instructionPointer +=3
    
    # jump zero
    elif instruction == 8:
        if parse_int(instructionPointer + 1) != 0:
            instructionPointer = parse_int(instructionPointer + 2)
        else:
            instructionPointer += 3

    # add
    elif instruction == 9:
        a = parse_int(instructionPointer + 1)
        a = (parse_int(instructionPointer + 2) + parse_int(instructionPointer + 3) ) % 32768
        instructionPointer += 4

    # multiply
    elif instruction == 10:
        a = parse_int(instructionPointer + 1)
        a = (parse_int(instructionPointer + 2) * parse_int(instructionPointer + 3) ) % 32768
        instructionPointer += 4

    # modulo
    elif instruction == 11:
        a = parse_int(instructionPointer + 1)
        a = parse_int(instructionPointer + 2) % parse_int(instructionPointer + 3)
        instructionPointer += 4
    
    # bitwise and
    elif instruction == 12:
        a = parse_int(instructionPointer + 1)
        a = parse_int(instructionPointer + 2) & parse_int(instructionPointer + 3)
        instructionPointer += 4

    # bitwise or
    elif instruction == 13:
        a = parse_int(instructionPointer + 1)
        a = parse_int(instructionPointer + 2) | parse_int(instructionPointer + 3)
        instructionPointer += 4

    # bitwise not
    elif instruction == 14:
        a = parse_int(instructionPointer + 1)
        a = ~parse_int(instructionPointer + 2)
        instructionPointer += 3

    # read memory
    elif instruction == 15:
        a = parse_int(instructionPointer + 1)
        a = parse_int(instructionPointer + 2)
        instructionPointer += 3

    # write memory
    elif instruction == 16:
        b = parse_int(instructionPointer + 2)
        program[parse_int(instructionPointer + 1)] = b
        instructionPointer += 3
    
    # call
    elif instruction == 17:
        stack.insert(instructionPointer + 2)
        instructionPointer = parse_int(instructionPointer + 1)

    # ret
    elif instruction == 18:
        instructionPointer = parse_int(stack.pop)
    
    # print
    elif instruction == 19:
        print(chr(program[instructionPointer + 1]))
        instructionPointer += 2

    # read
    elif instruction == 20:
        if buffer == "":
            buffer = input()
        a = parse_int(instructionPointer + 1)
        a = buffer[0]
        instructionPointer += 2
        buffer = buffer[1:]
        
    # noop
    elif instruction == 21:
        instructionPointer += 1
    else:
        raise NotImplementedError(f"Instruction {instruction} not implemented.")
