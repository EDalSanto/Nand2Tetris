import sys
import os
import re
import glob

class VMCommand():
    """
    provides simpler interface and encapsulation for inspecting current command
    """
    COMMENT_SYMBOL = '//'
    NEWLINE_SYMBOL = '\n'
    EMPTY_SYMBOL = ''
    COMPARISON_OPERATIONS = [ 'eq', 'lt', 'gt' ]
    ARITHMETIC_BINARY_OPERATIONS = [ 'add', 'sub', 'and', 'or' ]
    ARITHMETIC_UNARY_OPERATIONS = [ 'neg', 'not' ]

    def __init__(self, raw_text):
        self.raw_text = raw_text

    def text(self):
        return self.raw_text.split(self.COMMENT_SYMBOL)[0].strip()

    def parts(self):
        return self.text().split(' ')

    def label(self):
        if self.is_branching_command():
            return self.parts()[1]

    def function_name(self):
        if self.is_function_definition_command() or self.is_function_call_command():
            return self.parts()[1]

    def num_arguments(self):
        if self.is_function_call_command():
            return self.parts()[2]

    def locals(self):
        if self.is_function_definition_command():
            return self.parts()[2]

    def for_static_memory_segment(self):
        if self.memory_access_command():
            return self.segment() == 'static'

    def segment(self):
        if self.memory_access_command():
            return self.parts()[1]

    def index(self):
        if self.memory_access_command():
            return self.parts()[2]

    def is_function_command(self):
        return self.is_function_definition_command() or self.is_call_command() or self.is_return_command()

    def is_function_definition_command(self):
        return self.operation() == 'function'

    def is_function_call_command(self):
        return self.operation() == 'call'

    def is_return_command(self):
        return self.operation() == 'return'

    def is_branching_command(self):
        return self.is_goto_command() or self.is_label_command() or self.is_ifgoto_command()

    def is_goto_command(self):
        return self.operation() == 'goto'

    def is_ifgoto_command(self):
        return self.operation() == 'if-goto'

    def is_label_command(self):
        return self.operation() == 'label'

    def is_push_or_pop_command(self):
        return self.is_push_command() or self.is_pop_command()

    def is_push_command(self):
        return self.operation() == 'push'

    def is_pop_command(self):
        return self.operation() == 'pop'

    def is_comment(self):
        return self.raw_text[0:2] == self.COMMENT_SYMBOL

    def is_whitespace(self):
        return self.raw_text == self.NEWLINE_SYMBOL

    def is_empty(self):
        return self.raw_text == self.EMPTY_SYMBOL

    def operation(self):
        return self.parts()[0]

    def memory_access_command(self):
        return len(self.parts()) == 3

    def is_logical_command(self):
        return self.is_comparison_command() or self.is_arithmetic_binary_command() or self.is_arithmetic_unary_command()

    def is_comparison_command(self):
        return self.operation() in self.COMPARISON_OPERATIONS

    def is_arithmetic_binary_command(self):
        return self.operation() in self.ARITHMETIC_BINARY_OPERATIONS

    def is_arithmetic_unary_command(self):
        return self.operation() in self.ARITHMETIC_UNARY_OPERATIONS

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

    def has_invalid_current_command(self):
        return self.current_command.is_whitespace() or self.current_command.is_comment()

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
    """
    simply wrapper for interacting with output file
    """
    def __init__(self, output_file_name):
        self.output_file = open(output_file_name, 'w')

    def write(self, command):
        self.output_file.write(command + "\n")

    def close_file(self):
        self.output_file.close()


