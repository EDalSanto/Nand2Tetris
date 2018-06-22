import sys
import re

class VMCommand():
    """
    provides simpler interface and encapsulation for inspecting current command
    """
    COMMENT_SYMBOL = '//'
    NEWLINE_SYMBOL = '\n'
    EMPTY_SYMBOL = ''

    def __init__(self, text):
        self.text = text.strip()
        self.raw_text = text

    def is_comment(self):
        return self.raw_text[0:2] == self.COMMENT_SYMBOL

    def is_whitespace(self):
        return self.raw_text == self.NEWLINE_SYMBOL

    def is_empty(self):
        return self.raw_text == self.EMPTY_SYMBOL

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

    def has_valid_current_command(self):
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

class VMWriter():
    def __init__(self, input_file):
        self.output_file = open(self._output_file_name_from(input_file), 'w')

    def write(self, command):
        self.output_file.write(command)

    def close_file(self):
        self.output_file.close()

    def _output_file_name_from(self, input_file):
        return input_file.split('.')[0] + '.asm'

class VMTranslator():
    ARITHMETIC_AND_LOGICAL_TRANSLATIONS = {
        'add': [ '@SP', 'AM=M-1', 'D=M', 'A=A-1', 'M=M+D' ],
        'sub': [ '@SP', 'AM=M-1', 'D=M', 'A=A-1', 'M=M-D' ]
        'neg': [ '@SP', 'A=M-1', 'M=-M' ]
        'eq' : [
            '(EQUAL)',
              '@SP',
              'M=-1',
              '@OUT',
              '0;JMP' # how to jump back to previous executing line?
            '@SP',
            'AM=M-1',
            'D=M', # y
            'A=A-1',
            'D=M-D', # y - x -> diff result stored in D
            '@EQUAL',
            'D;JEQ',
            '@SP',
            'M=0',
            '(OUT)'


        ],
        'lt': [

        ],
        'gt': [

        ],
    }
    def translate(self, command):
        if command.text in self.ARITHMETIC_AND_LOGICAL_TRANSLATIONS:
            return self.ARITHMETIC_AND_LOGICAL_TRANSLATIONS[command.text]
        #else if command.is_push_or_pop_type():
        else:
            op, segment, index = command.text.split(' ')
            if op == 'push':
                to_load = '@{}'.format(index).strip()
                # add the index to the top of the segment
                return [ to_load, 'D=A', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1' ]


if __name__ == "__main__" and len(sys.argv) == 2:
    vm_code_file = sys.argv[1]

    parser = VMParser(vm_code_file)
    writer = VMWriter(vm_code_file)
    translator = VMTranslator()

    while parser.has_more_commands:
        parser.advance()
        output = []

        if parser.has_valid_current_command():
            #print(parser.current_command.stripped())
            output = translator.translate(parser.current_command)
            #if parser.current_command.text == 'add':
            #    output = ArithmeticTranslator.TRANSLATIONS['add']
            #elif parser.current_command.text.split(' ')[0] == 'push':
            #    output = PushPopTranslator.translate(parser.current_command.text)
            for line in output:
                writer.write(line + '\n')

    writer.close_file()
