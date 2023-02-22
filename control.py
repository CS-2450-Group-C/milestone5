class Control:
    def __init__(self, parent):
        self._parent = parent

    def interpret(self, op_code, memory_index):
        '''A branching method of all the branch operation.
        Possible op_codes:
            "0": branch to memory location
            "1": branch to memory location if accumulator is negative
            "2": branch to memory location if accumulator is zero
            "3": halt machine operation'''
        if op_code == "0":
            self.branch(memory_index)
        elif op_code == "1":
            self.branch_neg(memory_index)
        elif op_code == "2":
            self.branch_zero(memory_index)
        elif op_code == "3":
            self.halt()

    def branch(self, memory_index):
        '''Set the program counter to the new memory location'''
        self._parent.set_program_counter(memory_index)

    def branch_neg(self, memory_index):
        '''If the accumulator is negative, branch to memory_index'''
        if self._parent.get_accumulator() < 0:
            # Set the program counter to the new memory location
            self._parent.set_program_counter(memory_index)

    def branch_zero(self, memory_index):
        '''If the accumulator is zero, branch to memory_index'''
        if self._parent.get_accumulator() == 0:
            # Set the program counter to the new memory location
            self._parent.set_program_counter(memory_index)

    def halt(self):
        '''Stop the program'''
        self._parent.halt()