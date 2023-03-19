from uvsim import Machine
from Parser import Parser
from Input import Input
from formatWord import format_word
import tkinter as tk
from tkinter import filedialog
from tkinter import colorchooser
import contextlib
import io

class GUI:
    def __init__(self, machine=Machine()):
        self._machine = machine
        self._root = None
        self._color_window = None
        self._mem_labels = []
        self._output = None
        self._input_entry = None
        self._input_button = None
        self._input_value = None
        self._colors = {
            "main" : "#FFFFFF",
            "accent" : "#FFFFFF"
        }
    
    def make_window(self):
        """Creates the window and adds all elements."""
        
        ## Standard variables
        default_left_padding = (30, 0)
        default_vert_padding = (20, 0)
        default_button_color = "#23350d"
        background_color = "#4c721d"
        text_color = "#FFF"
        label_color = "#75af2d"
        input_background_color = "#FFF"
        output_background_color = "#FFF"
        mem_button_padding = (0, 10)
        small_button_height = 2
        small_button_width = 6
        
        # Initialize the window
        self._root = tk.Tk()
        self._root.configure(bg=background_color)
        self._root.grid_rowconfigure(0, weight=1)
        self._root.columnconfigure(0, weight=1)
        self._root.resizable(width=False, height=False)
        
        # Create container to keep at the right side of window
        general_container = tk.Frame(self._root, bg=background_color)
        general_container.grid(row=0, column=0, sticky=tk.NS)
        
        # Create import button
        action_button_container = tk.Frame(general_container, bg=background_color)
        action_button_container.grid(
            row=0, 
            column=0,
            sticky=tk.W
        )
        import_button = tk.Button(
            action_button_container, 
            bg=default_button_color, 
            text ="Import",
            fg=text_color, 
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
            action_button_container, 
            bg=default_button_color, 
            text="Run",
            fg=text_color,
            command=self.run,
            width=15,
            height=3)
        run_button.grid(
            row=0, 
            column=1, 
            padx=default_left_padding, 
            pady=default_vert_padding, 
            sticky=tk.W)
        
        # Create color button
        color_button = tk.Button(
            action_button_container, 
            bg=default_button_color, 
            text="Color",
            fg=text_color,
            # TODO: Change the command to the color picker
            command=self.open_color_menu,
            width=10,
            height=3)
        color_button.grid(
            row=0, 
            column=2, 
            padx=default_left_padding, 
            pady=default_vert_padding, 
            sticky=tk.W)
        
        # Create Input Entry
        input_container = tk.Frame(general_container, bg=background_color)
        input_container.grid(
            row=2, 
            column=0,
            pady=default_vert_padding, 
            sticky=tk.W)
        input_label = tk.Label(
            input_container, 
            text="Input",
            bg=label_color)
        input_label.grid(
            row=2, 
            column=0, 
            padx=default_left_padding,
            pady=default_vert_padding, 
            sticky=tk.W)
        input_entry = tk.Entry(
            input_container,
            bg=input_background_color,
            width=30)
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
            bg=default_button_color, text="Enter",
            fg=text_color,
            height=small_button_height,
            width=small_button_width,
            command=lambda: self._input_value.set(self._input_entry.get()))
        input_button.grid(
            row=3, 
            column=1,
            padx=(15, 0))
        self._input_button = input_button
        
        # Create console container
        console_container = tk.Frame(general_container, bg=background_color)
        console_container.grid(
            row=3, 
            column=0,
            pady=(0, 20),
            sticky=tk.W
        )

        # Create output console
        output_label = tk.Label(
            console_container,
            bg=label_color,
            text="Output")
        output_label.grid(
            row=0, 
            column=0,
            padx=default_left_padding,
            pady=default_vert_padding, 
            sticky=tk.W)
        self._output = tk.Text(
            console_container,
            bg=output_background_color)
        self._output.grid(row=1, column=0, padx=(30, 15), sticky=tk.W)
        self._output.config(state=tk.DISABLED)
        self.print_to_output("Welcome to the UVSim")

        # Clear console button
        clear_button = tk.Button(
            console_container, 
            bg=default_button_color, text="Clear",
            fg=text_color,
            height=small_button_height,
            width=small_button_width,
            command=lambda: self._input_value.set(self._input_entry.get()))
        clear_button.grid(
            row=2, 
            column=0,
            padx=(0,15),
            pady=(5,0),
            sticky=tk.E)
        self._input_button = input_button

        ## Memory widget 
        # Create container to keep at left side of window
        mem_container = tk.Frame(self._root, bg=background_color)
        mem_container.grid(row=0, column=1, padx=(20, 20))
        # Create frame for memory
        mem_frame = tk.Frame(mem_container, bg=background_color)
        mem_frame.grid(row=0, column=0, pady=5, sticky=tk.NW)
        mem_frame.grid_rowconfigure(1, weight=1)
        mem_frame.grid_columnconfigure(0, weight=1)
        mem_frame.grid_propagate(False)
        mem_frame.config(width=250, height=570)
        # Create label
        label = tk.Label(
            mem_frame,
            bg=label_color,
            text="Memory")
        label.grid(row=0, column=0, sticky=tk.NW)
        # Create canvas for scrolling
        mem_canvas = tk.Canvas(
            mem_frame, 
            bg=output_background_color)
        mem_canvas.grid(row=1, column=0, sticky=tk.NSEW)
        # Create scrollbar for scrolling
        mem_scroll = tk.Scrollbar(mem_frame, orient=tk.VERTICAL, command=mem_canvas.yview)
        mem_scroll.grid(row=1, column=1, sticky=tk.NS)
        mem_canvas.configure(yscrollcommand=mem_scroll.set)
        # Create frame for memory grid placement
        mem_grid = tk.Frame(mem_canvas, bg=output_background_color)
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

        # Memory buttons
        mem_buttons_container = tk.Frame(mem_container, bg=background_color)
        mem_buttons_container.grid(row=1, column=0, pady=(0,5), sticky=tk.NW)

        # Copy button
        copy_button = tk.Button(
            mem_buttons_container, 
            bg=default_button_color, text="Copy",
            fg=text_color,
            height=small_button_height,
            width=small_button_width,
            # TODO: Implement copy functionality
            command=lambda: self._input_value.set(self._input_entry.get()))
        copy_button.grid(
            row=0, 
            column=0,
            padx=mem_button_padding)
        
        # Cut button
        cut_button = tk.Button(
            mem_buttons_container, 
            bg=default_button_color, text="Cut",
            fg=text_color,
            height=small_button_height,
            width=small_button_width,
            # TODO: Implement cut functionality
            command=lambda: self._input_value.set(self._input_entry.get()))
        cut_button.grid(
            row=0, 
            column=1,
            padx=mem_button_padding)
        
        # Paste button
        paste_button = tk.Button(
            mem_buttons_container, 
            bg=default_button_color, text="Paste",
            fg=text_color,
            height=small_button_height,
            width=small_button_width,
            # TODO: Implement paste functionality
            command=lambda: self._input_value.set(self._input_entry.get()))
        paste_button.grid(
            row=0, 
            column=2,
            padx=mem_button_padding)
        
        # Save button
        save_button = tk.Button(
            mem_buttons_container, 
            bg=default_button_color, text="Save",
            fg=text_color,
            height=small_button_height,
            width=small_button_width,
            # TODO: Implement save functionality
            command=lambda: self._input_value.set(self._input_entry.get()))
        save_button.grid(
            row=1, 
            column=0,
            padx=mem_button_padding,
            sticky=tk.W)
        
        # Save button
        save_as_button = tk.Button(
            mem_buttons_container, 
            bg=default_button_color, text="Save As",
            fg=text_color,
            height=small_button_height,
            width=small_button_width,
            # TODO: Implement save as functionality
            command=lambda: self._input_value.set(self._input_entry.get()))
        save_as_button.grid(
            row=1, 
            column=1,
            padx=mem_button_padding,
            sticky=tk.W)

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

    def open_color_menu(self):
        # Ensure color picker window doesn't exist
        if self._color_window is None or not tk.Toplevel.winfo_exists(self._color_window):
            # Make new window
            self._color_window = tk.Toplevel(self._root)
            self._color_window.title("Color Picker")
            self._color_window.geometry("300x150")
        
            # Add color picker buttons
            tk.Label(self._color_window,
                text="Main Color").pack()
            tk.Button(self._color_window, 
                text="Pick Main Color",
                command=lambda: self.change_color("main")).pack()
            tk.Label(self._color_window,
                text="Accent Color").pack()
            tk.Button(self._color_window, 
                text="Pick Accent Color",
                command=lambda: self.change_color("accent")).pack()
        else:
            # Bring prexisting color picker window to the front
            self._color_window.lift()


    def change_color(self, key):
        selectedColor = "#FFFFFF"
        selectedColor = colorchooser.askcolor()[1]
        self._color_window.lift()
        
        if selectedColor is not None:
            self._colors[key] = selectedColor
        print("Main color is " + self._colors["main"])
        print("Accent color is " + self._colors["accent"])


def main():
    """For testing purposes only."""
    # Prints 1234 when run
    memory = [1102, 4300, 1234]
    machine = Machine(memory)
    gui = GUI(machine)
    gui.make_window()

if __name__ == "__main__":
    main()
