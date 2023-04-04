import re

class Input:
    def __init__(self):
        "Constructor for Input. Creates two attributes, _validity and _default_message"
        self._validity = False
        self._default_message = "Type input: "


    def get_validity(self):
        """Getter for the _validity attribute"""
        return self._validity


    def set_validity(self, validity):
        """Setter for the _validity attribute"""
        self._validity = validity

    
    def validate_input(self, input):
        """Uses a RegEx to check if an input is a valid word"""
        
        regex = re.search("^\s*((\+|-|)(\d{1,6}))\s*$", input)
        # Valid Input
        if regex:
            self.set_validity(True)
        # Invalid input
        else:
            self.set_validity(False)
        

    def check_exit(self, input):
        """Checks if the user wants to quit
        the input, returns a Bool"""
        if input.lower() == "exit":
            return True

        return False
            
    # Note: currently used only for command line input.
    def get_input(self):
        """Method for getting input from the user. Validates
        the input then returns a string"""
        new_word = ""

        # Ask the user for input until their input is valid
        while not self.get_validity():
            new_word = input(self._default_message)
            
            # Check if the user wants to quit
            if self.check_exit(new_word):
                return None
            
            # Ensure the input is a valid word
            self.validate_input(new_word)

            # Ask the user for valid input again
            if not self.get_validity():
                print("Error: Input must be a 4-digit number. Please try again.")

        return new_word

def main():
    """For testing purposes only."""
    ip = Input()
    word = ip.get_input()
    print(word)

if __name__ == "__main__":
    main()
