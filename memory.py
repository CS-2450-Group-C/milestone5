class Memory:

    def __init__(self):
        self.i = -1
        self.memory = [0] * 100

    def __setitem__(self, index, value):
        self.memory[index] = value
    
    def __getitem__(self, index):
        return self.memory[index]
    
    def __iter__(self):
        self.i = -1
        return self
    
    def __next__(self):
        self.i += 1
        if self.i < 100:
            return self[self.i]
        raise StopIteration