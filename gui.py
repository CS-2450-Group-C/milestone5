'''Module contains everything that main.py needs in order to start and
run the GUI. Create an instance of the class and then call make_window()'''

import tkinter as tk
from tkinter import filedialog
from tkinter import colorchooser
from tkinter import Entry
from pathlib import Path
import contextlib
import io
import json
import pyperclip
from uvsim import Machine
from Parser import Parser
from Input import Input
from memory import Memory
from formatWord import format_word
from color_operations import lighten_color, get_contrasting_text_color


class GUI:
    '''GUI class. Runs fairly autonomously once instance and make_window()
    is run. Such usage probably works but has not been tested.'''
    def __init__(self):
        self._machine = None
        self._root = None
        self._color_window = None
        self._output = None
        self._input_entry = None
        self._input_button = None
        self._input_value = None
        self._colors = None
        self._word_entry_list = None
        self._current_filepath = None
        self._gui_memory = Memory()
        self._gui_clipboard = []
        self.set_default_colors()
        self.read_colors()

    def make_window(self):
        """Creates the window and adds all elements."""

        # Standard variables
        default_left_padding = (30, 0)
        default_vert_padding = (20, 0)
        background_color = self._colors["main"]
        default_button_color = self._colors["accent"]

        label_color = lighten_color(self._colors["accent"])
        button_text_color = get_contrasting_text_color(self._colors["accent"])
        label_text_color = get_contrasting_text_color(label_color)

        # Additional variables
        input_background_color = "#FFF"
        output_background_color = "#FFF"
        mem_button_padding = (0, 10)
        small_button_height = 2
        small_button_width = 6

        # Initialize the window
        self._root = tk.Tk()
        self._root.configure(bg=background_color)
        self._root.rowconfigure(0, weight=1)
        self._root.columnconfigure(0, weight=1)
        self._root.resizable(width=False, height=False)
        self._root.title("UVSim")

        # Create container to keep at the right side of window
        general_container = tk.Frame(self._root, bg=background_color)
        general_container.grid(row=0, column=0, sticky=tk.NS)

        # Create import button
        action_button_container = tk.Frame(
            general_container, bg=background_color)
        action_button_container.grid(
            row=0,
            column=0,
            sticky=tk.W
        )
        tk.Button(
            action_button_container,
            bg=default_button_color,
            text="Import",
            fg=button_text_color,
            command=self.import_memory,
            width=15,
            height=3).grid(
            row=0,
            column=0,
            padx=default_left_padding,
            pady=default_vert_padding,
            sticky=tk.W)

        # Create run button
        tk.Button(
            action_button_container,
            bg=default_button_color,
            text="Run",
            fg=button_text_color,
            command=self.run,
            width=15,
            height=3).grid(
            row=0,
            column=1,
            padx=default_left_padding,
            pady=default_vert_padding,
            sticky=tk.W)
        
        # Create New Window button
        tk.Button(
            action_button_container,
            bg=default_button_color,
            text="New Window",
            fg=button_text_color,
            # TODO: Implement new window function
            command=make_new_window,
            width=15,
            height=3).grid(
            row=0,
            column=2,
            padx=default_left_padding,
            pady=default_vert_padding,
            sticky=tk.W)

        # Create color button
        tk.Button(
            action_button_container,
            bg=default_button_color,
            text="Color",
            fg=button_text_color,
            command=self.open_color_menu,
            width=10,
            height=3).grid(
            row=0,
            column=3,
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
            fg=label_text_color,
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
        self._input_value = tk.StringVar(self._root)

        # Input button (Enter)
        input_button = tk.Button(
            input_container,
            bg=default_button_color, text="Enter",
            fg=button_text_color,
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
            fg=label_text_color,
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
            fg=button_text_color,
            height=small_button_height,
            width=small_button_width,
            command=self.button_clear)
        clear_button.grid(
            row=2,
            column=0,
            padx=(0, 15),
            pady=(5, 0),
            sticky=tk.E)

        # Memory widget
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
            fg=label_text_color,
            bg=label_color,
            text="Memory")
        label.grid(row=0, column=0, sticky=tk.NW)

        # Create canvas for scrolling
        mem_canvas = tk.Canvas(
            mem_frame,
            bg=output_background_color)
        mem_canvas.grid(row=1, column=0, sticky=tk.NSEW)

        # Create scrollbar for scrolling
        mem_scroll = tk.Scrollbar(
            mem_frame, orient=tk.VERTICAL, command=mem_canvas.yview)
        mem_scroll.grid(row=1, column=1, sticky=tk.NS)
        mem_canvas.configure(yscrollcommand=mem_scroll.set)

        # Create frame for memory grid placement
        mem_grid = tk.Frame(mem_canvas, bg=output_background_color)
        mem_canvas.create_window((0, 0), window=mem_grid, anchor=tk.NW)

        # Create memory location labels and word entry to place into grid
        self._word_entry_list = []
        for loc in range(self._gui_memory.get_num_memory()):
            tk.Label(mem_grid, text=loc).grid(
                row=loc + 1, column=0, sticky=tk.E, padx=2, pady=2)
            self._word_entry_list.append(tk.Entry(mem_grid))
            self._word_entry_list[loc].grid(
                row=loc + 1, column=1, stick=tk.W, padx=2, pady=2)
        self.update_gui_from_mem()

        # Reconfigure for scrolling
        mem_grid.update_idletasks()
        mem_canvas.config(scrollregion=mem_canvas.bbox("all"))

        # Memory buttons
        mem_buttons_container = tk.Frame(mem_container, bg=background_color)
        mem_buttons_container.grid(row=1, column=0, pady=(0, 5), sticky=tk.NW)

        # Copy button
        tk.Button(
            mem_buttons_container,
            bg=default_button_color, text="Copy",
            fg=button_text_color,
            height=small_button_height,
            width=small_button_width,
            command=self.open_copy_menu).grid(
            row=0,
            column=0,
            padx=mem_button_padding)

        # Cut button
        tk.Button(
            mem_buttons_container,
            bg=default_button_color, text="Cut",
            fg=button_text_color,
            height=small_button_height,
            width=small_button_width,
            command=self.open_cut_menu).grid(
            row=0,
            column=1,
            padx=mem_button_padding)

        # Paste button
        tk.Button(
            mem_buttons_container,
            bg=default_button_color, text="Paste",
            fg=button_text_color,
            height=small_button_height,
            width=small_button_width,
            command=self.open_paste_menu).grid(
            row=0,
            column=2,
            padx=mem_button_padding)

        # Save button
        tk.Button(
            mem_buttons_container,
            bg=default_button_color, 
            text="Save",
            fg=button_text_color,
            height=small_button_height,
            width=small_button_width,
            command=self.button_save).grid(
            row=1,
            column=0,
            padx=mem_button_padding,
            sticky=tk.W)

        # Save As button
        tk.Button(
            mem_buttons_container,
            bg=default_button_color, text="Save As",
            fg=button_text_color,
            height=small_button_height,
            width=small_button_width,
            command=self.button_save_as).grid(
            row=1,
            column=1,
            padx=mem_button_padding,
            sticky=tk.W)

        self._root.mainloop()

    def final_stringer(self):
        '''Loops through the GUI memory and creates a string containing the words in memory.'''
        final_string = ""
        self.update_mem_from_gui()  # sync-up before stringifying
        self.update_gui_from_mem()
        for i in self._word_entry_list:
            final_string += i.get() + "\n"
        return final_string

    def button_clear(self):
        '''Clears the contents of the console'''
        self._output.config(state=tk.NORMAL)

        # Clear the console textbox
        self._output.delete("1.0", tk.END)

        # Reinsert the welcome text
        self._output.insert(tk.END, "Welcome to the UVSim\n")
        self._output.config(state=tk.DISABLED)

    # def button_copy(self):
    #     '''Uses pyperclip to copy final_string to clipboard.'''
    #     final_string = self.final_stringer()
    #     pyperclip.copy(final_string)

    def gui_copy(self, start_index, end_index, calling_copy_from_cut = False):
        '''Uses pyperclip to copy final_string to clipboard. But mainly it copies
        a data range from the gui into to gui clipboard.'''
        
        # Check to make sure the end_index does not exceed the bounds of memory
        if end_index >= self._gui_memory.get_num_memory():
            self.print_to_output(f"Copy failed: The end index: {end_index} is larger than the maximum index: {self._gui_memory.get_num_memory() - 1}.")
            return
        
        # Check to make sure the indices are not negative
        if start_index < 0 or end_index < 0:
            self.print_to_output(f"Copy failed: A cut index cannot be negative.")
            return
        
        # Check to make sure the end_index is greater than the start_index
        if start_index > end_index:
            self.print_to_output(f"Copy failed: The start index: {start_index} is larger than the end index: {end_index}.")
            return
        
        # Sample data to output to the output box
        min_num_sample = 5
        if (end_index - start_index) >  min_num_sample:
            end_sample = (start_index + min_num_sample)     
        else:
            end_sample = (end_index + 1)
        sample_data = self._gui_memory[start_index:end_sample]
        
        # Copy the data
        final_string = self.final_stringer()
        pyperclip.copy(final_string)
        self.update_mem_from_gui()
        self._gui_clipboard = self._gui_memory[start_index:end_index+1]
        print(self._gui_clipboard)

        # Don't output the successful copy if calling from cut
        if calling_copy_from_cut:
            return
        
        # Output on successful copy
        output_text = f"Successfully copied words from memory address {start_index} to {end_index}:\n"
        sample_text = f"Sample of words that were copied:\n"
        sample_text += " ".join(f"{format_word(sample)}," for sample in sample_data)
        
        if len(sample_data) >= min_num_sample:
            sample_text += "..."
        output_text += f"{sample_text}"

        self.print_to_output(output_text)

    
    def open_copy_menu(self):
        # Style Variables
        label_color = lighten_color(self._colors["accent"])
        label_text_color = get_contrasting_text_color(label_color)
        button_color = self._colors["accent"]
        button_text_color = get_contrasting_text_color(self._colors["accent"])
        background_color = self._colors["main"]
        
        # Make new window
        copy_gui = tk.Toplevel(self._root)
        copy_gui.title("Copy")
        copy_gui.configure(
            bd=5,
            bg=background_color)
        
        # Direction Label
        tk.Label(copy_gui,
                 font=12,
                 bg=background_color,
                 fg=get_contrasting_text_color(background_color),
                 text="Choose the memory range (inclusive) to copy:").pack(pady=(20, 0), padx=(20, 20))
        
        # Start Index Label
        tk.Label(copy_gui,
                 text="Copy Start Index:",
                 fg=label_text_color,
                 bg=label_color).pack(pady=(20, 0))
        
        # Start Index Input Box
        start_index = tk.Entry(copy_gui)
        start_index.pack()
        
        # End Index Label
        tk.Label(copy_gui, 
                 text="Copy End Index:",
                 fg=label_text_color,
                 bg=label_color).pack(pady=(20, 0))
        
        # End Index Input Box
        end_index = tk.Entry(copy_gui)
        end_index.pack()

        # Button
        tk.Button(
            copy_gui, 
            text="Copy",
            bg=button_color,
            fg=button_text_color,
            width = 15, 
            height = 3,
            command=lambda: self.gui_copy(int(start_index.get()), int(end_index.get()))
            ).pack(pady=(20,20))

    def gui_cut(self, start_index, end_index):
        '''Calls gui_copy, then clears memory entries by setting to +0.'''
        
        # Check to make sure the end_index does not exceed the bounds of memory
        if end_index >= self._gui_memory.get_num_memory():
            self.print_to_output(f"Cut failed: The end index: {end_index} is larger than the maximum index: {self._gui_memory.get_num_memory() - 1}.")
            return
        
        # Check to make sure the indices are not negative
        if start_index < 0 or end_index < 0:
            self.print_to_output(f"Cut failed: A cut index cannot be negative.")
            return
        
        # Check to make sure the end_index is greater than the start_index
        if start_index > end_index:
            self.print_to_output(f"Cut failed: The start index: {start_index} is larger than the end index: {end_index}.")
            return
        
        # Sample data to output to the output box
        min_num_sample = 5
        if (end_index - start_index) >  min_num_sample:
            end_sample = (start_index + min_num_sample)     
        else:
            end_sample = (end_index + 1)
        sample_data = self._gui_memory[start_index:end_sample]
        
        # Copy the data to the clipboard, update memory to be 0
        calling_copy_from_cut = True
        self.gui_copy(start_index, end_index, calling_copy_from_cut)
        for i in range(start_index, end_index+1):
            self._gui_memory[i] = 0
        self.update_gui_from_mem()
            
        # Output on successful cut
        output_text = f"Successfully cut words from memory address {start_index} to {end_index}:\n"
        sample_text = f"Sample of words that were cut:\n"
        sample_text += " ".join(f"{format_word(sample)}," for sample in sample_data)
        
        if len(sample_data) >= min_num_sample:
            sample_text += "..."
        output_text += f"{sample_text}"

        self.print_to_output(output_text)

    def open_cut_menu(self):
        # Style Variables
        label_color = lighten_color(self._colors["accent"])
        label_text_color = get_contrasting_text_color(label_color)
        button_color = self._colors["accent"]
        button_text_color = get_contrasting_text_color(self._colors["accent"])
        background_color = self._colors["main"]
        
        # Make new window
        cut_gui = tk.Toplevel(self._root)
        cut_gui.title("Cut")
        cut_gui.configure(
            bd=5,
            bg=background_color)

        # Direction Label
        tk.Label(cut_gui,
                 font=12,
                 bg=background_color,
                 fg=get_contrasting_text_color(background_color),
                 text="Choose the memory range (inclusive) to cut:").pack(pady=(20, 0), padx=(20, 20))
        
        # Start Index Label
        tk.Label(cut_gui,
                 text="Cut Start Index:",
                 fg=label_text_color,
                 bg=label_color).pack(pady=(20, 0))
        
        # Start Index Input Box
        start_index = tk.Entry(cut_gui)
        start_index.pack()

        # End Index Label
        tk.Label(cut_gui, 
                 text="Cut End Index:",
                 fg=label_text_color,
                 bg=label_color).pack(pady=(20, 0))
        
        # End Index Input Box
        end_index = tk.Entry(cut_gui)
        end_index.pack()
        
        # Button
        tk.Button(
            cut_gui, 
            text="Cut",
            bg=button_color,
            fg=button_text_color,
            width = 15, 
            height = 3,
            command=lambda: self.gui_cut(int(start_index.get()), int(end_index.get()))
            ).pack(pady=(20,20))

    def button_paste(self):
        '''Gets what is in paste entry box and puts into memory.'''
        paste_contents = self._paste_entry.get()
        paste_content_lines = 0
        new_memory = []
        for i in paste_contents.splitlines():
            paste_content_lines += 1
            new_memory.append(int(i))
        if paste_content_lines > self._gui_memory.get_num_memory():
            raise Exception(f"Pasted memory is longer than {self._gui_memory.get_num_memory()} lines.")
        for i, word in enumerate(new_memory):
            self._gui_memory[i] = word
        self.update_gui_from_mem()

    def gui_paste(self, paste_index):
        # Check to make sure the paste_index does not exceed the bounds of memory
        if paste_index >= self._gui_memory.get_num_memory():
            self.print_to_output(f"Paste failed: The paste index: {paste_index} is larger than the maximum index: {self._gui_memory.get_num_memory() - 1}.")
            return
        
        # Check to make sure the indices are not negative
        if paste_index < 0:
            self.print_to_output(f"Paste failed: A paste index cannot be negative.")
            return

        # Update the memory for the machine
        self.update_mem_from_gui()
        for i, value in enumerate(self._gui_clipboard):
            if paste_index + i >= self._gui_memory.get_num_memory():
                break
            self._gui_memory[paste_index + i] = value
        # Use the updated memory from the machine to update the gui
        self.update_gui_from_mem()

        # Check if the paste will fit in memory
        if (paste_index + len(self._gui_clipboard)) > self._gui_memory.get_num_memory():
            self.print_to_output(f"Warning: Some data was not pasted. The length of the clipboard added to the paste index exceeds the bounds of memory.")
            
            # Output on partially successful paste
            total_pasted = self._gui_memory.get_num_memory() - paste_index
            output_text = f"Pasted {total_pasted} word(s) starting at memory address {paste_index}."
        else:
            # Output on successful paste
            output_text = f"Successfully pasted to memory address {paste_index}."
        
        # Print the paste message
        self.print_to_output(output_text)


    def open_paste_menu(self):
        # Style Variables
        label_color = lighten_color(self._colors["accent"])
        label_text_color = get_contrasting_text_color(label_color)
        button_color = self._colors["accent"]
        button_text_color = get_contrasting_text_color(self._colors["accent"])
        background_color = self._colors["main"]
        
        # Make new window
        paste_gui = tk.Toplevel(self._root)
        paste_gui.title("Paste")
        paste_gui.configure(
            bd=5,
            bg=background_color)
        
        # Direction Label
        tk.Label(paste_gui,
                 font=12,
                 bg=background_color,
                 fg=get_contrasting_text_color(background_color),
                 text="Choose the memory location to paste:").pack(pady=(20, 0), padx=(20, 20))

        # Paste Index Label
        tk.Label(paste_gui,
                 text="Paste at Index:",
                 fg=label_text_color,
                 bg=label_color).pack(pady=(20, 0))
        
        # Paste Location Input Box
        paste_index = tk.Entry(paste_gui)
        paste_index.pack()

        # Button
        tk.Button(
            paste_gui, 
            text="Paste",
            bg=button_color,
            fg=button_text_color,
            width = 15, 
            height = 3,
            command=lambda: self.gui_paste(int(paste_index.get()))
            ).pack(pady=(20,20))

    def button_save(self):
        '''Save function, uses save-as function if there is no file that has
        been imported or saved as.'''
        if not self._current_filepath:
            self.button_save_as()
            return
        with open(self._current_filepath, "w", encoding="utf-8") as file:
            final_string = self.final_stringer()
            file.write(final_string)

    def button_save_as(self):
        '''Save-as function.'''
        returned = filedialog.asksaveasfile(
            filetypes=[("UVSIM program", "*.txt")], defaultextension=".txt")
        if not returned:
            return
        self._current_filepath = returned.name
        self._root.title(f"UVSim - {self._current_filepath}")
        self.button_save()

    def import_memory(self):
        """Import memory from a given file."""
        self._root.filename = filedialog.askopenfilename(
            initialdir="./", title="Select a text file containing BasicML code",
            filetypes=(('text files', '.txt'),))
        try:
            parser = Parser()
            memory = parser.parse(self._root.filename)
        except ValueError as ex:
            self.print_to_output(
                f"Error: File {self._root.filename.split('/')[-1]} is not formatted properly")
            self.print_to_output(str(ex))
            return
        self._gui_memory = memory
        self.print_to_output(
            f"File {self._root.filename.split('/')[-1]} was imported successfully")
        self._current_filepath = self._root.filename
        self._root.title(f"UVSim - {self._current_filepath}")
        self._root.lift()
        self.update_gui_from_mem()

    def update_gui_from_mem(self):
        '''Copies the GUI's internal memory into GUI memory entry list values'''
        for i, entry in enumerate(self._word_entry_list):
            entry.delete(0, "end")
            if self._gui_memory[i] < 0:
                entry.insert(0, f"{self._gui_memory[i]:07}")
            else:
                entry.insert(0, f"+{self._gui_memory[i]:06}")

    def update_mem_from_gui(self):
        '''Reads the values in the GUI entry list and copies them to the GUI's intenal memory'''
        for i, entry in enumerate(self._word_entry_list):
            entry.delete(7, "end")  # chop off excessive characters
            try:
                self._gui_memory[i] = int(entry.get())
            except ValueError:
                self.print_to_output(
                    f"Error: invalid entry at memory location {i}")
                self._gui_memory[i] = 0

    def run(self):
        """Run the program."""

        self.update_mem_from_gui()
        self._machine = Machine(self._gui_memory)

        self.print_to_output("Program starting...")
        # Capture terminal output
        captured_output = io.StringIO()
        with contextlib.redirect_stdout(captured_output):
            # Run program
            while self._machine.is_running():
                self._machine.tick()
                if self._machine.get_needs_input() >= 0:
                    self.wait_for_input()
                self._gui_memory = self._machine.get_memory()
                self.update_gui_from_mem()
        self.print_to_output(captured_output.getvalue(), '')
        self.print_to_output("Program ended.")
        # Reset the accumulator and program counter
        del self._machine

    def print_to_output(self, text, end="\n"):
        '''Interface to output text in the GUI's log box'''
        self._output.config(state=tk.NORMAL)
        self._output.insert(tk.END, text + end)
        self._output.config(state=tk.DISABLED)

    def wait_for_input(self):
        '''Wait for input'''
        while True:
            self.print_to_output(
                f"Awaiting input for memory location {self._machine.get_needs_input()}...")
            self._input_button.wait_variable(self._input_value)
            word = self._input_value.get()
            # Reset for next input
            self._input_entry.delete(0, "end")
            self._input_value = tk.StringVar(self._root)
            # Quit if machine is destroyed
            if self._machine is None:
                return
            # Validate Input
            validator = Input()
            validator.validate_input(word)
            if not validator.get_validity():
                self.print_to_output(
                    "Error: Input must be a 6-digit number. Please try again.")
                continue
            # Store input
            word = int(word)
            self._machine.set_memory_at_address(
                self._machine.get_needs_input(), word)
            self.print_to_output(
                f"{format_word(word)} was stored at memory address \
{self._machine.get_needs_input()}.")
            break

    def open_color_menu(self):
        '''Creates a color picker window so that the user can change the GUI's
        color while the main program is running'''
        # Ensure color picker window doesn't exist
        if self._color_window is None or not tk.Toplevel.winfo_exists(self._color_window):
            # Make new window
            self._color_window = tk.Toplevel(self._root)
            self._color_window.title("Color Picker")
            self._color_window.geometry("180x280+50+50")
            self._color_window.configure(bg=self._colors["main"])
            self._color_window.grid_columnconfigure(0, weight=1)

            # Set color alts
            label_color = lighten_color(self._colors["accent"])
            button_text_color = get_contrasting_text_color(
                self._colors["accent"])
            label_text_color = get_contrasting_text_color(label_color)

            # Add color picker buttons
            tk.Label(self._color_window,
                     fg=label_text_color,
                     bg=label_color,
                     text="Main Color",
                     width=18
                     ).grid(
                row=0,
                column=0,
                pady=(10, 0)
            )
            tk.Button(self._color_window,
                      fg=button_text_color,
                      bg=self._colors["accent"],
                      text="Pick Main Color",
                      command=lambda: self.set_color("main"),
                      width=18,
                      pady=5
                      ).grid(
                row=1,
                column=0,
                pady=(0, 10)
            )

            tk.Label(self._color_window,
                     fg=label_text_color,
                     bg=label_color,
                     text="Accent Color",
                     width=18
                     ).grid(
                row=2,
                column=0,
            )
            tk.Button(self._color_window,
                      fg=button_text_color,
                      bg=self._colors["accent"],
                      text="Pick Accent Color",
                      command=lambda: self.set_color("accent"),
                      width=18,
                      pady=5
                      ).grid(
                row=3,
                column=0,
                pady=(0, 10)
            )

            tk.Label(self._color_window,
                     fg=label_text_color,
                     bg=label_color,
                     text="Restore Default Colors",
                     width=18
                     ).grid(
                row=4,
                column=0,
            )
            tk.Button(self._color_window,
                      fg=button_text_color,
                      bg=self._colors["accent"],
                      text="Restore Default Colors",
                      command=self.set_default_colors,
                      width=18,
                      pady=5
                      ).grid(
                row=5,
                column=0,
                pady=(0, 10)
            )

            tk.Label(self._color_window,
                     fg=label_text_color,
                     bg=label_color,
                     text="Apply",
                     width=18,
                     ).grid(
                row=6,
                column=0,
            )
            tk.Button(self._color_window,
                      fg=button_text_color,
                      bg=self._colors["accent"],
                      text="Apply",
                      command=self.apply_color,
                      width=18,
                      pady=5,
                      ).grid(
                row=7,
                column=0,
                pady=(0, 10)
            )
        else:
            # Bring prexisting color picker window to the front
            self._color_window.lift()

    def set_color(self, key):
        '''Asks for a new color and then sets it as the color at _colors.key'''
        selected_color = "#FFFFFF"
        selected_color = colorchooser.askcolor(color=self._colors[key])[1]
        self._color_window.lift()

        if selected_color is not None:
            self._colors[key] = selected_color

        # Reopen color window so changes apply
        self._color_window.destroy()
        self._color_window = None
        self.open_color_menu()

    def set_default_colors(self):
        '''Resets custom set color values to hard-coded default values'''
        self._colors = {
            "main": "#4C721D",
            "accent": "#293714"
        }
        # Reopen window to apply changes (only if already open)
        if self._color_window is not None and tk.Toplevel.winfo_exists(self._color_window):
            self._color_window.destroy()
            self._color_window = None
            self.open_color_menu()

    def apply_color(self):
        '''Applies newly chosen colors by destroying and remaking the main window'''
        self.write_colors()
        self._color_window = None
        self.update_mem_from_gui()
        self._root.destroy()
        self._root.quit()
        self.make_window()
        for loc in self._gui_memory:
            print(loc)
        self.update_gui_from_mem()

    def read_colors(self):
        '''Reads colors.json for color settings if it exists. Creates a new
        colors.json if not.'''
        if Path("colors.json").is_file():
            with open("colors.json", 'r', encoding="utf-8") as file:
                self._colors = json.load(file)
        else:
            self.write_colors()

    def write_colors(self):
        '''Write custom color settings into colors.json. Creates the file if it
        doesn't exist already'''
        with open("colors.json", 'w', encoding="utf-8") as file:
            json.dump(self._colors, file)


def make_new_window():
    new_window = GUI()
    new_window.make_window()


def main():
    """For testing purposes only."""
    # # Prints 1234 when run
    # memory = [1102, 4300, 1234]
    # machine = Machine(memory)
    gui = GUI()
    gui.make_window()


if __name__ == "__main__":
    main()
