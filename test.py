import token
import statement
import heapq
import random
import syscall
from assembly_parser import lexer, parser
from process import Process
import loader
from priority_queue import PriorityQueue
from roundrobin import RoundRobinScheduler
#tokens, variables = lexer("test.txt")
#print(tokens)
#print(variables)
#st = parser(tokens)
queue = loader.input_programs()
scheduler = RoundRobinScheduler(1)
done = []
timer = 0
acc = 0
pc = 0
while not (queue.is_empty() and scheduler.is_empty() and scheduler.cur_process == None):
    while(not queue.is_empty() and queue.peek_priority() == timer):
        scheduler.add_to_ready(queue.pop())
    scheduler.interrupt(timer, pc, acc)
    acc, pc = scheduler.load_if_none(acc, pc)
    try:
        acc, pc = scheduler.run(acc, pc)
    except syscall.SyscallHalt:
        process = scheduler.cur_process
        process.downtime = timer - process.uptime - process.arrival
        process.turnaround = process.uptime + process.downtime
        done.append(process)
        scheduler.cur_process = None
    except syscall.SyscallWrite:
        delay = random.randint(10, 40)
        print(acc)
        scheduler.cur_process.pc = pc+1
        scheduler.block(timer, delay, pc, acc)
    except syscall.SyscallRead:
        delay = random.randint(10,40)
        scheduler.cur_process.acc = int(input("> "))
        scheduler.cur_process.pc = pc+1
        scheduler.block(timer, delay, pc, acc)
    scheduler.is_done(pc, timer, done)
    scheduler.interrupt(timer, pc, acc)
    scheduler.update_ready(timer)
    timer += 1
print(done[0].uptime)

