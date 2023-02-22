'''Main module. Enables the invocation and running of the UVSim machine'''
import sys
from uvsim import Machine
from parse import parse
from gui import GUI

def main():
    '''Main function. reads the invocation parameters, calls the file parser,
    and makes the machine'''
    ## Run from gui if no file is given
    if len(sys.argv) < 2:
        gui = GUI()
        return

    ## Run from command line if file is given
    # Fill memory from given file
    memory = []
    try:
        memory = parse(sys.argv[1])
    except ValueError as ex:
        print(ex)
        return
    # Create new machine from parsed memory
    machine = Machine(memory)
    while machine.is_running():
        machine.tick()


if __name__ == "__main__":
    main()
