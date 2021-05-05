import syscall
def ADD(op, data, acc, pc):
    if not isinstance(op, int):
        op = data[op]
    return acc + op, pc+1

def SUB(op, data, acc, pc):
    if not isinstance(op, int):
        op = data[op]
    return acc - op, pc+1

def MULT(op, data, acc, pc):
    if not isinstance(op, int):
        op = data[op]
    return acc * op, pc+1

def DIV(op, data, acc, pc):
    if not isinstance(op, int):
        op = data[op]
    return acc // op, pc+1

def LOAD(op, data, acc, pc):
    if not isinstance(op, int):
        op = data[op]
    return op, pc+1

def STORE(op, data, acc, pc):
    data[op] = acc
    return acc, pc+1

def BRANY(op, data, acc, pc):
    return acc, op

def BRPOS(op, data, acc, pc):
    if acc>0:
        return acc, op
    return acc, pc+1

def BRZERO(op, data, acc, pc):
    if acc == 0:
        return acc, op
    return acc, pc+1

def BRNEG(op, data, acc, pc):
    if acc < 0:
        return acc, op
    return acc, pc+1

def SYSCALL(op, data, acc, pc):
    #print(f'SYSCALL OP:{op}')
    if op == 0:
        raise syscall.SyscallHalt
    if op == 1:
        raise syscall.SyscallWrite
    if op == 2:
        raise syscall.SyscallRead
    else:
        raise  syscall.SyscallError