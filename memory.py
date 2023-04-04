class Memory:

    def __init__(self, num_memory = 250):
        self.i = -1
        self._num_memory = num_memory
        self.memory = [0] * self._num_memory

    def __setitem__(self, index, value):
        self.memory[index] = value
    
    def __getitem__(self, index):
        return self.memory[index]
    
    def set_num_memory(self, num):
        if isinstance(num, int):
            self._num_memory = num
            
    def get_num_memory(self):
        return self._num_memory
    
    def __iter__(self):
        self.i = -1
        return self
    
    def __next__(self):
        self.i += 1
        if self.i < self.get_num_memory():
            return self[self.i]
        raise StopIteration