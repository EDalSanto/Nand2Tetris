import sys
import re

class VMTranslator():
    """
    Takes an input file in Hack VM code and translate to Hack Assembly
    """
    def run(self, input_file_name):
        input_file = open(input_file_name, 'r')
        parser = VMParser(input_file)

        output_file_name = input_file.name.split('.')[0] + '.asm'
        output_file = open(output_file_name, 'w')
        writer = VMToHackCodeWriter(output_file)

        while parser.has_more_lines_to_parse:
            # advance
            # if not valid command
                # continue
            # else
                # translate
                # write


class VMParser():
    """
    Encapsulates access to the input code in the file
    Reads VM commands, parses them and provides a convenient access to their components
    Ignores Whitespace and Comments
    """
    def __init__(self, input_file):
        self.input_file = input_file


class VMToHackCodeWriter():
    def __init__(self, output_file):
        self.output_file = output_file


vm_code_file = sys.argv[1]
vm_translator = VMTranslator()
asm_code = vm_translator.translate()