class VMLogicalTranslator():
    ARITHMETIC_OPERATIONS_ASM_INSTRUCTIONS = {
        'add': 'M=M+D',
        'sub': 'M=M-D',
        'neg': 'M=-M',
        'or' : 'M=M|D',
        'not': 'M=!M',
        'and': 'M=M&D'
    }

    COMPARISON_OPERATIONS_JUMP_DIRECTIVES = {
        'eq': 'JNE',
        'lt': 'JGE',
        'gt': 'JLE'
    }

    def __init__(self):
        self.comparison_counters = {
            'eq' : { 'count': 0 },
            'lt' : { 'count': 0 },
            'gt' : { 'count': 0 }
        }

    def translate_arithmetic_binary(self, command):
        return [
            *self._pop_top_number_off_stack_instructions(),
            # put in temp D for operation
            'D=M',
            *self._pop_top_number_off_stack_instructions(),
            self.ARITHMETIC_OPERATIONS_ASM_INSTRUCTIONS[command.operation()],
            *self._increment_stack_pointer_instructions()
        ]

    def translate_arithmetic_unary(self, command):
        return [
            *self._pop_top_number_off_stack_instructions(),
            self.ARITHMETIC_OPERATIONS_ASM_INSTRUCTIONS[command.operation()],
            *self._increment_stack_pointer_instructions()
        ]

    def translate_comparison(self, command):
        counter = self.comparison_counters[command.operation()]
        counter['count'] += 1
        label_identifier = '{}{}'.format(command.text().upper(), counter['count'])
        jump_directive = self.COMPARISON_OPERATIONS_JUMP_DIRECTIVES[command.operation()]

        return [
            *self._pop_top_number_off_stack_instructions(),
            # set D to top of stack
            'D=M',
            *self._pop_top_number_off_stack_instructions(),
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
            *self._increment_stack_pointer_instructions()
        ]

    def _pop_top_number_off_stack_instructions(self):
        return [
            # load stack pointer
            '@SP',
            # decrement stack pointer and set address
            'AM=M-1'
        ]

    def _increment_stack_pointer_instructions(self):
        return [
            # load stack pointer
            '@SP',
            # increment stack pointer
            'M=M+1'
        ]


