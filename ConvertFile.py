#main for command line utility to convert 4 number word file format to 6 number word file format.
from sys import argv
from parse import parse

def reformat(memory_list):
    #list_of_commands = [10, 11, 20, 21, 30, 31, 32, 33, 40, 41, 42, 43]
    j = 0
    for count, i in enumerate(memory_list):
        #print(count)
        if len(str(i)) == 4:
            #ordinary old format word
            i = str(i)
            i = i[:3] + "0" + i[3:]
            i = int(i)
            memory_list[count] = i
        else:
            pass
    return memory_list
            
def main():

    memory_list = parse(argv[1])
    
    if len(argv) == 3:
        #2 files names given
        pass
    elif len(argv) == 2:
        #1 file name given
        reformatted_mem_list = reformat(memory_list)
        with open(argv[1], "w") as given_file:
            for i in reformatted_mem_list:
                if i is not 0:
                    given_file.write("+0" + str(i) + "\n")
                else:
                    given_file.write("+" + str(i) + "\n")
    else:
        print("Error: No file name given.")

if __name__ == "__main__":
    main()