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
    ARITHMETIC_TRANSLATIONS = {
        'add': [ '@SP', 'AM=M-1', 'D=M', '@SP', 'AM=M-1', 'M=M+D', '@SP', 'M=M+1' ],
        'sub': [ '@SP', 'AM=M-1', 'D=M', '@SP', 'AM=M-1', 'M=M-D', '@SP', 'M=M+1' ],
        'neg': [ '@SP', 'A=M-1', 'M=-M' ],
        'or' : [ '@SP', 'AM=M-1', 'D=M', '@SP', 'AM=M-1', 'M=M|D', '@SP', 'M=M+1' ],
        'not': [ '@SP', 'AM=M-1', 'D=M', 'M=!M', '@SP', 'M=M+1'],
        'and': [ '@SP', 'AM=M-1', 'D=M', '@SP', 'AM=M-1', 'M=M&D', '@SP', 'M=M+1']
    }

    def __init__(self):
        self.eq_counter = 0
        self.lt_counter = 0
        self.gt_counter = 0

    def translate(self, command):
        if command.text in self.ARITHMETIC_TRANSLATIONS:
            return self.ARITHMETIC_TRANSLATIONS[command.text]
        elif command.text == 'eq':
            self.eq_counter += 1
            return [
                '@SP',
                'AM=M-1',
                'D=M',
                '@SP',
                'AM=M-1',
                'D=M-D', # diff x - y
                '@NOT_EQ{}'.format(self.eq_counter),
                'D;JNE', # if diff not equal jump to 0 otherwise will execute equal
                '@SP',
                'A=M',
                'M=-1',
                '@INC_STACK_POINTER_EQ{}'.format(self.eq_counter),
                '0;JMP', # skip not_equal that we executed equal above
                '(NOT_EQ{})'.format(self.eq_counter),
                '@SP',
                'A=M',
                'M=0',
                '(INC_STACK_POINTER_EQ{})'.format(self.eq_counter),
                '@SP',
                'M=M+1' # increment stack pointer
            ]
        elif command.text == 'lt':
            self.lt_counter += 1
            return [
                '@SP',
                'AM=M-1',
                'D=M',
                '@SP',
                'AM=M-1',
                'D=M-D',
                '@NOT_LT{}'.format(self.lt_counter),
                'D;JGE',
                '@SP',
                'A=M',
                'M=-1',
                '@INC_STACK_POINTER_LT{}'.format(self.lt_counter),
                '0;JMP',
                '(NOT_LT{})'.format(self.lt_counter),
                '@SP',
                'A=M',
                'M=0',
                '(INC_STACK_POINTER_LT{})'.format(self.lt_counter),
                '@SP',
                'M=M+1'
            ]
        elif command.text == 'gt':
            self.gt_counter += 1
            return [
                '@SP',
                'AM=M-1',
                'D=M',
                '@SP',
                'AM=M-1',
                'D=M-D',
                '@NOT_GT{}'.format(self.gt_counter),
                'D;JLE',
                '@SP',
                'A=M',
                'M=-1',
                '@INC_STACK_POINTER_GT{}'.format(self.gt_counter),
                '0;JMP',
                '(NOT_GT{})'.format(self.gt_counter),
                '@SP',
                'A=M',
                'M=0',
                '(INC_STACK_POINTER_GT{})'.format(self.gt_counter),
                '@SP',
                'M=M+1'
            ]
        else: #elif command.is_push_or_pop_type():
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
        translation = []

        if parser.has_valid_current_command():
            translation = translator.translate(parser.current_command)

            for line in translation:
                writer.write(line + '\n')

    writer.close_file()
