'''Module containing the parse function'''

import re
from pathlib import Path

def parse(file_name):
    """Given a BasicML file, returns list of 100 ints representing memory locations."""
    WORD_SIZE = 6
    MEMORY_SIZE = 100
    # Validate given file
    if not Path(file_name).is_file():
        raise ValueError("File not found")

    memory = [0] * MEMORY_SIZE
    with open(file_name, 'r', encoding='UTF-8') as reader:
        lines = reader.readlines()
        # Read file line by line
        for i, line in enumerate(lines):
            regex = re.search("^\s*((\+|-|)(\d+)|)\s*$", line)
            # Valid Input
            if regex:
                # Fill memory (empty lines and oversized ints default to 0)
                if regex.group(1) != "" and len(regex.group(3)) <= WORD_SIZE:
                    memory[i] = int(regex.group(1))
            # Invalid Input
            else:
                raise ValueError("Invalid word at line " + str(i + 1))
    return memory


def main():
    """For testing purposes only."""
    # Test file 1
    try:
        memory = parse("ParserTest1.txt")
        for word in memory:
            print(word)
    except ValueError as ex:
        print(ex)

    # Test file 2
    try:
        memory = parse("ParserTest2.txt")
        for word in memory:
            print(word)
    except ValueError as ex:
        print(ex)

    # Test file 3
    try:
        memory = parse("NonexistentFile.txt")
        for word in memory:
            print(word)
    except ValueError as ex:
        print(ex)


if __name__ == "__main__":
    main()
