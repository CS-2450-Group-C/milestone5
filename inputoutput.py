from formatWord import format_word
from Input import Input

class InputOutput:
    def __init__(self, parent):
        self._parent = parent

    def __call__(self, op_code, memory_index):
        if op_code == "0":
            self.read(memory_index)
        elif op_code == "1":
            self.write(memory_index)

    def read(self, memory_index):
        '''Read takes user input and stores that in a location in memory'''
        input_obj = Input()
        word = input_obj.get_input()
        self._parent.set_memory_at_address(memory_index, int(word))

    def write(self, memory_index):
        '''Write a word from a location in memory to the screen'''
        word = self._parent.get_memory_at_address(memory_index)
        print(format_word(word))
