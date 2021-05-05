from token import Token, label, op, hashed_op, command
import commands

run_funcs ={"ADD" :     commands.ADD,
            "SUB" :     commands.SUB, 
            "MULT":     commands.MULT,
            "DIV" :     commands.DIV, 
            "LOAD":     commands.LOAD,
            "STORE":    commands.STORE, 
            "BRANY":    commands.BRANY, 
            "BRPOS":    commands.BRPOS, 
            "BRZERO":   commands.BRZERO, 
            "BRNEG":    commands.BRNEG, 
            "SYSCALL":  commands.SYSCALL}

class Statement():
    def __init__(self, label, command, op):
        self.label = label
        self.command = command
        self.op = op
        if self.command.content.upper() == "SYSCALL":
            self.op.content = int(self.op.content)
    def __repr__(self):
        return f'<{self.label.content+" " if self.label is not None else ""}{self.command.content} {self.op.content}>'
    def run(self, data, acc, pc):
        return run_funcs[self.command.content.upper()](self.op.content, data, acc, pc)
class StatementBuilder():
    def __init__(self):
        self.processed_label = False
        self.processed_command = False
        self.processed_op = False
        self.label = None
        self.command = None
        self.op = None
    
    def add(self, token):
        if token.type == label and not self.processed_label:
            self.label = token
            self.processed_label = True
        elif token.type == command and not self.processed_command:
            self.command = token
            self.processed_command = True
        elif (token.type == op or token.type == hashed_op) and self.processed_command and not self.processed_op:
            self.op = token
            self.processed_op = True
        else:
            raise RuntimeError("Invalid Statement")
    def is_ready(self):
        return self.processed_op

    def get_statement(self):
        statement = Statement(self.label, self.command, self.op)
        self.processed_label = False
        self.processed_command = False
        self.processed_op = False
        self.label = None
        self.command = None
        self.op = None
        return statement