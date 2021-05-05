import heapq

class PriorityQueue():
    def __init__(self, first = None, key = lambda x:x):
        self.key = key
        self.index = 0
        if first:
            self._data = [(key(item), i, item) for i, item in enumerate(first)]
            self.index = len(self._data)
            heapq.heapify(self._data)
        else:
            self._data = []
    def push(self, item):
        heapq.heappush(self._data, (self.key(item), self.index, item))
        self.index += 1
    def pop(self):
        p = heapq.heappop(self._data)
        return p[2]
    def is_empty(self):
        if not self._data:
            return True
        return False
    def peek_priority(self):
        return self._data[0][0]