class VMPushPopTranslator():
    VIRTUAL_MEMORY_SEGMENTS_BASE_ADDRESSES = {
        'local': '1',
        'argument': '2',
        'this': '3',
        'that': '4'
    }
    POINTER_SEGMENT_BASE_ADDRESS = '3'
    TEMP_SEGMENT_BASE_ADDRESS = '5'
    STATIC_SEGMENT_BASE_ADDRESS = '16'

    def translate_static_pop(self, command, current_file_name):
        return [
            *self.store_top_of_stack_in_D_instructions(),
            # set value at address to D
            *self.set_address_to_top_of_stack_instructions(
                address='{}.{}'.format(current_file_name, command.index())
            )
        ]

    def translate_static_push(self, command, current_file_name):
        return [
            # load Filename.index
            *self.load_referenced_value_in_D_instructions(
                '{}.{}'.format(current_file_name, command.index()),
            ),
            *self.place_value_in_D_on_top_of_stack_instructions(),
            *self.increment_stack_pointer_instructions()
        ]

    def translate_push(self, command):
        # Push the value of segment[index] onto the stack
        return [
            *self._load_desired_value_into_D_instructions_for(command),
            *self._place_value_in_D_on_top_of_stack_instructions(),
            *self._increment_stack_pointer_instructions()
        ]

    def translate_pop(self, command):
        return [
            *self._store_top_of_stack_in_D_instructions(),
            *self._store_top_of_stack_first_temp_register_instructions(),
            *self._load_base_address_instructions_for(segment=command.segment()),
            *self._add_index_to_base_address_in_D_instructions(command),
            *self._store_target_address_in_second_temp_register_instructions(),
            *self._set_target_address_to_value_instructions()
        ]

    def _load_desired_value_into_D_instructions_for(self, command):
        if command.segment() == 'constant':
            return [
                *self._load_value_in_D_instructions(value=command.index())
            ]
        else:
            return [
                *self._load_base_address_instructions_for(segment=command.segment()),
                *self._add_index_to_base_address_in_D_instructions(command),
                *self._load_value_at_memory_address_in_D_instructions()
            ]

    def _load_base_address_instructions_for(self, segment):
        if segment in self.VIRTUAL_MEMORY_SEGMENTS_BASE_ADDRESSES:
            pointer_to_segment_base_address = self.VIRTUAL_MEMORY_SEGMENTS_BASE_ADDRESSES[segment]
            return self._load_referenced_value_in_D_instructions(address=pointer_to_segment_base_address)
        elif segment == 'temp':
            return self.load_value_in_D_instructions(value=self.TEMP_SEGMENT_BASE_ADDRESS)
        elif segment == 'static':
            return self.load_value_in_D_instructions(value=self.STATIC_SEGMENT_BASE_ADDRESS)
        elif segment == 'pointer':
            return self.load_value_in_D_instructions(value=self.POINTER_SEGMENT_BASE_ADDRESS)

    def _place_value_in_D_on_top_of_stack_instructions(self):
        return [
            # load stack pointer
            '@SP',
            # Get current address
            'A=M',
            # Store constant in address
            'M=D'
        ]

    def _increment_stack_pointer_instructions(self):
        return [
            # load stack pointer
            '@SP',
            # increment stack pointer
            'M=M+1'
        ]

    def _load_value_in_D_instructions(self, value):
        return [
            # load value
            '@' + value,
            # store value in D
            'D=A'
        ]

    def _load_referenced_value_in_D_instructions(self, address):
        return [
            # load address
            '@' + address,
            # store address value
            'D=M'
        ]

    def _add_index_to_base_address_in_D_instructions(self, command):
        return [
            '@' + command.index(),
            'D=D+A'
        ]

    def _load_value_at_memory_address_in_D_instructions(self):
        return [
            # set A to address stored in D
            'A=D',
            # now put value at new address in D
            'D=M'
        ]

    def _set_address_to_top_of_stack_instructions(self, address):
        return [
            # load segment address
            '@' + address,
            # set segment equal to top of stack
            'M=D'
        ]

    # makes use of temp registers
    def _set_target_address_to_value_instructions(self):
        return [
            # load top of stack value
            '@R13',
            # store in D
            'D=M',
            # load segment + index address
            '@R14',
            # set as current address register
            'A=M',
            # set segment[index] to stack top
            'M=D'
        ]

    # makes use of temp registers
    def _store_target_address_in_second_temp_register_instructions(self):
        return [
            # load temp
            '@R14',
            # store segment + index address
            'M=D'
        ]

    # makes use of temp registers
    # (when top of stack already in D)
    def _store_top_of_stack_first_temp_register_instructions(self):
        return [
            # load temp register
            '@R13',
            # store top of stack in temp register
            'M=D'
        ]

    def _store_top_of_stack_in_D_instructions(self):
        return [
            # load stack pointer
            '@SP',
            # decrement pointer to top of stack
            'AM=M-1',
            # store value in D
            'D=M'
        ]

class VMBranchingTranslator():
    def translate_label(self, command):
        return [
            '({})'.format(command.label())
        ]

    def translate_goto(self, command):
        # unconditionally jump to label
        return [
            '@' + command.label(),
            '0;JMP'
        ]

    def translate_ifgoto(self, command):
        # jump if the topmost item on the stack is not equal to zero
        return [
            # pop top most item off stack
            '@SP',
            'AM=M-1',
            'D=M',
            # jump is not 0
            '@' + command.label(),
            'D;JNE'
        ]

