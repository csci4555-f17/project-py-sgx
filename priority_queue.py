from heapq import heappush, heappop
import itertools


# Code from: https://docs.python.org/2/library/heapq.html


class Removed:
    def __init__(self):
        pass


REMOVED = Removed()


class PriorityQueue:
    def __init__(self, priority=id):
        self.heap = []
        self.entries = {}
        self.priority = priority
        self.counter = itertools.count()
        self.removed = 0

    def pop(self):
        while self:
            priority, count, item = heappop(self.heap)
            if item is not REMOVED:
                del self.entries[item]
                return item
            else:
                self.removed -= 1
        raise KeyError('pop from an empty priority queue')

    def insert(self, item, priority=None):
        # type: (object) -> ()
        if priority is None:
            priority = self.priority(item)
        if item in self.entries:
            if self.entries[item][0] == priority:
                return
            else:
                self._remove(item)
        id = next(self.counter)
        entry = [priority, id, item]
        self.entries[item] = entry
        heappush(self.heap, entry)

    def _remove(self, item):
        entry = self.entries[item]
        entry[-1] = REMOVED
        self.removed += 1

    def __nonzero__(self):
        return len(self.heap) > self.removed
