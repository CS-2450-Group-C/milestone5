'''Module containing the parse function'''

import re
from pathlib import Path

from memory import Memory

class Parser:
    """Contains operations for parsing text from an input file 
    into a list and returning that list"""
    def __init__(self, word_size = 6):
        """Constructor for Parser, accepts 1 parameter:
        1. word_size: integer that determines how long parsed words will be"""
        # Word size can be altered
        self._word_size = word_size

    def get_word_size(self):
        """Returns the word size the parser will use"""
        return self._word_size

    def validate_file_name(self, file_name):
        """Checks the local directory to determine if the input
        filename is valid"""
        if not Path(file_name).is_file():
            raise ValueError("File not found")

    def parse(self, file_name):
        """Given a BasicML file, returns list of 100 ints representing memory locations."""
        # Validate given file
        self.validate_file_name(file_name)

        # List that will be returned
        # TODO: May need to update this depending on how memory is implemented
        memory = Memory()

        # Open the file
        with open(file_name, 'r', encoding='UTF-8') as reader:
            lines = reader.readlines()
            # Read file line by line
            for i, line in enumerate(lines):
                regex = re.search("^\s*((\+|-|)(\d+)|)\s*$", line)
                # Valid Input
                if regex:
                    # Fill memory (empty lines and oversized ints default to 0)
                    if regex.group(1) != "" and len(regex.group(3)) <= self.get_word_size():
                        memory[i] = int(regex.group(1))
                # Invalid Input
                else:
                    raise ValueError("Invalid word at line " + str(i + 1))
        
        return memory


def main():
    """For testing purposes only."""
    # Initialize parser object
    parser = Parser()
    
    # Test file 1
    try:
        memory = parser.parse("ParserTest1.txt")
        for word in memory:
            print(word)
    except ValueError as ex:
        print(ex)

    # Test file 2
    try:
        memory = parser.parse("ParserTest2.txt")
        for word in memory:
            print(word)
    except ValueError as ex:
        print(ex)

    # Test file 3
    try:
        memory = parser.parse("NonexistentFile.txt")
        for word in memory:
            print(word)
    except ValueError as ex:
        print(ex)


if __name__ == "__main__":
    main()