class VMFunctionTranslator():
    NUM_SEGMENTS_COPIED_TO_NEW_STACK_FRAME = 5

    def __init__(self):
        self.function_count = 0
        self.call_count = 0

    def init_code(self):
        return [
            # set SP = 256
            '@256',
            'D=A',
            '@SP',
            'M=D',
            # call Sys.init
            *self.translate_function_call(VMCommand('call Sys.init 0'))
        ]

    def translate_function_definition(self, command):
        self.function_count += 1

        return [
            # establish function label -> will be used to jump to spot when called
            '({})'.format(command.function_name()),
            ## push onto the stack 0 command.locals() times
            # initialize loop times
            '@' + command.locals(),
            # store in D
            'D=A',
            # establish loop label
            '(LOOP.ADD_LOCALS.{})'.format(self.function_count),
            # skip if D eq 0
            '@NO_LOCALS.{}'.format(self.function_count),
            'D;JEQ',
            ## push 0 onto stack D times
            # load stack pointer
            '@SP',
            # get pointer address
            'A=M',
            # set to 0
            'M=0',
            # increment stack pointer
            '@SP',
            'M=M+1',
            # decrement D
            'D=D-1',
            # load loop
            '@LOOP.ADD_LOCALS.{}'.format(self.function_count),
            # jump back if not 0
            'D;JNE',
            '(NO_LOCALS.{})'.format(self.function_count)
        ]

    def translate_function_call(self, command):
        self.call_count += 1

        return [
            ## push return address onto stack
            # load return address label
            '@RET_ADDRESS.{}'.format(self.call_count),
            # get address value
            'D=A',
            # load stack pointer
            '@SP',
            # load address
            'A=M',
            # set value at address to D, return address
            'M=D',
            # increment stack pointer
            '@SP',
            'M=M+1',
            ## push LCL address onto stack
            *self._push_referenced_address_onto_stack('LCL'),
            ## push ARG address onto stack
            *self._push_referenced_address_onto_stack('ARG'),
            ## push THIS address onto stack
            *self._push_referenced_address_onto_stack('THIS'),
            ## push THAT address onto stack
            *self._push_referenced_address_onto_stack('THAT'),
            ## ARG = SP - nArgs - 5
            # get value of SP
            '@SP',
            'D=M',
            # substract num arguments
            '@{}'.format(command.num_arguments()),
            'D=D-A',
            # subtract 5
            '@{}'.format(self.NUM_SEGMENTS_COPIED_TO_NEW_STACK_FRAME),
            'D=D-A',
            # set ARG
            '@ARG',
            'M=D',
            ## LCL = SP reposition LCL
            '@SP',
            'D=M',
            '@LCL',
            'M=D',
            ## jump to function (which will run this function's instructions)
            '@{}'.format(command.function_name()),
            '0;JMP',
            ## label for return address
            '(RET_ADDRESS.{})'.format(self.call_count)
        ]

    def translate_return(self, command):
        return [
            # FRAME=LCL // FRAME is a temporary variable
            '@LCL',
            # store in D
            'D=M', # Frame
            # load temp register
            '@R13',
            # store Frame in temp register
            'M=D',
            # RET=*(FRAME-5) // save return address in a temp. var
            # load value to subtract
            '@5',
            # store value in D
            'D=A',
            # load frame from temp
            '@R13',
            # get address value into A
            'A=M-D',
            # dereference to get value at mem address
            'D=M',
            # load into temp reg
            '@R14',
            'M=D',
            # *ARG=pop() // reposition return value for caller
            # pop of stack off into D
            '@SP',
            # decrment address and stack pointer
            'AM=M-1',
            # store value at top of stack in D
            'D=M',
            # set top of arg stack to return value for caller
            '@ARG',
            # get register access at memory address
            'A=M',
            # set to D, top of stack value
            'M=D',
            #SP=ARG+1 // restore SP for caller
            '@ARG',
            # store current address of ARG + 1 in D
            'D=M+1',
            # load stack pointer
            '@SP',
            # set address to arg + 1
            'M=D',
            *self._restore_calling_function('THAT', slots_behind_frame_end=1),
            *self._restore_calling_function('THIS', slots_behind_frame_end=2),
            *self._restore_calling_function('ARG', slots_behind_frame_end=3),
            *self._restore_calling_function('LCL', slots_behind_frame_end=4),
            #goto RET // GOTO the return-address
            # load RET
            '@R14',
            'A=M',
            # go to RET
            '0;JMP'
        ]

    def _push_referenced_address_onto_stack(virtual_memory_segment):
        return [
            # load register with address value
            '@{}'.format(virtual_memory_segment),
            # get its address
            'D=M',
            # load stack pointer
            '@SP',
            # load address
            'A=M',
            # set value at address to D, return address
            'M=D',
            # increment stack pointer
            '@SP',
            'M=M+1',
        ]

    def _restore_calling_function(self, memory_segment, slots_behind_frame_end):
        return [
            # load delta before frame end
            '@{}'.format(slots_behind_frame_end),
            # place in D
            'D=A',
            # load frame
            '@R13',
            # get address value into A
            'A=M-D',
            # dereference to get value at mem address
            'D=M',
            # load LCL
            '@{}'.format(memory_segment),
            # set value at THAT to D
            'M=D'
        ]

