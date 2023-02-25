from uvsim import Machine
from Parser import Parser
from Input import Input
from formatWord import format_word
import tkinter as tk
from tkinter import filedialog
import contextlib
import io

class GUI:
    def __init__(self, machine=Machine()):
        self._machine = machine
        self._root = None
        self._mem_labels = []
        self._output = None
        self._input_entry = None
        self._input_button = None
        self._input_value = None
    
    def make_window(self):
        """Creates the window and adds all elements."""
        self._root = tk.Tk()
        self._root.grid_rowconfigure(0, weight=1)
        self._root.columnconfigure(0, weight=1)
        self._root.resizable(width=False, height=False)

        ## Memory widget 
        # Create container to keep at left side of window
        mem_container = tk.Frame(self._root)
        mem_container.grid(row=0, column=0, padx=(20, 0))
        # Create frame for memory
        mem_frame = tk.Frame(mem_container)
        mem_frame.grid(row=0, column=0, pady=5, sticky=tk.NW)
        mem_frame.grid_rowconfigure(1, weight=1)
        mem_frame.grid_columnconfigure(0, weight=1)
        mem_frame.grid_propagate(False)
        mem_frame.config(width=250, height=580)
        # Create label
        label = tk.Label(mem_frame, text="Memory")
        label.grid(row=0, column=0, sticky=tk.NW)
        # Create canvas for scrolling
        mem_canvas = tk.Canvas(mem_frame, bg="lightgrey")
        mem_canvas.grid(row=1, column=0, sticky=tk.NSEW)
        # Create scrollbar for scrolling
        mem_scroll = tk.Scrollbar(mem_frame, orient=tk.VERTICAL, command=mem_canvas.yview)
        mem_scroll.grid(row=1, column=1, sticky=tk.NS)
        mem_canvas.configure(yscrollcommand=mem_scroll.set)
        # Create frame for memory grid placement
        mem_grid = tk.Frame(mem_canvas, bg="lightgrey")
        mem_canvas.create_window((0, 0), window=mem_grid, anchor=tk.NW)
        # Create memory location labels and word entry to place into grid
        mem = self._machine.get_memory()
        self._mem_labels 
        for loc, word in enumerate(mem):
            location_label = tk.Label(mem_grid, text=loc)
            word_entry = tk.Label(mem_grid, width=5)
            location_label.grid(row=loc, column=0, sticky=tk.E, padx=2, pady=2)
            word_entry.grid(row=loc, column=1, stick=tk.W, padx=2, pady=2)
            self._mem_labels.append(word_entry)
        self.update_memory_labels()
        # Reconfigure for scrolling
        mem_grid.update_idletasks()
        mem_canvas.config(scrollregion=mem_canvas.bbox("all"))

        ## Buttons, input, output
        default_left_padding = (30, 0)
        default_vert_padding = (20, 0)
        # Create container to keep at the right side of window
        general_container = tk.Frame(self._root, bg="#006080")
        general_container.grid(row=0, column=1, sticky=tk.NS)
        # Create import button
        import_button = tk.Button(
            general_container, 
            bg="#0099CC", 
            text ="Import", 
            command=self.import_memory,
            width=15,
            height=3)
        import_button.grid(
            row=0, 
            column=0, 
            padx=default_left_padding, 
            pady=default_vert_padding, 
            sticky=tk.W)
        # Create run button
        run_button = tk.Button(
            general_container, 
            bg="#0099CC", 
            text="Run", 
            command=self.run,
            width=15,
            height=3)
        run_button.grid(
            row=1, 
            column=0, 
            padx=default_left_padding, 
            pady=default_vert_padding, 
            sticky=tk.W)
        
        # Create Input Entry
        input_container = tk.Frame(general_container, bg="#006080")
        input_container.grid(
            row=2, 
            column=0,
            pady=default_vert_padding, 
            sticky=tk.W)
        input_label = tk.Label(input_container, text="Input")
        input_label.grid(
            row=2, 
            column=0, 
            padx=default_left_padding,
            pady=default_vert_padding, 
            sticky=tk.W)
        input_entry = tk.Entry(input_container, width=30)
        input_entry.grid(
            row=3, 
            column=0, 
            padx=default_left_padding, 
            sticky=tk.W)
        self._input_entry = input_entry
        self._input_value = tk.StringVar()
        
        # Input button (Enter)
        input_button = tk.Button(
            input_container, 
            bg="#0099CC", text="Enter", 
            command=lambda: self._input_value.set(self._input_entry.get()))
        input_button.grid(
            row=3, 
            column=1,
            padx=(15, 0))
        self._input_button = input_button
        
        # Create output console
        output_label = tk.Label(general_container, text="Output")
        output_label.grid(
            row=5, 
            column=0,
            padx=default_left_padding,
            pady=default_vert_padding, 
            sticky=tk.W)
        self._output = tk.Text(general_container)
        self._output.grid(row=6, column=0, pady=(0, 30), padx=(30, 15), sticky=tk.W)
        self._output.config(state=tk.DISABLED)
        self.print_to_output("Welcome to the UVSim")

        self._root.mainloop()


    def import_memory(self):
        """Import memory from a given file."""
        self._root.filename = filedialog.askopenfilename(initialdir="./", title="Select a text file containing BasicML code", filetypes=(('text files', '.txt'),))
        try:
            parser = Parser()
            memory = parser.parse(self._root.filename)
        except ValueError as ex:
            self.print_to_output(f"Error: File {self._root.filename.split('/')[-1]} is not formatted properly")
            self.print_to_output(str(ex))
            return
        self._machine = Machine(memory)
        self.update_memory_labels()
        self.print_to_output(f"File {self._root.filename.split('/')[-1]} was imported successfully")


    def run(self):
        """Run the program."""
        self.print_to_output("Program starting...")
        # Capture terminal output
        captured_output = io.StringIO()
        with contextlib.redirect_stdout(captured_output):
            # Run program
            while self._machine.is_running():
                self._machine.tick()
                if self._machine.get_needs_input() >= 0:
                    self.wait_for_input()
        self.print_to_output(captured_output.getvalue(), '')
        self.print_to_output("Program ended.")
        # Reset the accumulator and program counter
        self._machine.reset()


    def update_memory_labels(self):
        """Sets the GUI labels with words from memory machine."""
        mem = self._machine.get_memory()
        for loc, word in enumerate(mem):
            self._mem_labels[loc].config(text=format_word(word))


    def print_to_output(self, text, end="\n"):
        self._output.config(state=tk.NORMAL)
        self._output.insert(tk.END, text + end)
        self._output.config(state=tk.DISABLED)


    def wait_for_input(self):
        # Wait for input
        while True:
            self.print_to_output(f"Awaiting input for memory location {self._machine.get_needs_input()}...")
            self._input_button.wait_variable(self._input_value)
            word = self._input_value.get()
            # Reset for next input
            self._input_entry.delete(0, tk.END)
            self._input_value = tk.StringVar()
            # Validate Input
            validator = Input()
            validator.validate_input(word)
            if not validator.get_validity():
                self.print_to_output("Error: Input must be a 4-digit number. Please try again.")
                continue
            # Store input
            word = int(word)
            self._machine.set_memory_at_address(self._machine.get_needs_input(), word)
            self.print_to_output(f"{format_word(word)} was stored at memory address {self._machine.get_needs_input()}.")
            self.update_memory_labels()
            break


def main():
    """For testing purposes only."""
    # Prints 1234 when run
    memory = [1102, 4300, 1234]
    machine = Machine(memory)
    gui = GUI(machine)
    gui.make_window()

if __name__ == "__main__":
    main()
