import sys
import re

class VMTranslator():
    """
    Takes an input file in Hack VM code and translate to Hack Assembly
    """
    @classmethod
    def run(cls, input_file):
        parser = VMParser(input_file)
        writer = VMToHackCodeWriter(input_file)

        while parser.has_more_commands:
            parser.advance()
            if parser.valid_current_command():
                writer.translate(parser.current_command, parser.current_command_type)


class VMCommand():
    def __init__(self, text):
        self.text = self._strip(text)

    def type(self):
        if self.text == '':


    def empty(self):
        return self.text == ''

    def _strip(self):
        # remove leading and trailing whitespace
        text = text.strip()
        # remove comments
        text = text.split('//')[0]
        # strip again in case space after, i.e., D=M+1 // comments
        text = text.strip(' ')

        return text



class VMParser():
    """
    Encapsulates access to the input code in the file
    Reads VM commands, parses them and provides a convenient access to their components
    Ignores Whitespace and Comments
    """
    def __init__(self, input_file):
        self.input_file = open(input_file, 'r')
        self.has_more_commands = True
        self.current_command = None
        self.next_command = None

    def advance(self):
        self._update_current_command()
        self._update_next_command()
        self._update_has_more_commands()

    def _update_has_more_commands(self):
        if self._next_command.empty():
            self.has_more_commands = False

    def _update_next_command(self):
        command = self.input_file.readline()
        self.next_command = self._strip_command(command)

    def _update_current_command(self):
        if self.current_command == None:
            command = self.input_file.readline()
            self.current_command = self._strip_command(command)
        else:
            self.current_command = self.next_command



class VMToHackCodeWriter():
    def __init__(self, output_file):
        self.output_file = open(self._output_file_name_from(input_file), 'w')

    def _output_file_name_from(self, input_file):
        return input_file.name.split('.')[0] + '.asm'


if __name__ == "__main__" and len(sys.argv) == 2:
    vm_code_file = sys.argv[1]
    asm_code = VMTranslator().run(vm_code_file)
    print(asm_code)
