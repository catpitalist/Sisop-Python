##Symbolic Constants
running_state = 0
blocked_state = 1
exit_state = 2
ready_state = 3

class Process():
    def __init__(self, code, data, name, arrival = 0, priority = 2):
        self.code = code
        self.data = data
        self.acc = 0
        self.pc = 0
        self.size = len(code)
        self.state = ready_state
        self.uptime = 0
        self.arrival = arrival
        self.blocked_time = 0
        self.priority = priority
        self.name = name + f' <{self.priority}>'
    def run(self, acc, pc):
        return self.code[pc].run(self.data, acc, pc)
    def __repr__(self):
        return f'{self.code}\n{self.data}'
    def __str__(self):
        return self.__repr__()
    def set_state(self, state):
        this.state = state
