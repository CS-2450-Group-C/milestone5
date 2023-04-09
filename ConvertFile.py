#command line utility to convert 4 number word file format to 6 number word file format.
from sys import argv
from Parser import Parser

def reformat(memory_list):
    list_of_commands = [10, 11, 20, 21, 30, 31, 32, 33, 40, 41, 42, 43]
    for count, i in enumerate(memory_list):
        if len(str(i)) == 4 and int(str(i)[:2]) in list_of_commands:
            #if is ordinary old format word
            i = str(i)
            i = i[:2] + "0" + i[2:]
            i = int(i)
            memory_list[count] = i
        else:
            pass
    return memory_list

def write_file(mem_list_param, argv_num):
    with open(argv[argv_num], "w") as given_file:
            for i in mem_list_param:
                if i == -99999:
                    given_file.write("-99999")
                    break
                elif i != 0:
                    given_file.write("+0" + str(i) + "\n")
                else:
                    # i == 0
                    given_file.write("+000000" + "\n")
            
def main():
    parser_obj = Parser()
    memory_list = parser_obj.parse(argv[1])
    reformatted_mem_list = reformat(memory_list)
    if len(argv) == 3:
        #2 files names given
        write_file(reformatted_mem_list, 2)
        print("File saved with new format")
    elif len(argv) == 2:
        #1 file name given
        write_file(reformatted_mem_list, 1)
        print("File converted to new format")
    else:
        print("Error: No file name given.")

if __name__ == "__main__":
    main()
