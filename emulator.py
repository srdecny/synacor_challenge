
def instructions_from_file(filename):
    with open(filename, "rb") as file:
        while True:
            bytes = file.read(2)
            if bytes:
                yield int.from_bytes(bytes, byteorder="little")
            else:
                break

def read_memory(address):
    if 0 <= address <= 32767:
        memory = program[address]
        if memory >= 32768:
            return registers[memory - 32768]
        else:
            return memory

    elif int >= 32776:
        raise NotImplementedError(f"Integer {address} is not a valid memory address")

def write_memory(address, value):
    if 0 <= address <= 32767:
        memory = program[address]
        if memory >= 32768:
            registers[memory - 32768] = value
        else:
            program[memory] = value
    else:
        raise NotImplementedError(f"Integer {address} is not a valid memory address")


program = []
registers = [0, 0, 0, 0, 0, 0, 0, 0]
stack = []
buffer = ""
ip = 0
for instruction in instructions_from_file("/home/srdecny/Documents/Synacor/challenge.bin"):
    program.append(instruction)

while True:
    instruction = program[ip]
    # print(f"Executing {ip}: {instruction}")

    if instruction == 0:
        break
    
    # set
    elif instruction == 1:
        write_memory(read_memory(ip + 1), read_memory(ip + 2))
        ip += 3

    # push on stack
    elif instruction == 2:
        stack.append(read_memory(ip + 1))
        ip += 2

    # pop from stack
    elif instruction == 3:
        write_memory(ip + 1, stack.pop)
        ip += 2

    # equals
    elif instruction == 4:
        if read_memory(ip + 2) == read_memory(ip + 3):
            write_memory(read_memory(ip + 1), 1)
        else:
            write_memory(read_memory(ip + 1), 0)
        ip += 4

    # greater than
    elif instruction == 5:
        if read_memory(ip + 2) > read_memory(ip + 3):
            write_memory(read_memory(ip + 1), 1)
        else:
            write_memory(read_memory(ip + 1), 0)
        ip += 4

    # jump
    elif instruction == 6:
        ip = read_memory(ip + 1)
    
    # jump nonzero
    elif instruction == 7:
        if read_memory(ip + 1) != 0:
            ip = read_memory(ip + 2)
        else:
            ip += 3
    
    # jump zero
    elif instruction == 8:
        if read_memory(ip + 1) == 0:
            ip = read_memory(ip + 2)
        else:
            ip += 3

    # add
    elif instruction == 9:
        write_memory(read_memory(ip + 1), (read_memory(ip + 2) + read_memory(ip + 3) ) % 32768)
        ip += 4

    # multiply
    elif instruction == 10:
        write_memory(read_memory(ip + 1), (read_memory(ip + 2) * read_memory(ip + 3) ) % 32768)
        ip += 4

    # modulo
    elif instruction == 11:
        write_memory(read_memory(ip + 1), read_memory(ip + 2) % read_memory(ip + 3))
        ip += 4
    
    # bitwise and
    elif instruction == 12:
        write_memory(read_memory(ip + 1), read_memory(ip + 2) & read_memory(ip + 3))
        ip += 4

    # bitwise or
    elif instruction == 13:
        write_memory( read_memory(ip + 1), read_memory(ip + 2) | read_memory(ip + 3))
        ip += 4

    # bitwise not
    elif instruction == 14:
        write_memory(ip + 1, ~read_memory(ip+ 2))
        ip += 3

    # read memory
    elif instruction == 15:
        write_memory(read_memory(ip + 1), read_memory(ip+2))
        ip += 3

    # write memory
    elif instruction == 16:
        write_memory(read_memory(read_memory(ip + 1)), program[ip + 2])
        ip += 3
    
    # call
    elif instruction == 17:
        stack.insert(ip + 2)
        ip = read_memory(ip + 1)

    # ret
    elif instruction == 18:
        ip = read_memory(stack.pop)
    
    # print
    elif instruction == 19:
        print(chr(program[ip + 1]), end='')
        if (chr(program[ip + 1])) == 10:
            print()
        ip += 2

    # read
    elif instruction == 20:
        if buffer == "":
            buffer = input()
        write_memory(read_memory(ip+1), buffer[0])
        ip += 2
        buffer = buffer[1:]
        
    # noop
    elif instruction == 21:
        ip += 1

    else:
        raise NotImplementedError(f"Instruction {instruction} not implemented.")
