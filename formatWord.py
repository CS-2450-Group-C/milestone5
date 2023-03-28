
def format_word(word):
    """Convert int to a string with format (+/-)1234"""
    if isinstance(word, str):
        word = int(word)
    output = str(abs(word))

    # Pad the number with zeroes until there are four digits
    output = output.rjust(6, "0")

    # Add a positive or negative symbol depending upon the number
    if word < 0:
        output = "-" + output
    else:
        output = "+" + output
    return output

def main():
    """For testing purposes only."""
    print(format_word("+123"))
    print(format_word("123"))
    print(format_word("+123456"))
    print(format_word("012300"))
    print(format_word("+012300"))
    print(format_word("-012300"))

if __name__ == "__main__":
    main()