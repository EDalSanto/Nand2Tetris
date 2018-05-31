# Input1: text file named SomeProgram.asm containing Hack assembly program
# Input2: name of output file of SomeProgram.asm containing Hack assembly program
# Output: text file name SomeProgram.hack containing translated Hack Machine Code

# Assembler Without Symbols
# main
  # for each line in input file
    # pass instruction to Parser
      # Parse Module -> tokenize instruction components */
        # note: ignore whitespaces and comments
        # define helper functions which diagnose instruction
        # main function logic */
        # initialize binary string that will be written to output file
        # if A command
        #   add starting 0 for A command
        #   set binary output string to decimal convert to binary
        # else C command
        #   Code Module */
        #     define structs
        #       dest
        #       comp
        #         note: multiple keys with same value
        #       jump
        #   add starting 1 for C command
        #   pass comp token to a-bit / comp-bits translator; add to binary output
        #   pass dest-bits to translator; add to binary output
        #   pass jump-bits to translator; add to binary output
        # write binary string to output file

#!/usr/local/bin/python
import sys

class Parser():
    def __init__(self, input_file):
        self.input_file = input_file

    def parse_file(self):
        output_file = open('./add/Add.hack', 'w+')

        for line in self.input_file:
            # strip new line
            line = line.rstrip('\n')
            # skip if comment or empty line
            if line == '' or line[0] == '/':
                continue
            # if A command
            if line[0] == '@':
                num_converted_to_binary_string = '{0:015}'.format(line[1::-1])
                print(num_converted_to_binary_string)
                output_file.write(num_converted_to_binary_string)

            print(line)


def main(input_file):
    with open(input_file) as f:
        parser = Parser(f)
        output_file = parser.parse_file()

    return output_file


main(sys.argv[1])
