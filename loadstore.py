class LoadStore:
    def __init__(self, parent):
        self._parent = parent

    def __call__(self, op_code, memory_index):
        '''A branching method of all the load/store operations.
        Possible op_codes:
            "0": load from memory location to accumulator
            "1": store from accumulator to memory location'''
        if op_code == "0":
            self.load(memory_index)
        elif op_code == "1":
            self.store(memory_index)
        else:
            # Invalid instruction
            return -1
        return 0

    def load(self, memory_index):
        '''Load what is at a location in memory to the accumulator'''
        word = self._parent.get_memory_at_address(memory_index)
        self._parent.set_accumulator(word)

    def store(self, memory_index):
        '''Store what is in the accumulator into a location in memory'''
        word = self._parent.get_accumulator()
        self._parent.set_memory_at_address(memory_index, word)