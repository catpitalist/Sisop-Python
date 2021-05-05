from token import Token, label, op, hashed_op, command, branch_commands
from statement import Statement, StatementBuilder

def lexer(filename):
    token_list = []
    variable_map = {}
    code_block = False
    data_block = False
    data_store = False
    last_var = None
    with open(filename) as f:
        words = [word for line in f.readlines() for word in line.split()]
        for word in words:
            if word == ".code":
                code_block = True
                continue
            if word == ".endcode":
                code_block = False
                continue
            if word == ".data":
                data_block = True
                continue
            if word == ".enddata":
                data_block = False
                continue
            
            if code_block:
                token_list.append(Token(word))
            elif data_block:
                if not data_store:
                    last_var = word
                    variable_map[word] = None
                    data_store = True
                else:
                    variable_map[last_var] = int(word)
                    last_var = None
                    data_store = False
        return token_list, variable_map

def substitute_labels(statement_list, label_map):
    keys = label_map.keys
    for statement in statement_list:
        if statement.command.content in branch_commands:
            statement.op.content = (label_map[statement.op.content])

def parser(token_list):
    statement_list = []
    statement_n = 0
    labels = {}
    builder = StatementBuilder()
    for token in token_list:
        builder.add(token)
        if token.type == label:
            labels[token.content[:-1]] = statement_n
        if builder.is_ready():
            statement_list.append(builder.get_statement())
            statement_n += 1
    substitute_labels(statement_list, labels)
    return statement_list
