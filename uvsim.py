'''Module containing the Machine Class.'''
from formatWord import format_word

class Machine:
    '''Machine Class. Represents a machine capable of reading and executing the
    BasicML language.

    Methods:
    tick() returns none
    interpret_instruction(int instruction) returns none
    is_running() returns bool
    debug_get_accumulator() returns signed int
    op_io(int sub_ob, int operand) returns none
    op_ls(int sub_ob, int operand) returns none
    op_ar(int sub_ob, int operand) returns none
    op_br(int sub_ob, int operand) returns none

    other methods are primarily used internally'''

    def __init__(self, init_mem):
        self._accumulator = 0
        self._program_counter = 0
        self._memory = [0000] * 100
        self._running = True
        for i, value in enumerate(init_mem):
            self._memory[i] = value
        print(self._memory)

    def tick(self):
        '''Obtains the next operation, increments the program counter, and
        passes the operation to the interpret_instruction() method for further
        processing.'''
        self._running = True
        operation_address = self._program_counter
        operation = self._memory[operation_address]
        self._program_counter += 1
        if self.interpret_instruction(operation) < 0:
            print(
                f"Error: Invalid instruction \"{operation}\" at memory \
                    address {operation_address}")
            print("Halting program.")
            self._running = False

    def interpret_instruction(self, instruction):
        '''Calls the different instruction set functions with
        (opcode, memory_index) as arguments'''
        if instruction < 0:
            return -1
        str_instruction = str(instruction)

        if str_instruction[0] == "1":
            self.op_io(str_instruction[1], int(str_instruction[2:]))
        elif str_instruction[0] == "2":
            self.op_ls(str_instruction[1], int(str_instruction[2:]))
        elif str_instruction[0] == "3":
            self.op_ar(str_instruction[1], int(str_instruction[2:]))
        elif str_instruction[0] == "4":
            self.op_br(str_instruction[1], int(str_instruction[2:]))
        else:
            return -1
        return 0

    def is_running(self):
        '''Returns the current running state of the machine instance'''
        return self._running
    
    def get_memory(self):
        return self._memory

    def debug_get_program_counter(self):
        '''Returns current value of the machine program counter for debuging and
        testing puposes.'''
        return self._program_counter

    def debug_get_accumulator(self):
        '''Returns current value of the machine accumulator for debuging and
        testing puposes.'''
        return self._accumulator

    def debug_set_accumulator(self, val):
        '''Sets current value of the machine accumulator for testing 
        puposes.'''
        self._accumulator = val

    def op_io(self, op_code, memory_index):
        '''A branching method of all the input/output operations.
        Possible op_codes:
            "0": read from keyboard to memory location
            "1": write from memory location to screen'''
        if op_code == "0":
            self.read(memory_index)
        elif op_code == "1":
            self.write(memory_index)

    def op_ls(self, op_code, memory_index):
        '''A branching method of all the load/store operations.
        Possible op_codes:
            "0": load from memory location to accumulator
            "1": store from accumulator to memory location'''
        if op_code == "0":
            self.load(memory_index)
        elif op_code == "1":
            self.store(memory_index)

    def op_ar(self, op_code, memory_index):
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

    def op_br(self, op_code, memory_index):
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

    def read(self, memory_index):
        '''Read takes user input and stores that in a location in memory'''
        new_word = input(
            f"Enter a new four-digit word to store in memory location \
                {memory_index}. Ex: +2156, -4328: ")
        word_num = 0
        # If the user input exceeds the maximum word length
        if len(new_word) > 5 or len(new_word) < 4:
            raise ValueError(f"Input word is the wrong length: {new_word} \n")

        try:
            # If the word has a positive or negative symbol
            # check if it can convert to an int
            if len(new_word) == 5:
                word_num = int(new_word[1:])

                # Convert the word to negative if it is negative
                if new_word[0] == "-":
                    word_num *= -1
            # If the word has no symbol, check if it can
            # convert to an int
            else:
                word_num = int(new_word)
        except:
            # Pylint doesn't like
            raise ValueError(f"Invalid word {new_word}\n")
        # this and I don't know why.

        self._memory[memory_index] = word_num

    def write(self, memory_index):
        '''Write a word from a location in memory to the screen'''
        word = self._memory[memory_index]
        print(format_word(word))

    def load(self, memory_index):
        '''Load what is at a location in memory to the accumulator'''
        self._accumulator = self._memory[memory_index]

    def store(self, memory_index):
        '''Store what is in the accumulator into a location in memory'''
        self._memory[memory_index] = self._accumulator

    def add(self, memory_index):
        '''Add word from memory to word in accumulator'''
        self._accumulator += self._memory[memory_index]

    def subtract(self, memory_index):
        '''Subtract word from memory from the word in accumulator'''
        self._accumulator -= self._memory[memory_index]

    def divide(self, memory_index):
        '''Divide word in accumulator by word in a memory index. NOTE: This
        function does floor division, which removes any decimal values'''
        self._accumulator //= self._memory[memory_index]

    def multiply(self, memory_index):
        '''Multiply word in accumulator by word in a memory index'''
        self._accumulator *= self._memory[memory_index]

    def branch(self, memory_index):
        '''Set the program counter to the new memory location'''
        self._program_counter = memory_index

    def branch_neg(self, memory_index):
        '''If the accumulator is negative, branch to memory_index'''
        if self._accumulator < 0:
            # Set the program counter to the new memory location
            self._program_counter = memory_index

    def branch_zero(self, memory_index):
        '''If the accumulator is zero, branch to memory_index'''
        if self._accumulator == 0:
            # Set the program counter to the new memory location
            self._program_counter = memory_index

    def halt(self):
        '''Stop the program'''
        self._running = False
