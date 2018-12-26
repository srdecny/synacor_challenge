
def instructions_from_file(filename):
    with open(filename, "rb") as file:
        while True:
            bytes = file.read(2)
            if bytes:
                yield int.from_bytes(bytes, byteorder="little")
            else:
                break


program = []
instructionPointer = 0
for instruction in instructions_from_file("/home/srdecny/Documents/Synacor/challenge.bin"):
    program.append(instruction)

while True:
    instruction = program[instructionPointer]

    if instruction == 0:
        break

    # print
    elif instruction == 19:
        print(chr(program[instructionPointer + 1]))
        instructionPointer += 2

    # noop
    elif instruction == 21:
        instructionPointer += 1
