class JQueue:
    def __init__(self):
        self.queue = []
    def push(self, element):
        self.queue.append(element)
    def pop(self):
        self.queue.pop(0)
    def size(self):
        return len(self.queue)
    def toList(self):
        return self.queue
