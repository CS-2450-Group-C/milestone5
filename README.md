# UVSim User Guide

- [What is it?](#what-is-it)
- [Required Libraries](#required-libraries)
- [Available Operations](#available-operations)
- [How to use](#how-to-use)
- [Accepted 4-digit Word Formats](#accepted-4-digit-word-formats)

## What is it?
The UVSim is a virtual machine that can interpret the machine language BasicML. It has a CPU, an accumulator, and main memory. The accumulator is register that can hold information to be opperated on. The main memory stores 100 instances of a 4-digit integer called a word. A word can either be a value or an instruction. Available instructions are listed below.

## Required Libraries
UVSim uses Pyperclip in order to facilitate copying memory entries to the user's clipboard. UVSim also uses Pytest for unit testing. These libraries can be installed using "pip install pyperclip" and "pip install pytest", respectively.

## Available Operations
A 4-digit word can be an instruction. The two rightmost digits indicate the specific operation. The two leftmost digits indicate a memory address (0-99).
### I/O Operations
* READ = 10 Read a word from the keyboard into a specific location in memory.
* WRITE = 11 Write a word from a specific location in memory to screen.

### Load/store Operations
* LOAD = 20 Load a word from a specific location in memory into the accumulator.
* STORE = 21 Store a word from the accumulator into a specific location in memory.

### Arithmetic Operations
* ADD = 30 Add a word from a specific location in memory to the word in the accumulator (leave the result in the accumulator)
* SUBTRACT = 31 Subtract a word from a specific location in memory from the word in the accumulator (leave the result in the accumulator)
* DIVIDE = 32 Divide the word in the accumulator by a word from a specific location in memory (leave the result in the accumulator).
* MULTIPLY = 33 multiply a word from a specific location in memory to the word in the accumulator (leave the result in the accumulator).

### Control Operations
* BRANCH = 40 Branch to a specific location in memory
* BRANCHNEG = 41 Branch to a specific location in memory if the accumulator is negative.
* BRANCHZERO = 42 Branch to a specific location in memory if the accumulator is zero.
* HALT = 43 Pause the program

## How to use
### Command-line interface (CLI)
The UVSim can load 4-digit words from a `.txt` file into memory, starting at address 00. Ensure all files are downloaded into the same directory. From that directory, call `python3 main.py fileName.txt`

### Graphical user interface (GUI)
Start the UVSim GUI by running `python3 main.py` without any arguments.

To import a program to run, click on the __import__ button. The UVSim can load 4-digit words from a `.txt` file into memory, starting at address 00.

To start the program, click __run__. The table on the left of the interface shows the current memory of the machine and will update as the machine runs if the program modifies the memory. The large output box on the bottom of the interface logs the output of UVSim and can be a useful resource for debugging a non-working program.

When the running program expects an input, it will say so in the output box and will pause execution until a valid 4-digit number is entered into the input box and the __enter__ button is clicked.

The program will run until it completes.

## GUI Interface
This section contains instructions on how to use various parts of the UVSim GUI.
* The Import button - This button allows the user to import a file containing BasicML instructions. To import a file into UVSim, click the Import button, and select a file containing your BasicML files.
* The Run button - This button runs the BasicML program that is currently in the memory editor. To run a program, click the run button.
* The Color button - This button opens a menu that allows the user to speciify the main and accent colors of the UVSim. To change the colors, click on the Color button. To change the main color, click on the Change Main Color button, a color chooser window will appear, select the desired main color and click ok. To change the accent color, click on the Change Accent Color button, a color chooser window will appear, select the desired accent color and click ok. To change to colors of the UVSim back to the default UVU colors, then click Restore Default Colors. To apply the color changes that have been made, click the Apply button.
* The Clear button - This button clears the output text box so that it only shows the default welcome message. To clear the output text box, click the Clear button.
* The Save As button - This button allows the user to save the current contents of the memory as a .txt file. To save the contents of the memory as a .txt file, click the Save As button, a file dialog will appear, navigate to the desired folder that will contain the file, type in the desired file name, and click "Save"
* The Save button - This button allows the user to save the current contents of the memory to the file that is currently open in UVSim. A file is opened in UVSim when the user imports a file using the Import button, or when a user creates a new file using the Save As button. To save the contents of the memory, click the Save button.

Users can modify the contents of BasicML programs using the UVSim's GUI memory editor. Users can use the Import button to import a file, or they can start from scratch using the Memory section on the right side of the window. Users can add, modify, and delete commands through the GUI. Changes to individual lines of the program can be made by clicking an entry and using the keyboard. Individual words can be modified and deleted, they can be copied by selecting the word and pressing Ctrl+C, they can be cut with Ctrl-X, and they can be pasted using Ctrl-V. However, this method only works with one individual word at a time, to paste, copy, or cut an entire program, use the buttons that have their details listed below:
* The Paste button - This button allows the user to paste a string into the UVSim memory editor. To do this, a user must have a program copied to their clipboard. This program must contain valid instructions seperated by newlines. For example: 
"+1007
+1008
+2007
+2008
+2109
+1109
+4300" Where instructions such as "+1007" and "+1008" are seperated by a newline. Once this program is copied to the user's clipboard, the user must paste this program into the "Paste:" entry in the Memory section of the window. Once this has been done, click the Paste button and the program that is in the "Paste:" entry will be parsed and pasted into the GUI memory editor.
* The Copy button - This button allows the user to copy the contents of the Memory editor to their clipboard. To copy the memory to clipboard, click on the Copy button.
* The Cut button - This button allows the user to cut the contents of the memory editor to their clipboard, once cut, the user will have the contents of the memory on their clipboard and every index of memory in the editor will contain the word "+0000" To cut the memory, click on the Cut button.

## Accepted 4-digit Word Formats
<pre>+0123
-0123
0123
123         (Adds leading zero 0123)
12          (Adds leading zeros 0012)
1           (Adds leading zeros 0001)
            (blank lines default to 0000)
-99999      (Oversized words default to 0000)  </pre>
