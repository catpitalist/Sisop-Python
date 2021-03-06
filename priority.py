from queue import Queue
from priority_queue import PriorityQueue

class PriorityScheduler():
    def __init__(self):
        super().__init__()
        self.cur_process = None
        self.ready = PriorityQueue(key=lambda x:x.priority)
        self.blocked = PriorityQueue(key=lambda x:x.blocked_time)
        self.internal_timer = 0
        self.done = []
    def add_to_ready(self, process):
        self.ready.push(process)
    def add_to_blocked(self, process):
        self.blocked.push(process)
    def pop_from_ready(self):
        return self.ready.pop()
    def pop_from_blocked(self):
        return self.blocked.pop()
    def run(self, acc, pc):
        self.internal_timer += 1 # Tick
        if self.cur_process is not None:
            self.cur_process.uptime += 1
            acc, pc = self.cur_process.run(acc, pc)
        return acc, pc
    def update_ready(self, criteria):
        if self.blocked.is_empty():
            return
        while(self.blocked.peek_priority() < criteria):
            process = self.blocked.pop()
            process.blocked_time = 0
            self.add_to_ready(process)
            if self.blocked.is_empty():
                return
    def block(self, timer, amount, pc, acc):
        self.cur_process.blocked_time = timer + amount
        self.cur_process.blocked += amount
        self.cur_process.pc = pc
        self.cur_process.acc = acc
        self.add_to_blocked(self.cur_process)
        self.cur_process = None
    def load_if_none(self, acc, pc):
        if self.cur_process is None and not self.ready.is_empty():
            self.cur_process = self.pop_from_ready()
            return self.cur_process.acc, self.cur_process.pc
        return acc, pc
    def interrupt(self, timer, pc, acc):
        if self.cur_process is None:
            return
        if not self.ready.is_empty() and self.ready.peek_priority() < self.cur_process.priority:
            self.cur_process.pc = pc
            self.cur_process.acc = acc
            self.add_to_ready(self.cur_process)
            self.cur_process = None
        
    def is_done(self, pc, timer):
        if self.cur_process is not None:
            if self.cur_process.size <= pc:
                self.cur_process.turnaround =  timer - self.cur_process.arrival
                self.cur_process.waiting = self.cur_process.turnaround - self.cur_process.uptime - self.cur_process.blocked
                self.done.append(self.cur_process)
                self.cur_process = None
    def halt_done(self, pc, timer):
        if self.cur_process is not None:
            self.cur_process.turnaround = timer - self.cur_process.arrival
            self.cur_process.waiting = self.cur_process.turnaround - self.cur_process.uptime - self.cur_process.blocked
            self.done.append(self.cur_process)
            self.cur_process = None
    
    def str_done(self):
        s = "[ "
        flag = False
        for done in self.done:
            flag = True
            s = s + done.name + ", "
        if flag:
            s = s[:-2]+ " "
        s = s + "]"
        return s
    
    def is_empty(self):
        return self.ready.is_empty() and self.blocked.is_empty()
   
    def str_blocked(self):
            s = "[ "
            flag = False
            for blocked in self.blocked.queue:
                flag = True
                s = s + blocked[2].name + ", "
            if flag:
                s = s[:-2]+ " "
            s = s + "]"
            return s

    def str_ready(self):
        s = "[ "
        flag = False
        for ready in self.ready.queue:
            flag = True
            s = s + ready[2].name + ", "
        if flag:
            s = s[:-2]+ " "
        s = s + "]"
        return s