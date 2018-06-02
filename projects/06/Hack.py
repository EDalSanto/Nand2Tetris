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
        #     define hash table
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

class HackAssembler():
    """
    Specific to Hack Computer in Nand2Tetris course

    Input: ASM file with assembly language instructions
    Output: input converted to machine code output
    """

    def __init__(self, input_file):
        self.parser = HackAssemblerParser(input_file)
        self.translator = HackAssemblerTranslator()

    def run(self):
        hack_file_name = self.parser.input_file.name.split('.')[0] + '.hack'
        hack_file = open(hack_file_name, 'w+')

        while self.parser.has_more_commands():
            self.parser.advance()
            translated_command = ''

            # comments and white space will be ignored
            if self.parser.command_type_is('a_command'):
                num = int(self.parser.symbol())
                print('num: {}'.format(num))
                num_converted_to_binary_string = '{0:016b}'.format(num)
                translated_command = num_converted_to_binary_string + '\n'
            elif self.parser.command_type_is('l_command'):
                continue
            elif self.parser.command_type_is('c_command'):
                continue

            print('translated: {}'.format(translated_command))
            hack_file.write(translated_command)

        hack_file.close()


class HackAssemblerTranslator():
    @classmethod
    def dest_bits(cls, mnemonic):
        print('dest')


class HackAssemblerParser():
    """
    Reads each line in the input file one a time and reports on state of current line
    """
    def __init__(self, input_file):
        self.input_file = open(input_file, 'r')
        self.current_line = None
        self.next_line = None

    def symbol(self):
        """
        remove symbols for A or Commands + trailing comments
        """
        return ''.join(c for c in self.current_line if c not in '()@/')

    def has_more_commands(self):
        # if empty line, would at least return \n
        return self.next_line != ''

    def advance(self):
        """
        get next line as well so we know if there are more lines after the current
        """
        if self.current_line == None:
            self.current_line = self.input_file.readline()
        else:
            self.current_line = self.next_line

        self.next_line = self.input_file.readline()

    def command_type_is(self, possible_command_type):
        return possible_command_type == self.command_type()

    def command_type(self):
        """
        assumes valid input
        """
        first_char = self.current_line[0]

        # ignore white space and comments
        if first_char == '/' or first_char == '\n':
            return 'comment_or_empty_line'
        elif first_char == '@':
            return 'a_command'
        elif first_char == '(':
            return 'l_command'
        else:
            return 'c_command'


asm_input_file = sys.argv[1]
assembler = HackAssembler(asm_input_file)
assembler.run()
