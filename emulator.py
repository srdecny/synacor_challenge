
import numpy as np

def instructions_from_file(filename):
    with open(filename, "rb") as file:
        while True:
            bytes = file.read(2)
            if bytes:
                yield int.from_bytes(bytes, byteorder="little")
            else:
                break

def read_memory(address):
    if 0 <= address <= 32775:
        if address >= 32768:
            return registers[address - 32768]
        else:
            return address

    elif int >= 32776:
        raise NotImplementedError(f"Integer {address} is not a valid memory address")

def write_memory(address, value):
    if 0 <= address <= 32775:
        if address >= 32768:
            registers[address - 32768] = value
        else:
            program[address] = value
    else:
        raise NotImplementedError(f"Integer {address} is not a valid memory address")

def get_parameters(start, count):
    if count > 1:
        parameters = []
        for i in range(start+1, start+count+1):
            parameters.append(program[i])
        return parameters
    else:
        return program[start + 1]

opcodes = ["halt", "set", "push", "pop", "eq", "gt", "jmp", "jt", "jf", "add", "mult", "mod", "and", "or", "not", "rmem", "wmem", "call", "ret", "out", "in", "noop"]
program = []
registers = [0, 0, 0, 0, 0, 0, 0, 0]
stack = []
buffer = ""
ip = 0
for instruction in instructions_from_file("/home/srdecny/Documents/Synacor/challenge.bin"):
    program.append(instruction)

while True:
    instruction = program[ip]
    #print(f"Executing {ip}: {opcodes[instruction]}")

    if ip == 697:
        print("")

    if instruction == 0:
        break
    
    # set
    elif instruction == 1:
        a, b = get_parameters(ip, 2)
        registers[a - 32768] = b
        ip += 3

    # push on stack
    elif instruction == 2:
        a = get_parameters(ip, 1)
        stack.append(read_memory(a))
        ip += 2

    # pop from stack
    elif instruction == 3:
        a = get_parameters(ip, 1)
        write_memory(a, stack.pop())
        ip += 2

    # equals
    elif instruction == 4:
        a, b, c = get_parameters(ip, 3)
        if read_memory(b) == read_memory(c):
            write_memory(a, 1)
        else:
            write_memory(a, 0)
        ip += 4

    # greater than
    elif instruction == 5:
        a, b, c = get_parameters(ip, 3)
        if read_memory(b) > read_memory(c):
            write_memory(a, 1)
        else:
            write_memory(a, 0)
        ip += 4

    # jump
    elif instruction == 6:
        a = get_parameters(ip, 1)
        ip = read_memory(a)
    
    # jump nonzero
    elif instruction == 7:
        a, b = get_parameters(ip, 2)
        if read_memory(a) != 0:
            ip = read_memory(b)
        else:
            ip += 3
    
    # jump zero
    elif instruction == 8:
        a, b = get_parameters(ip, 2)
        if read_memory(a) == 0:
            ip = read_memory(b)
        else:
            ip += 3

    # add
    elif instruction == 9:
        a, b, c = get_parameters(ip, 3)
        write_memory(a, (read_memory(b) + read_memory(c)) % 32768)
        ip += 4

    # multiply
    elif instruction == 10:
        a, b, c = get_parameters(ip, 3)
        write_memory(a, (read_memory(b) * read_memory(c)) % 32768)
        ip += 4

    # modulo
    elif instruction == 11:
        a, b, c = get_parameters(ip, 3)
        write_memory(a, read_memory(b) % read_memory(c))
        ip += 4
    
    # bitwise and
    elif instruction == 12:
        a, b, c = get_parameters(ip, 3)
        write_memory(a, (read_memory(b) & read_memory(c)) & 32767)
        ip += 4

    # bitwise or
    elif instruction == 13:
        a, b, c = get_parameters(ip, 3)
        write_memory(a, (read_memory(b) | read_memory(c)) & 32767)
        ip += 4

    # bitwise not
    elif instruction == 14:
        a, b = get_parameters(ip, 2)
        write_memory(a, (~np.uint16(read_memory(b)) & 32767))
        ip += 3

    # read memory
    elif instruction == 15:
        a, b = get_parameters(ip, 2)
        write_memory(a, read_memory(b))
        ip += 3

    # write memory
    elif instruction == 16:
        a, b = get_parameters(ip, 2)
        write_memory(read_memory(a), b)
        ip += 3
    
    # call
    elif instruction == 17:
        a, get_parameters(ip, 1)
        stack.append(ip + 2)
        ip = read_memory(a)

    # ret
    elif instruction == 18:
        ip = stack.pop
    
    # print
    elif instruction == 19:
        a = program[ip + 1]
        print(chr(a), end='')
        if (chr(a)) == 10:
            print()
        ip += 2

    # read
    elif instruction == 20:
        a = get_parameters(ip, 1)
        if buffer == "":
            buffer = input()
        write_memory(a, buffer[0])
        ip += 2
        buffer = buffer[1:]
        
    # noop
    elif instruction == 21:
        ip += 1

    else:
        raise NotImplementedError(f"Instruction {instruction} not implemented.")
