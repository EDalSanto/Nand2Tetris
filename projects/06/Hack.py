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
        output_file = open('input_file name converted to .hack', 'w+')

        with open(self.input_file) as asm_instructions:
            for instruction in asm_instructions:
                parsed_instruction = parser.parsed_instruction_for(instruction)
                if parsed_instruction == "not valid asm instruction":
                    continue
                translated_instruction = translator.translate_instruction(parsed_instruction)
                output_file.write(translated_instruction)


class HackAssemblerTranslator():
    def translated_line_for(self, instruction):


class HackAssemblerParser():
    """
    Reads each line in the input file
    """
    def __init__(self, input_file):
        self.input_file = input_file
        self.current_line = None

    def instruction_type(self, instruction):
        # strip new line
        instruction = instruction.rstrip('\n')
        # skip if comment or empty line
        if instruction == '' or instruction[0] == '/':
            return "comment or empty line"
        # if A command
        if line[0] == '@':
            return "A"
            Assembler.translate_to_machine_code(line[1:], type='A')
            num_converted_to_binary_string = '{0:016b}'.format(int(line[1:]))
            output_file.write(num_converted_to_binary_string + '\n')
        else: # C command
            return "C"


asm_input_file = sys.argv[1]
assembler = HackAssembler(asm_input_file)
assembler.run()
