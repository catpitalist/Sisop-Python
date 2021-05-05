import heapq

class PriorityQueue():
    def __init__(self, first = None, key = lambda x:x):
        self.key = key
        self.index = 0
        if first:
            self.queue = [(key(item), i, item) for i, item in enumerate(first)]
            self.index = len(self.queue)
            heapq.heapify(self.queue)
        else:
            self.queue = []
    def push(self, item):
        heapq.heappush(self.queue, (self.key(item), self.index, item))
        self.index += 1
    def pop(self):
        p = heapq.heappop(self.queue)
        return p[2]
    def is_empty(self):
        if not self.queue:
            return True
        return False
    def peek_priority(self):
        return self.queue[0][0]