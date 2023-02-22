from uvsim import Machine
from Parser import Parser
from formatWord import format_word
import tkinter as tk
from tkinter import filedialog

class GUI:
    def __init__(self, machine):
        self._machine = machine
        self._root = None
        self._mem_labels = []
        self._output = None
        self.make_window()
    
    def make_window(self):
        """Creates the window and adds all elements"""
        self._root = tk.Tk()
        self._root.grid_rowconfigure(0, weight=1)
        self._root.columnconfigure(0, weight=1)
        self._root.resizable(width=False, height=False)

        ## Memory widget 
        # Create container to keep at left side of window
        mem_container = tk.Frame(self._root)
        mem_container.grid(row=0, column=0)
        # Create frame for memory
        mem_frame = tk.Frame(mem_container)
        mem_frame.grid(row=0, column=0, pady=5, sticky=tk.NW)
        mem_frame.grid_rowconfigure(1, weight=1)
        mem_frame.grid_columnconfigure(0, weight=1)
        mem_frame.grid_propagate(False)
        mem_frame.config(width=175, height=485)
        # Create label
        label = tk.Label(mem_frame, text="Memory")
        label.grid(row=0, column=0, sticky=tk.EW)
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
        # Create container to keep at the right side of window
        general_container = tk.Frame(self._root, bg="orange")
        general_container.grid(row=0, column=1, sticky=tk.NS)
        # Create import button
        import_button = tk.Button(general_container, bg="green", text ="Import", command=self.import_memory)
        import_button.grid(row=0, column=0, sticky=tk.W)
        # Create run button
        run_button = tk.Button(general_container, bg="green", text="Run")
        run_button.grid(row=1, column=0, sticky=tk.W)
        # Create Input Field
        input_label = tk.Label(general_container, text="Input")
        input_label.grid(row=2, column=0, sticky=tk.W)
        input_field = tk.Entry(general_container)
        input_field.grid(row=3, column=0, sticky=tk.W)
        # Create output console
        output_label = tk.Label(general_container, text="Output")
        output_label.grid(row=4, column=0, sticky=tk.W)
        self._output = tk.Text(general_container)
        self._output.grid(row=5, column=0, sticky=tk.W)
        self._output.config(state=tk.DISABLED)
        self.print_to_output("Testing")

        self._root.mainloop()



    def import_memory(self):
        """Import memory from a given file"""
        self._root.filename = filedialog.askopenfilename(initialdir="./", title="Select a text file containing BasicML code", filetypes=(('text files', '.txt'),))
        try:
            parser = Parser()
            memory = parser.parse(self._root.filename)
        except ValueError as ex:
            self.print_to_output(f"Error: File {self._root.filename.split('/')[-1]} is not formatted properly")
            self.print_to_output(str(ex))
            return
        self._machine.set_memory(memory)
        self.update_memory_labels()
        self.print_to_output(f"File {self._root.filename.split('/')[-1]} was imported successfully")


    def update_memory_labels(self):
        """Sets the GUI labels with words from memory machine"""
        mem = self._machine.get_memory()
        for loc, word in enumerate(mem):
            self._mem_labels[loc].config(text=format_word(word))


    def print_to_output(self, text, end="\n"):
        self._output.config(state=tk.NORMAL)
        self._output.insert(tk.END, text + end)
        self._output.config(state=tk.DISABLED)


def main():
    """For testing purposes only."""
    memory = [5689, -2451, +1254, 123, -34]
    machine = Machine(memory)
    gui = GUI(machine)


if __name__ == "__main__":
    main()
