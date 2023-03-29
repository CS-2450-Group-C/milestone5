class Memory:

    def __init__(self, num_memory = 250):
        self.i = -1
        self.num_memory = num_memory
        self.memory = [0] * self.num_memory

    def __setitem__(self, index, value):
        self.memory[index] = value
    
    def __getitem__(self, index):
        return self.memory[index]
    
    def __iter__(self):
        self.i = -1
        return self
    
    def __next__(self):
        self.i += 1
        if self.i < self.num_memory:
            return self[self.i]
        raise StopIteration