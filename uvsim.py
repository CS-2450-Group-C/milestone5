'''Module containing the Machine Class.'''

# op imports
from memory import Memory
from inputoutput import InputOutput
from arithmetic import Arithmetic
from loadstore import LoadStore
from control import Control

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

    def __init__(self, init_mem=Memory()):
        self._accumulator = 0
        self._program_counter = 0
        self._memory = Memory()
        self._running = True
        self._needs_input = -1

        self.op_io = InputOutput(self)
        self.op_ar = Arithmetic(self)
        self.op_ls = LoadStore(self)
        self.op_br = Control(self)

        for i, value in enumerate(init_mem):
            self._memory[i] = value
        # print(self._memory)

    def tick(self):
        '''Obtains the next operation, increments the program counter, and
        passes the operation to the interpret_instruction() method for further
        processing.'''
        self._running = True
        self._needs_input = -1
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
    
    def get_needs_input(self):
        return self._needs_input
    
    def set_needs_input(self, memory_index):
        self._needs_input = memory_index
    
    def reset(self):
        '''Prepare machine to rerun program'''
        self._accumulator = 0
        self._program_counter = 0
        self._running = True

    def get_memory(self):
        return self._memory
    
    def set_memory(self, memory):
        self._memory = memory

    def get_memory_at_address(self, address):
        return self._memory[address]
    
    def set_memory_at_address(self, address, word):
        self._memory[address] = word

    def debug_get_program_counter(self):
        '''Returns current value of the machine program counter for debuging and
        testing puposes.'''
        return self._program_counter

    def debug_get_accumulator(self): # depreciate
        '''Returns current value of the machine accumulator for debuging and
        testing puposes.'''
        return self._accumulator

    def debug_set_accumulator(self, val): # depreciate
        '''Sets current value of the machine accumulator for testing 
        puposes.'''
        self._accumulator = val

    def get_accumulator(self):
        '''Returns current value of the machine accumulator for actual
        puposes.'''
        return self._accumulator

    def set_accumulator(self, val):
        '''Sets current value of the machine accumulator for actual puposes.'''
        self._accumulator = val

    def get_program_counter(self):
        '''Returns current value of the machine program counter.'''
        return self._program_counter

    def set_program_counter(self, value):
        '''Sets current value of the machine program counter.'''
        self._program_counter = value

    def halt(self):
        '''Stop the program'''
        self._running = False
