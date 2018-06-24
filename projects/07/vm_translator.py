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
        self.raw_text = text
        self.text = text.strip()
        self.parts = text.strip().split(' ')

    def is_comment(self):
        return self.raw_text[0:2] == self.COMMENT_SYMBOL

    def is_whitespace(self):
        return self.raw_text == self.NEWLINE_SYMBOL

    def is_empty(self):
        return self.raw_text == self.EMPTY_SYMBOL

    def segment(self):
        # only for memory access commands
        if len(self.parts) != 3:
            return

        return self.parts[1]

    def index(self):
        # only for memory access commands
        if len(self.parts) != 3:
            return

        return self.parts[2]

    def operation(self):
        return self.parts[0]

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
        'add': [
            # load stack pointer
            '@SP',
            # decrement stack pointer and set address
            'AM=M-1',
            # store top of stack in D
            'D=M',
            # load stack pointer again
            '@SP',
            # decrement stack pointer and set address
            'AM=M-1',
            # set top of stack to x + y
            'M=M+D',
            # load stack pointer
            '@SP',
            # increment stack pointer
            'M=M+1'
        ],
        'sub': [
            # load stack pointer
            '@SP',
            # decrement stack pointer and set address
            'AM=M-1',
            # store top of stack in D
            'D=M',
            # load stack pointer again
            '@SP',
            # decrement stack pointer and set address
            'AM=M-1',
            # set top of stack to x - y
            'M=M-D',
            # load stack pointer
            '@SP',
            # increment stack pointer
            'M=M+1'
        ],
        'neg': [
            # load stack pointer
            '@SP',
            # set address to top of stack pointer
            'A=M-1',
            # negate value at address
            'M=-M'
        ]
    }

    LOGICAL_TRANSLATIONS = {
        'or' : [
            # load stack pointer
            '@SP',
            # decrement stack pointer and set address
            'AM=M-1',
            # store top of stack in D
            'D=M',
            # load stack pointer
            '@SP',
            # decrement stack pointer and set address
            'AM=M-1',
            # x or y
            'M=M|D',
            # load stack pointer
            '@SP',
            # increment stack pointer
            'M=M+1'
        ],
        'not': [
            # load stack pointer
            '@SP',
            # decrement stack pointer and set address
            'AM=M-1',
            # Not top of stack
            'M=!M',
            # decrement stack pointer and set address
            '@SP',
            # load stack pointer
            'M=M+1'
            # increment stack pointer
        ],
        'and': [
            # load stack pointer
            '@SP',
            # decrement stack pointer and set address
            'AM=M-1',
            # store top of stack in D
            'D=M',
            # load stack pointer
            '@SP',
            # decrement stack pointer and set address
            'AM=M-1',
            # x or y
            'M=M&D',
            # load stack pointer
            '@SP',
            # increment stack pointer
            'M=M+1'
        ]
    }
    # can't put translations here because need to update with counter at each iteration
    COMP_COMMANDS = {
        'eq': { 'jump_directive': 'JNE'},
        'lt': { 'jump_directive': 'JGE'},
        'gt': { 'jump_directive': 'JLE'}
    }

    SEGMENT_REGISTER_NAMES = {
        'local'   : 'LCL',
        'argument': 'ARG',
        'this'    : 'THIS',
        'that'    : 'THAT'
    }
    TEMP_BASE_ADDRESS = '5'

    def __init__(self):
        self.counters = {
            'eq' : { 'count': 0 },
            'lt' : { 'count': 0 },
            'gt' : { 'count': 0 }
        }

    def translate(self, command):
        if command.text in self.ARITHMETIC_TRANSLATIONS:
            return self.ARITHMETIC_TRANSLATIONS[command.text]
        elif command.text in self.LOGICAL_TRANSLATIONS:
            return self.LOGICAL_TRANSLATIONS[command.text]
        elif command.text in self.COMP_COMMANDS:
            return self.comp_translation(command.text)
        else: #elif command.push_or_pop():
            if command.operation() == 'push':
                # Push the value of segment[index] onto the stack

                if command.segment() == 'constant':
                    # put the index value on top of the stack

                    return [
                        # load index value
                        '@' + command.index(),
                        # store in D as temp
                        'D=A',
                        # load stack pointer
                        '@SP',
                        # Get current address
                        'A=M',
                        # Store constant in address
                        'M=D',
                        # load stack pointer
                        '@SP',
                        # increment stack pointer
                        'M=M+1'
                    ]
                elif command.segment() in self.SEGMENT_REGISTER_NAMES:
                    # put segment[index] on top of the stack
                    segment_name  = self.SEGMENT_REGISTER_NAMES[command.segment()]

                    return [
                        # load segment ram pointer
                        '@' + segment_name,
                        # store segment base address
                        'D=M', #
                        # load index value
                        '@' + command.index(),
                        # set address base + index
                        'A=A+D',
                        # store segment[index] in D
                        'D=M',
                        # load stack pointer
                        '@SP',
                        # set address
                        'A=M',
                        # set value at address to segment[index]
                        'M=D',
                        # load stack pointer
                        '@SP',
                        # increment stack pointer
                        'M=M+1'
                    ]
                elif command.segment() == 'temp':
                    # put index value
                    return [
                        # load temp address
                        '@' + self.TEMP_BASE_ADDRESS,
                        # store temp base address
                        'D=A',
                        # load index value
                        '@' + command.index(),
                        # set address base + index
                        'A=A+D',
                        # store segment[index] in D
                        'D=M',
                        # load stack pointer
                        '@SP',
                        # set address
                        'A=M',
                        # set top of stack to temp[index]
                        'M=D',
                        # load stack pointer
                        '@SP',
                        # increment stack pointer
                        'M=M+1'
                    ]
            elif command.operation() == 'pop':
                # Pop the top-most value off the stack store in segment[index]

                if command.segment() in self.SEGMENT_REGISTER_NAMES:
                    # pop the top-most item off the stack and store in segment

                    segment_name  = self.SEGMENT_REGISTER_NAMES[command.segment()]

                    return [
                        # load stack pointer
                        '@SP',
                        # decrement pointer to top of stack
                        'AM=M-1',
                        # store value temp in D
                        'D=M',
                        # load temp register
                        '@R5',
                        # store top of stack in temp register
                        'M=D',
                        # load segment base address
                        '@' + segment_name,
                        # store segment base address
                        'D=M',
                        # load index value
                        '@' + command.index(),
                        # store index + base = address we care about
                        'D=A+D',
                        # load temp
                        '@R6',
                        # store segment + index address
                        'M=D',
                        # load top of stack value
                        '@R5',
                        # store in D
                        'D=M',
                        # load segment + index address
                        '@R6',
                        # set as current address register
                        'A=M',
                        # set segment[index] to stack top
                        'M=D'
                    ]
                elif command.segment() == 'temp':
                    return [
                        # load stack pointer
                        '@SP',
                        # decrement pointer to top of stack
                        'AM=M-1',
                        # store value temp in D
                        'D=M',
                        # load temp register
                        '@R5',
                        # store top of stack in temp register
                        'M=D',
                        # load segment base address
                        '@' + self.TEMP_BASE_ADDRESS,
                        # store temp base address
                        'D=A',
                        # load index value
                        '@' + command.index(),
                        # store index + base = address we care about
                        'D=A+D',
                        # load temp
                        '@R6',
                        # store segment + index address
                        'M=D',
                        # load top of stack value
                        '@R5',
                        # store in D
                        'D=M',
                        # load segment + index address
                        '@R6',
                        # set as current address register
                        'A=M',
                        # set segment[index] to stack top
                        'M=D'
                    ]
                elif command.segment() == 'pointer':
                    if command.index() == 0:
                        segment = 'this'
                    elif command.index() == 1:
                        segment == 'that'

                    return [
                        #
                    ]



    def comp_translation(self, command_text):
        counter = self.counters[command_text]
        counter['count'] += 1
        label_identifier = '{}{}'.format(command_text.upper(), counter['count'])
        jump_directive = self.COMP_COMMANDS[command_text]['jump_directive']

        return [
            '@SP',
            'AM=M-1',
            'D=M',
            '@SP',
            'AM=M-1',
            'D=M-D', # x - y
            '@NOT_{}'.format(label_identifier),
            'D;{}'.format(jump_directive),
            '@SP',
            'A=M',
            'M=-1',
            '@INC_STACK_POINTER_{}'.format(label_identifier),
            '0;JMP',
            '(NOT_{})'.format(label_identifier),
            '@SP',
            'A=M',
            'M=0',
            '(INC_STACK_POINTER_{})'.format(label_identifier),
            '@SP',
            'M=M+1'
        ]



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
