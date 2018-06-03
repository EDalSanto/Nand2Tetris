#!/usr/local/bin/python

import sys
import re

class HackAssembler():
    """
    Specific to Hack Computer in Nand2Tetris course

    Input: ASM file with assembly language instructions
    Output: input converted to machine code output
    """

    def __init__(self, input_file):
        self.parser = HackAssemblerParser(input_file)
        self.translator = HackAssemblerDecoder()
        self.symbol_table = SymbolTable()

    # 1st pass
    def parse_for_labels(self):
        count = 0

        while self.parser.has_more_commands():
            self.parser.advance()

            if self.parser.valid_instruction():
                if self.parser.command_type_is('l_command'):
                    self.symbol_table.add_entry(symbol=self.parser.symbol(), address=count)
                else:
                    count += 1

    # 2nd pass
    def run(self):
        self.parser.reset()

        hack_file_name = self.parser.input_file.name.split('.')[0] + '.hack'
        hack_file = open(hack_file_name, 'w+')

        num_matcher = re.compile('[0-9]+')

        while self.parser.has_more_commands():
            self.parser.advance()
            machine_code_parts = []

            if self.parser.command_type_is('a_command'):
                symbol = self.parser.symbol()

                if num_matcher.match(symbol):
                    register_number = int(symbol)
                else:
                    if self.symbol_table.contains(symbol):
                        register_number = self.symbol_table.get_address(symbol)
                    else:
                        register_number = self.symbol_table.add_entry(symbol)

                machine_code = HackAssemblerDecoder.decimal_to_binary_string(register_number)
                machine_code_parts.append(machine_code)
            elif self.parser.command_type_is('l_command'):
                continue
            elif self.parser.command_type_is('c_command'):
                # Init
                machine_code_parts.append(HackAssemblerDecoder.C_COMMAND_INIT_BITS)
                # Comp
                comp_mnemonic = self.parser.comp_mnemonic()
                comp_bits = HackAssemblerDecoder.COMP_MNEMONIC_TO_BITS[comp_mnemonic]
                machine_code_parts.append(comp_bits)
                # Dest
                dest_mnemonic = self.parser.dest_mnemonic()
                dest_bits = HackAssemblerDecoder.DEST_MNEMONIC_TO_BITS[dest_mnemonic]
                machine_code_parts.append(dest_bits)
                # Jump
                jump_mnemonic = self.parser.jump_mnemonic()
                jump_bits = HackAssemblerDecoder.JUMP_MNEMONIC_TO_BITS[jump_mnemonic]
                machine_code_parts.append(jump_bits)

            if len(machine_code_parts) > 0:
                machine_code_command = ''.join(machine_code_parts)
                hack_file.write(machine_code_command + '\n')

        hack_file.close()


class HackAssemblerDecoder():
    C_COMMAND_INIT_BITS = '111'

    DEST_MNEMONIC_TO_BITS = {
        None : '000',
        'M'  : '001',
        'D'  : '010',
        'MD' : '011',
        'A'  : '100',
        'AM' : '101',
        'AD' : '110',
        'AMD': '111'
    }

    COMP_MNEMONIC_TO_BITS = {
        None : '',
        '0'  : '0101010',
        '1'  : '0111111',
        '-1' : '0111010',
        'D'  : '0001100',
        'A'  : '0110000',
        'M'  : '1110000',
        '!D' : '0001101',
        '!A' : '0110011',
        '!M' : '1110011',
        'D+1': '0011111',
        'A+1': '0110111',
        'M+1': '1110111',
        'D-1': '0001110',
        'A-1': '0110010',
        'M-1': '1110010',
        'D+A': '0000010',
        'D+M': '1000010',
        'D-A': '0010011',
        'D-M': '1010011',
        'A-D': '0000111',
        'M-D': '1000111',
        'D&A': '0000000',
        'D&M': '1000000',
        'D|A': '0010101',
        'D|M': '1010101'
    }

    JUMP_MNEMONIC_TO_BITS = {
        None : '000',
        'JGT': '001',
        'JEQ': '010',
        'JGE': '011',
        'JLT': '100',
        'JNE': '101',
        'JLE': '110',
        'JMP': '111'
    }

    @classmethod
    def decimal_to_binary_string(cls, num):
        return '{0:016b}'.format(num)


