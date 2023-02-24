'''Main module. Enables the invocation and running of the UVSim machine'''
import sys
from uvsim import Machine
from parse import parse
from gui import GUI
from Input import Input
from formatWord import format_word

def main():
    '''Main function. reads the invocation parameters, calls the file parser,
    and makes the machine'''
    ## Run from gui if no file is given
    if len(sys.argv) < 2:
        gui = GUI()
        gui.make_window()
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
        if machine.get_needs_input() > -1:
            print(f"Awaiting input for memory location {machine.get_needs_input()}...")
            input = Input()
            word = input.get_input()
            machine.set_memory_at_address(machine.get_needs_input(), word)
            print(f"{format_word(word)} was stored at memory address {machine.get_needs_input()}.")
            print()



if __name__ == "__main__":
    main()
