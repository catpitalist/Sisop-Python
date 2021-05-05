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
    while True:
        print("|1) Load File")
        print("|2) Select Scheduler")
        print("|3) Run")
        print("|4 Quit")
        try:
            selection = int(input("> "))
            if selection < 0 or selection > 4:
                raise RuntimeError()
        except:
            print("Not a valid option!")
        if selection == 1:
            try:
                queue.push(menu_load())
            except:
                print("Couldn't read the file!")
        elif selection == 2:
            scheduler = menu_scheduler()
        elif selection == 3:
            menu_run(queue, scheduler)
        elif selection == 4:
            print("| Goodbye!")
            exit()

def menu_load():
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
            raise RuntimeError()
    except:
        print(" | Hey, that wasn't a valid priority!")
        print(" | I'm taking you back.")
        print("/")
        return
    try:
        code, data = lexer(filename)
        code = parser(code)
        process = Process(code, data, filename, arrival, priority=priority)
        return process
    except FileNotFoundError:
        try:
            code, data = lexer(f'{filename}.txt')
            code = parser(code)
            process = Process(code, data, filename, arrival, priority=priority)
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
                if quantum < 0:
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
    print(f'TIMER: {timer}')
    while not (queue.is_empty() and scheduler.is_empty() and scheduler.cur_process == None):
        while(not queue.is_empty() and queue.peek_priority() == timer):
            scheduler.add_to_ready(queue.pop())
        scheduler.interrupt(timer, pc, acc)
        acc, pc = scheduler.load_if_none(acc, pc)
        if scheduler.cur_process == None:
            print(f'Current Process: NONE')
        else:
            print(f'Current Process {scheduler.cur_process.name}')
        print(f'Ready:')
        for item in scheduler.ready.queue:
            print(item.name)
        print(f'Blocked:')
        for process in scheduler.blocked._data:
            print(process[2].name)
        print(f'Done:')
        for process in done:
            print(process.name)
        try:
            acc, pc = scheduler.run(acc, pc)
        except syscall.SyscallHalt:
            process = scheduler.cur_process
            process.downtime = (timer+1) - process.uptime - process.arrival
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
    print("\n-----\n")
    for process in done:
        print(f'{process.name}\nuptime: {process.uptime} time units\ndowntime: {process.downtime} time units \nturnarround:{process.turnaround}\n-----\n')


def main():
    print("-----------------------------------------------------")
    print("                  W E L C O M E                      ")
    print("                   TO  min_OS                        ")
    print("-----------------------------------------------------")
    main_menu()

main()