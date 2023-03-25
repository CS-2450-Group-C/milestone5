class Arithmetic:
    def __init__(self, parent):
        self._parent = parent

    def __call__(self, op_code, memory_index):
        '''A branching method of all the arithmetic operations.
        Possible op_codes:
            "0": add from memory location and accumulator to accumulator
            "1": subtract memory location and accumulator to accumulator
            "2": divide memory location and accumulator to accumulator
            "3": multiply memory location and accumulator to accumulator'''
        if op_code == "0":
            self.add(memory_index)
        elif op_code == "1":
            self.subtract(memory_index)
        elif op_code == "2":
            self.divide(memory_index)
        elif op_code == "3":
            self.multiply(memory_index)

    def add(self, memory_index):
        '''Add word from memory to word in accumulator'''
        accumulator = self._parent.get_accumulator()
        word = self._parent.get_memory_at_address(memory_index)
        self._parent.set_accumulator(accumulator + word)

    def subtract(self, memory_index):
        '''Subtract word from memory from the word in accumulator'''
        accumulator = self._parent.get_accumulator()
        word = self._parent.get_memory_at_address(memory_index)
        self._parent.set_accumulator(accumulator - word)

    def divide(self, memory_index):
        '''Divide word in accumulator by word in a memory index. NOTE: This
        function does floor division, which removes any decimal values'''
        accumulator = self._parent.get_accumulator()
        word = self._parent.get_memory_at_address(memory_index)
        self._parent.set_accumulator(accumulator // word)

    def multiply(self, memory_index):
        '''Multiply word in accumulator by word in a memory index'''
        accumulator = self._parent.get_accumulator()
        word = self._parent.get_memory_at_address(memory_index)
        self._parent.set_accumulator(accumulator * word)
