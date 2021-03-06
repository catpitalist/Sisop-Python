from assembly_parser import lexer, parser
from roundrobin import RoundRobinScheduler
from priority import PriorityScheduler
from priority_queue import PriorityQueue
from process import Process
import syscall
import random
def main_menu():
    scheduler = None
    queue = PriorityQueue(key=lambda x:x.arrival)
    id = 0
    while True:
        print("|1) Load File")
        print("|2) Select Scheduler")
        print("|3) Run")
        print("|4) Quit")
        selection = -1
        try:
            selection = int(input("> "))
            if selection < 0 or selection > 4:
                raise RuntimeError()
        except:
            print("Not a valid option!")
        if selection == 1:
            try:
                queue.push(menu_load(id))
                id += 1
            except:
                print("Couldn't read the file!")
        elif selection == 2:
            scheduler = menu_scheduler()
        elif selection == 3:
            menu_run(queue, scheduler)
            scheduler = None
        elif selection == 4:
            print("| Goodbye!")
            exit()

def menu_load(id):
    print("\\")
    print(" | Ok! What is the name of the file you want to load?")
    filename = input(" > ")
    print(" | Also, what is the arrival time? (positive integers only!)")
    try:
        arrival = int(input(" > "))
    except:
        print(" | Hey, that wasn't a positive integer!")
        print(" | I'm taking you back.")
        print("/")
        return
    print(" | Finally, let's give this process a priority (0, 1, 2) [0 is high!]")
    try:
        priority = int(input(" > "))
        if priority < 0 or priority > 3:
            print("I will assume that this was a low priority task.")
            priority = 2
    except:
        print(" | Hey, that wasn't a valid priority!")
        print(" | I'm taking you back.")
        print("/")
        return
    try:
        code, data = lexer(filename)
        code = parser(code)
        process = Process(code, data, filename+" ["+str(id)+"]", arrival, priority=priority)
        return process
    except FileNotFoundError:
        try:
            code, data = lexer(f'{filename}.txt')
            code = parser(code)
            process = Process(code, data, filename+" id - "+str(id), arrival, priority=priority)
            return process
        except:
            print(" | Hey, that wasn't a valid file!")
            print(" | I'm taking you back.")
            print("/")
            return


def menu_scheduler():
    print("\\")
    print(" |Select a scheduler")
    print(" |1) Round Robin")
    print(" |2) Priority with preemption")
    try:
        selection = int(input(" > "))
        if selection != 1 and selection != 2:
            raise RuntimeError()
        if selection == 1:
            print("| Neat! What is the quantum? (positive integer!)")
            try:
                quantum = int(input(" > "))
                if quantum <= 0:
                    raise RuntimeError()
            except:
                print(" | Hey, that wasn't a valid quantum!")
                print(" | I'm taking you back.")
                print("/")
                return None
            print("/")
            return RoundRobinScheduler(quantum)
        if selection == 2:
            print(" | Neat!")
            print("/")
            return PriorityScheduler()
    except:
        print(" | Hey, that wasn't a scheduler!")
        print(" | I'm taking you back.")
        print("/")
        return None

def menu_run(queue, scheduler):
    print("\\")
    if queue.is_empty():
        print(" | Please load at least one file!")
        return
    if scheduler is None:
        print(" | Please select a scheduler")
    else:
        print(" | Ok! We will start... now!")
        print("/")
        run_os(queue, scheduler)
        
def run_os(queue, scheduler):
    done = []
    timer = 0
    acc = 0
    pc = 0
    while not (queue.is_empty() and scheduler.is_empty() and scheduler.cur_process == None):
        while(not queue.is_empty() and queue.peek_priority() == timer):
            scheduler.add_to_ready(queue.pop())
        scheduler.interrupt(timer, pc, acc)
        acc, pc = scheduler.load_if_none(acc, pc)
        print("----------------------------------")
        print(f'|->Time: {timer}')
        if scheduler.cur_process == None:
            print(f'|Current Process:\tNONE\n')
        else:
            print(f'|Current Process: {scheduler.cur_process.name}')
        print(f'|Ready:\t\t{scheduler.str_ready()}')
        print(f'|Blocked:\t{scheduler.str_blocked()}')
        print(f'|Done:\t\t{scheduler.str_done()}')
        print("----------------------------------")
        print("               -----               ")
        print("                ---                ")
        print("               -----               ")
        try:
            acc, pc = scheduler.run(acc, pc)
        except syscall.SyscallHalt:
            process = scheduler.cur_process
            process.turnaround = timer + 1 - process.arrival
            process.waiting = process.turnaround - process.uptime - process.blocked
            scheduler.halt_done(pc, timer+1)
        except syscall.SyscallWrite:
            #delay = random.randint(10, 40)
            delay = 10
            print(f'\tOUTPUT: {acc}')
            #scheduler.cur_process.pc = pc+1
            scheduler.block(timer, delay, pc+1, acc)
        except syscall.SyscallRead:
            #delay = random.randint(10,40)
            delay = 10
            acc = int(input("> "))
            #scheduler.cur_process.pc = pc+1
            scheduler.block(timer, delay, pc+1, acc)
        scheduler.is_done(pc, timer)
        scheduler.interrupt(timer, pc, acc)
        timer += 1
        scheduler.update_ready(timer)
    for process in scheduler.done:
        print("------------------------------------")
        print(f'|{process.name}')
        print(f'|Processing Time: {process.uptime}')
        print(f'|Waiting: {process.waiting}')
        print(f'|Turnarround: {process.turnaround}')
        print(f'|Blocked: {process.blocked}')
    print("------------------------------------")
def main():
    print("-----------------------------------------------------")
    print("                  W E L C O M E                      ")
    print("                   TO  min_OS                        ")
    print("-----------------------------------------------------")
    main_menu()

main()