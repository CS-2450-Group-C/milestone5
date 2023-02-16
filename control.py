"""These are functions to control the flow of the UVSim
machine. They can branch and halt the machine"""

def branch(self, memory_index):
    # Set the program counter to the new memory location
    self.tick(memory_index)

def branch_neg(self, memory_index):
    # If the accumulator is negative, branch to memory_index
    if self.accumulator < 0:
        # Set the program counter to the new memory location
        self.tick(memory_index)

def branch_zero(self, memory_index):
    if self.accumulator == 0:
        # Set the program counter to the new memory location
        self.tick(memory_index)

def halt(self):
    # Stop the program until the user indicates if they want
    # to quit the program or not
    halted = True
    while halted:
        # Validate the user input data
        user_continue = input('Program halted. Continue? (y/n): ')
        if len(user_continue) > 1:
            print("Please input either 'y' or 'n' ")
            continue
        
        user_continue.lower()
        if user_continue not in 'yn':
            print("Please input either 'y' or 'n' ")
            continue

        if user_continue == 'y':
            halted = False
    
        # Exit the program by setting the program counter 
        # outside of memory
        self.tick(len(self.memory))

def main():
    """For testing purpose"""
    halt(1)

if __name__ == '__main__':
    main()