class Main():
    def __init__(self, input):
        self.input = input
        self.current_file = None
        # maybe these go inside the translator and wrap up to 1 translate method
        self.logical_translator = VMLogicalTranslator()
        self.push_pop_translator = VMPushPopTranslator()
        self.branching_translator = VMBranchingTranslator()
        self.function_translator = VMFunctionTranslator()

    def run_program(self):
        if os.path.isfile(self.input):
            # get vm files to translate
            vm_files = [self.input]
            # get output file name
            ouput_file_name = input.split('.')[0] + '.asm'
            # init writer
            writer = VMWriter(output_file_name)
        elif os.path.isdir(self.input):
            # get vm files to translate
            vm_path = os.path.join(self.input, "*.vm")
            vm_files = glob.glob(vm_path)
            # get output file name
            last_dir_name = os.path.basename(input)
            output_file_name = input + "/" + last_dir_name + ".asm"
            # init writer
            writer = VMWriter(output_file_name)
            # init code specific for directory
            init_code = self.function_translator.init_code()
            for line in init_code:
                writer.write(line)

        for vm_file in vm_files:
            self.current_file = vm_file
            parser = VMParser(vm_file)

            while parser.has_more_commands:
                parser.advance()

                if parser.has_invalid_current_command():
                    continue

                translation = _self.find_translation_for(parser.current_command)
                for line in translation:
                    writer.write(line)

        writer.close_file()

    def _find_translation_for(self, current_command):
        if current_command.is_push_command():
            if current_command.for_static_memory_segment():
                return self.push_pop_translator.translate_static_push(current_command, self._current_filename_without_extension())
            else:
                return self.push_pop_translator.translate_push(current_command)
        elif current_command.is_pop_command():
            if current_command.for_static_memory_segment():
                return self.push_pop_translator.translate_static_pop(current_command, self._current_filename_without_extension())
            else:
                return self.push_pop_translator.translate_pop(current_command)
        elif current_command.is_return_command():
            return self.function_translator.translate_return(current_command)
        elif current_command.is_function_definition_command():
            return self.function_translator.translate_function_definition(current_command)
        elif current_command.is_function_call_command():
            return self.function_translator.translate_function_call(current_command)
        elif current_command.is_label_command():
            return self.branching_translator.translate_label(current_command)
        elif current_command.is_goto_command():
            return self.branching_translator.translate_goto(current_command)
        elif current_command.is_ifgoto_command():
            return self.branching_translator.translate_ifgoto(current_command)
        elif current_command.is_arithmetic_binary_command():
            return self.logical_translator.translate_arithmetic_binary(current_command)
        elif current_command.is_arithmetic_unary_command():
            return self.logical_translator.translate_arithmetic_unary(current_command)
        elif current_command.is_comparison_command():
            return self.logical_translator.translate_comparison(current_command)

    def _current_filename_without_extension(self):
        return self.current_file.split(".")[0].split("/")[-1]



if __name__ == "__main__" and len(sys.argv) == 2:
    input = sys.argv[1]
    Main(input).run_program()
