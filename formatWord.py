
def format_word(word):
    """Convert int to a string with format (+/-)1234"""
    if isinstance(word, str):
        word = int(word)
    output = str(abs(word))

    # Pad the number with zeroes until there are four digits
    output = output.rjust(4, "0")

    # Add a positive or negative symbol depending upon the number
    if word < 0:
        output = "-" + output
    else:
        output = "+" + output
    return output