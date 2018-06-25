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

    VIRTUAL_MEMORY_SEGMENTS = {
        'local'    : { 'base_address_pointer': '1' },
        'argument' : { 'base_address_pointer': '2' },
        'this'     : { 'base_address_pointer': '3' },
        'that'     : { 'base_address_pointer': '4' }
    }

    POINTER_SEGMENT_BASE_ADDRESS = '3'

    HOST_SEGMENTS = {
        'temp'  : { 'base_address': '5' },
        'static': { 'base_address': '16'}
    }

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
        elif command.operation() == 'push':
            # Push the value of segment[index] onto the stack

            return [
                *self.load_desired_value_into_D_instructions_for(segment=command.segment(), index=command.index()),
                *self.place_value_in_D_on_top_of_stack_instructions(),
                *self.increment_stack_pointer_instructions()
            ]
        elif command.operation() == 'pop':
            # Pop the top-most value off the stack store in segment[index]

            return [
                *self.store_top_of_stack_in_D_instructions(),
                *self.store_top_of_stack_first_temp_register_instructions(),
                *self.load_base_address_instructions_for(segment=command.segment()),
                *self.add_index_to_base_address_in_D_instructions(index=command.index()),
                *self.store_target_address_in_second_temp_register_instructions(),
                *self.set_target_address_to_value_instructions()
            ]


    def load_desired_value_into_D_instructions_for(self, segment, index):
        if segment == 'constant':
            return [
                *self.load_value_in_D_instructions(value=index)
            ]
        else:
            return [
                *self.load_base_address_instructions_for(segment=segment),
                *self.add_index_to_base_address_in_D_instructions(index=index),
                *self.load_value_at_memory_address_in_D_instructions()
            ]

    def load_base_address_instructions_for(self, segment):
        if segment in self.VIRTUAL_MEMORY_SEGMENTS:
            pointer_to_segment_base_address = self.VIRTUAL_MEMORY_SEGMENTS[segment]['base_address_pointer']
            return self.load_referenced_value_in_D_instructions(address=pointer_to_segment_base_address)
        elif segment in self.HOST_SEGMENTS:
            host_segment_base_address = self.HOST_SEGMENTS[segment]['base_address']
            return self.load_value_in_D_instructions(value=host_segment_base_address)
        elif segment == 'pointer':
            return self.load_value_in_D_instructions(value=self.POINTER_SEGMENT_BASE_ADDRESS)


    def place_value_in_D_on_top_of_stack_instructions(self):
        return [
            # load stack pointer
            '@SP',
            # Get current address
            'A=M',
            # Store constant in address
            'M=D'
        ]

    def increment_stack_pointer_instructions(self):
        return [
            # load stack pointer
            '@SP',
            # increment stack pointer
            'M=M+1'
        ]

    def load_value_in_D_instructions(self, value):
        return [
            # load value
            '@' + value,
            # store value in D
            'D=A'
        ]

    def load_referenced_value_in_D_instructions(self, address):
        return [
            # load address
            '@' + address,
            # store address value
            'D=M'
        ]

    def add_index_to_base_address_in_D_instructions(self, index):
        return [
            '@' + index,
            'D=D+A'
        ]
    def load_value_at_memory_address_in_D_instructions(self):
        return [
            'A=D',
            'D=M'
        ]

    def set_address_to_top_of_stack_instructions(self, address):
        return [
            # load segment address
            '@' + address,
            # set segment equal to top of stack
            'M=D'
        ]

    def set_target_address_to_value_instructions(self):
        return [
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

    def store_target_address_in_second_temp_register_instructions(self):
        return [
            # load temp
            '@R6',
            # store segment + index address
            'M=D'
        ]

    def store_top_of_stack_first_temp_register_instructions(self):
        return [
            # load temp register
            '@R5',
            # store top of stack in temp register
            'M=D'
        ]

    def store_top_of_stack_in_D_instructions(self):
        return [
            # load stack pointer
            '@SP',
            # decrement pointer to top of stack
            'AM=M-1',
            # store value in D
            'D=M'
        ]

    def comp_translation(self, command_text):
        counter = self.counters[command_text]
        counter['count'] += 1
        label_identifier = '{}{}'.format(command_text.upper(), counter['count'])
        jump_directive = self.COMP_COMMANDS[command_text]['jump_directive']

        return [
            # load stack pointer
            '@SP',
            # set address and decrement stack pointer
            'AM=M-1',
            # set D to top of stack
            'D=M',
            # load stack pointer
            '@SP',
            # set address and decrement stack pointer
            'AM=M-1',
            # set D to x-y
            'D=M-D',
            # load not true label
            '@NOT_{}'.format(label_identifier),
            # jump to not true section on directive
            'D;{}'.format(jump_directive),
            # load stack pointer
            '@SP',
            # set A to top of stack address
            'A=M',
            # set it to -1 for true
            'M=-1',
            # load inc stack pointer
            '@INC_STACK_POINTER_{}'.format(label_identifier),
            # jump uncoditionally
            '0;JMP',
            # not true section
            '(NOT_{})'.format(label_identifier),
            # load stack pointer
            '@SP',
            # set A to to top of stack address
            'A=M',
            # set to 0 for false
            'M=0',
            # define inc stack pointer label
            '(INC_STACK_POINTER_{})'.format(label_identifier),
            # load stack pointer
            '@SP',
            # increment stack pointer
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
