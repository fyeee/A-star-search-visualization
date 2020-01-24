import heapq


class PriorityQueue:

    def __init__(self):
        self.__priority_queue = []

    def get_queue(self):
        return [item[1] for item in self.__priority_queue]

    def is_empty(self):
        return self.__priority_queue == []

    def add(self, element, priority):
        heapq.heappush(self.__priority_queue, (priority, element))

    def exist(self, element):
        return element in self.__priority_queue

    def pop(self):
        priority, element = heapq.heappop(self.__priority_queue)
        return element
