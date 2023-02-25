# UVSim User Guide

- [What is it?](#what-is-it)
- [Available Operations](#available-operations)
- [How to use](#how-to-use)
- [Accepted 4-digit Word Formats](#accepted-4-digit-word-formats)

## What is it?
The UVSim is a virtual machine that can interpret the machine language BasicML. It has a CPU, an accumulator, and main memory. The accumulator is register that can hold information to be opperated on. The main memory stores 100 instances of a 4-digit integer called a word. A word can either be a value or an instruction. Available instructions are listed below.

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

## Accepted 4-digit Word Formats
<pre>+0123
-0123
0123
123         (Adds leading zero 0123)
12          (Adds leading zeros 0012)
1           (Adds leading zeros 0001)
            (blank lines default to 0000)
-99999      (Oversized words default to 0000)  </pre>
