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
                #print(parser.current_command.stripped())
                writer.translate(parser.current_command)

class VMCommand():
    """
    provides simpler interface and encapsulation for inspecting current command
    """
    COMMENT_SYMBOL = '//'
    NEWLINE_SYMBOL = '\n'
    EMPTY_SYMBOL = ''

    def __init__(self, text):
        self.text = text

    def stripped(self):
        return self.text.strip()

    def is_comment(self):
        return self.text[0:2] == self.COMMENT_SYMBOL

    def is_whitespace(self):
        return self.text == self.NEWLINE_SYMBOL

    def is_empty(self):
        return self.text == self.EMPTY_SYMBOL

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

    def valid_current_command(self):
        return not self.current_command.is_whitespace() and not self.current_command.is_comment()

    def advance(self):
        self._update_current_command()
        self._update_next_command()
        self._update_has_more_commands()

    def _update_has_more_commands(self):
        if self.next_command.is_empty():
            self.has_more_commands = False

    def _update_next_command(self):
        text = self.input_file.readline()
        self.next_command = VMCommand(text)

    def _update_current_command(self):
        # initialization
        if self.current_command == None:
            text = self.input_file.readline()
            self.current_command = VMCommand(text)
        else:
            self.current_command = self.next_command


class VMToHackCodeWriter():
    def __init__(self, input_file):
        self.output_file = open(self._output_file_name_from(input_file), 'w')

    def _output_file_name_from(self, input_file):
        return input_file.split('.')[0] + '.asm'


if __name__ == "__main__" and len(sys.argv) == 2:
    vm_code_file = sys.argv[1]
    asm_code_file = VMTranslator().run(vm_code_file)
