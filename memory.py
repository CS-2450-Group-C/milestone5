class Memory:

    def __init__(self):
        self.memory = [0] * 100

    def __setitem__(self, index, value):
        self.memory[index] = value
    
    def __getitem__(self, index):
        return self.memory[index]