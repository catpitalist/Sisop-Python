from assembly_parser import lexer, parser
from process import Process
from priority_queue import PriorityQueue

def input_program():
    filename = input("What is the file you want to load? ")
    time = int(input("What is the arrival time?(integers only) "))
    code, data = lexer(filename)
    code = parser(code)
    process = Process(code, data, time, filename)
    return process

def input_programs():
    queue = PriorityQueue(key=lambda x:x.arrival)
    while k := input("Do you want to input a program? (y/n) ") == 'y':
        queue.push(input_program())
    return queue