class SymbolTable():
    PREDEFINED_SYMBOLS = {
        'SP': 0,
        'LCL': 1,
        'ARG': 2,
        'THIS': 3,
        'THAT': 4,
        'R0': 0,
        'R1': 1,
        'R2': 2,
        'R3': 3,
        'R4': 4,
        'R5': 5,
        'R6': 6,
        'R7': 7,
        'R8': 8,
        'R9': 9,
        'R10': 10,
        'R11': 11,
        'R12': 12,
        'R13': 13,
        'R14': 14,
        'R15': 15
    }

    def __init__(self):
        self.symbols = self.PREDEFINED_SYMBOLS

    def add_entry(self, symbol=None, address=None):
        if address:
            self.symbols[symbol] = address
        else:
            self.symbols[symbol] = len(self.symbols)

        return self.get_address(symbol)


    def contains(self, symbol):
        return symbol in self.symbols

    def get_address(self, symbol):
        return self.symbols[symbol]


class HackAssemblerParser():
    """
    Reads each line in the input file one a time and reports on state of current line
    """
    DEST_DELIMITER = '='
    JUMP_DELIMITER = ';'

    def __init__(self, input_file):
        self.input_file = open(input_file, 'r')
        self.current_line = None
        self.current_command = None
        self.next_line = None
        self.valid_char_matcher = re.compile('[a-zA-Z0-9=+;]+')

    def reset(self):
        self.input_file.seek(0)
        self.current_line = None
        self.current_command = None
        self.next_line = None

    def dest_mnemonic(self):
        if self.current_line.find(self.DEST_DELIMITER) != -1:
            res = self.current_line.split(self.DEST_DELIMITER)[0]
            return self.string_without_invalid_characters(res)

    def comp_mnemonic(self):
        if self.current_line.find(self.DEST_DELIMITER) != -1:
            res = self.current_line.split(self.DEST_DELIMITER)[1].rstrip('\n')
            return self.string_without_invalid_characters(res)
        elif self.current_line.find(self.JUMP_DELIMITER) != -1:
            res = self.current_line.split(self.JUMP_DELIMITER)[0].rstrip('\n')
            return self.string_without_invalid_characters(res)


    def jump_mnemonic(self):
        if self.current_line.find(self.JUMP_DELIMITER) != -1:
            res = self.current_line.split(self.JUMP_DELIMITER)[1].rstrip('\n')
            return self.string_without_invalid_characters(res)

    def symbol(self):
        """
        returns decimal number or symbol
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

        if self._matching_chars(self.current_line):
            self.current_line = self.string_without_invalid_characters(self.current_line)

        self.next_line = self.input_file.readline()
        self.find_new_command_type()

    def command_type_is(self, possible_command_type):
        return possible_command_type == self.current_command

    def command_type(self):
        return self.command_type

    def find_new_command_type(self):
        """
        assumes valid input
        """
        first_char = self.current_line[0]

        if not self.valid_instruction():
            self.current_command = 'comment_or_empty_line'
        elif first_char == '@':
            self.current_command = 'a_command'
        elif first_char == '(':
            self.current_command = 'l_command'
        else:
            self.current_command = 'c_command'

    def string_without_invalid_characters(self, string):
        return self._matching_chars(string).group()

    def _matching_chars(self, string):
        return self.valid_char_matcher.match(string.strip())

    def valid_instruction(self):
        return not self._comment_line() and not self._empty_line()

    def _comment_line(self):
        return self.current_line[0] == '/'

    def _empty_line(self):
        return self.current_line == '\n'


asm_input_file = sys.argv[1]
assembler = HackAssembler(asm_input_file)
assembler.parse_for_labels()
assembler.run()
