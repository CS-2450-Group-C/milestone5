# UVSim User Guide

- [What is it?](#what-is-it)
- [Required Libraries](#required-libraries)
- [Available Operations](#available-operations)
- [How to use](#how-to-use)
- [GUI Interface](#gui-interface)
- [Accepted 6-digit Word Formats](#accepted-6-digit-word-formats)
- [Program input](#program-input)

## What is it?
The UVSim is a virtual machine that can interpret the machine language BasicML. It has a CPU, an accumulator, and main memory. The accumulator is register that can hold information to be opperated on. The main memory stores 250 instances of a 6-digit integer called a word. A word can either be a value or an instruction. Available instructions are listed below.

## Required Libraries
UVSim uses Pyperclip in order to facilitate copying memory entries to the user's clipboard. UVSim also uses Pytest for unit testing. These libraries can be installed using "pip install pyperclip" and "pip install pytest", respectively.

## Available Operations
A 6-digit word can be an instruction. The three rightmost digits indicate the specific operation. The three leftmost digits indicate a memory address (0-249).
### I/O Operations
* READ = 010 Read a word from the keyboard into a specific location in memory.
* WRITE = 011 Write a word from a specific location in memory to screen.

### Load/store Operations
* LOAD = 020 Load a word from a specific location in memory into the accumulator.
* STORE = 021 Store a word from the accumulator into a specific location in memory.

### Arithmetic Operations
* ADD = 030 Add a word from a specific location in memory to the word in the accumulator (leave the result in the accumulator)
* SUBTRACT = 031 Subtract a word from a specific location in memory from the word in the accumulator (leave the result in the accumulator)
* DIVIDE = 032 Divide the word in the accumulator by a word from a specific location in memory (leave the result in the accumulator).
* MULTIPLY = 033 multiply a word from a specific location in memory to the word in the accumulator (leave the result in the accumulator).

### Control Operations
* BRANCH = 040 Branch to a specific location in memory
* BRANCHNEG = 041 Branch to a specific location in memory if the accumulator is negative.
* BRANCHZERO = 042 Branch to a specific location in memory if the accumulator is zero.
* HALT = 043 Pause the program

## How to use
### Command-line interface (CLI)
The UVSim can load 6-digit words from a `.txt` file into memory, starting at address 000. Ensure all files are downloaded into the same directory. From that directory, call `python3 main.py fileName.txt`

### Graphical user interface (GUI)
Start the UVSim GUI by running `python3 main.py` without any arguments.

To import a program to run, click on the __import__ button. The UVSim can load 6-digit words from a `.txt` file into memory, starting at address 000.

To start the program, click __run__. The table on the right of the interface shows the current memory of the machine and will update as the machine runs if the program modifies the memory. The large output box on the bottom of the interface logs the output of UVSim and can be a useful resource for debugging a non-working program.

When the running program expects an input, it will say so in the output box and will pause execution until a valid 6-digit number is entered into the input box and the __enter__ button is clicked.

The program will run until it completes.

Read more about interacting with the GUI in [GUI Interface](#gui-interface).

## GUI Interface
This section contains instructions on how to use various parts of the UVSim GUI.
* The __Import__ button - This button allows the user to import a file containing BasicML instructions. To import a file into UVSim, click the Import button, and select a file containing your BasicML program.
* The __Run__ button - This button runs the BasicML program that is currently in the memory editor. To run a program, click the run button.
* The __Color__ button - This button opens a menu that allows the user to speciify the main and accent colors of the UVSim GUI. To change the colors, click on the __Color__ button. To change the main color, click on the __Change Main Color__ button. A color chooser window will appear. Select the desired main color and click __ok__. To change the accent color, click on the __Change Accent Color__ button. A color chooser window will appear. Select the desired accent color and click __ok__. To change to colors of the UVSim back to the default UVU colors, click __Restore Default Colors__. To apply the color changes that have been made, click the __Apply__ button.
* The __New Window__ button - This button creates a new UVSim window so that more than one program can be opened and edited at the same time. To create a new window, click the __New Window__ button.
* The __Clear__ button - This button clears the output text box so that it only shows the default welcome message. To clear the output text box, click the __Clear__ button.
* The __Save As__ button - This button allows the user to save the current contents of the memory as a `.txt` file. To save the contents of the memory as a `.txt` file, click the __Save As__ button. Your system's file dialog will appear. Navigate to the desired folder that will contain the file, type in the desired file name, and click __Save__.
* The __Save__ button - This button allows the user to save the current contents of the memory to the currently active file in UVSim if there is one. A file is opened in UVSim when the user imports a file using the __Import__ button, or when a user creates a new file using the __Save As__ button. To save the contents of the memory, click the __Save__ button. If there is not a currently active file, __Save__ has the same behavior as __Save As__.

### Memory editor
Users can modify the contents of BasicML programs using the UVSim's GUI memory editor. Users can use the __Import__ button to import a file, or they can start from scratch using the Memory viewer on the right side of the window. Users can add, modify, and delete words through this interface. Changes to individual lines of the program can be made by clicking the entry box at the desired memory location and manually typing in the word. Individual words can be copied by selecting the word and pressing Ctrl+C, they can be cut with Ctrl-X, and they can be pasted using Ctrl-V. To paste, copy, or cut multiple lines of the program at once, use the __Paste__, __Copy__, and __Cut__ buttons located directly beneath the memory viewer:
* The __Paste__ button - This button allows the user to paste code that was copied through the Copy or Cut dialogues. To paste multiple lines into memory, click the __Paste__ button which will open the Paste dialogue. Enter the starting memory location of where the code needs to be pasted into the __Paste Index__ box and click the __Paste__ button from within the dialogue. Paste will overwrite as many lines in the program as were copied or cut.
* The __Copy__ button - This button will open the Copy dialogue. To copy a section of code, enter the starting memory address of the code that needs to be copied in the __Copy Start Index__ box, enter the desired ending memory address (inclusive) into the __Copy End Index__ box, and click the __Copy__ button from within the dialogue. The copied section can now be pasted elsewhere in the program using the __Paste__ button.
* The __Cut__ button - This button will open the Cut dialogue. To cut a section of code, enter the starting memory address of the code that needs to be cut in the __Cut Start Index__ box, enter the desired ending memory address (inclusive) into the __Cut End Index__ box, and click the __Cut__ button from within the dialogue. The cut section can now be pasted elsewhere in the program using the __Paste__ button. All of the memory locations that were cut will be replaced with the word "+000000".

## Accepted 6-digit Word Formats
```
+0123456
-0123456
0123456
12345       (Adds leading zero 012345)
1234        (Adds leading zeros 001234)
123         (Adds leading zeros 000123)
12          (Adds leading zeros 000012)
1           (Adds leading zeros 000001)
            (blank lines default to 000000)
-9999999    (Oversized words default to 000000)
```
## Program Input
If a program that contains a user input instruction is run, the user can use the GUI to provide the input. To do so, run the said program using the Run button. When the program gets to the user input instruction, then a message will appear in the output text box stating that the program is waiting for input, to provide the input, type it into the Input textbox and click the Enter button.
