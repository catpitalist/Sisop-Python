import commands
## Symbolic consts
label = 0
command = 1
op = 2
hashed_op = 3
commands = ["ADD", "SUB", "MULT", "DIV", "LOAD", "STORE", "BRANY", "BRPOS", "BRZERO", "BRNEG", "SYSCALL"]
branch_commands = ["BRANY", "BRPOS", "BRZERO", "BRNEG"]
## End Symbolic consts

def is_label(word):
    return word[-1] == ":"

def is_command(word):
    return word in commands

def is_hashed(word):
    return word[0] == "#"


class Token():
    def __init__(self, word):
        self.content = word
        word = word.upper()
        if is_label(word):
            self.type = label
        elif is_command(word):
            self.type = command
        elif is_hashed(word):
            self.type = hashed_op
            self.content = int(word[1:])
        else:
            self.type = op
    
    def __repr__(self):
        if self.type == label:
            token_type = "<label>"
        if self.type == command:
            token_type = "<command>"
        if self.type == op:
            token_type = "<op>"
        if self.type == hashed_op:
            token_type = "<#op>"
        return f'TOKEN:[{self.content} {token_type}]'
    
    def __str__(self):
        return self.__repr__()