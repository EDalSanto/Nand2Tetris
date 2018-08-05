class JackTokenizer():
    KEYWORDS = [
        'class',
        'constructor',
        'function',
        'method',
        'field',
        'static',
        'var',
        'int',
        'char',
        'boolean',
        'void',
        'true',
        'false',
        'null',
        'this',
        'let',
        'do',
        'if',
        'else',
        'while',
        'return'
    ]
    SYMBOL_CONVERSIONS = {
        '<': '&lt;',
        '>': '&gt;',
        '\"': '&quot;',
        '&': '&amp;'
    }

    """
    goes through a .jack input file and produces a stream of tokens
    ignores all whitespace and comments
    """
    def __init__(self, input_file):
        self.input_file = input_file
        self.tokens_found = []
        self.current_token = None
        self.next_token = None
        self.has_more_tokens = True

    def advance(self):
        # read first char
        char = self.input_file.read(1)

        # skip whitespace and comments
         # if space
             # read 1 char bc we don't know what's next
         # if start of comment
             # check that not operator
             # if not, read whole line

        while char.isspace() or char in ["/", "*"]:
            if char.isspace():
                char = self.input_file.read(1)
            elif char in ["/", "*"]:
                # make sure not operator
                last_pos = self.input_file.tell()
                next_2_chars = self.input_file.read(2)
                single_line_comment = next_2_chars[0] == "/"
                multi_line_comment = char == "/" and next_2_chars[0] == "*" and next_2_chars[1] == "*"
                if not single_line_comment and not multi_line_comment:
                    # go back
                    self.input_file.seek(last_pos)
                    break

                multi_line_comment = False
                # read whole line
                self.input_file.readline()
                # read next char
                char = self.input_file.read(1)
            continue

       # process found token
        token = ""

        if self._is_string_const_delimeter(char):
            # add initial "
            token += char
            char = self.input_file.read(1)

            # get rest of token up to ending "
            while not self._is_string_const_delimeter(char):
                token += char
                char = self.input_file.read(1)

            # get last "
            token += char
        elif char.isalnum():
            # get rest of token
            while self._is_alnum_or_underscore(char):
                token += char
                last_pos = self.input_file.tell()
                char = self.input_file.read(1)

            # go back 1 char that was peek ahead
            self.input_file.seek(last_pos)
        else: # symbol
            # adjust for stupid xml
            if char in self.SYMBOL_CONVERSIONS:
                token = self.SYMBOL_CONVERSIONS[char]
            else:
                token = char

        # set tokens
        if self.current_token:
            self.current_token = self.next_token
            self.next_token = token
            self.tokens_found.append(token)
        else: # initial setup
            self.current_token = token
            self.next_token = token
            # update next token
            self.advance()

        if not len(self.next_token) > 0:
            self.has_more_tokens = False
            return False
        else:
            return True

    def part_of_subroutine_call(self):
        if len(self.tokens_found) < 3:
            return False

        index = len(self.tokens_found) - 4
        token = self.tokens_found[index]

        if token == ".":
            return True
        else:
            return False

    def current_token_type(self):
        if self.current_token[0] == "\"":
            return "STRING_CONST"
        elif self.current_token in self.KEYWORDS:
            return "KEYWORD"
        elif self.current_token.isnumeric():
            return "INT_CONST"
        elif self.current_token.isalnum():
            return "IDENTIFIER"
        else:
            return "SYMBOL"

    def keyword(self):
        if self.current_token_type() == "KEYWORD":
            return self.current_token

    def symbol(self):
        if self.current_token_type() == "SYMBOL":
            return self.current_token

    def identifier(self):
        if self.current_token_type() == "IDENTIFIER":
            return self.current_token

    def int_val(self):
        if self.current_token_type() == "INT_CONST":
            return self.current_token

    def string_val(self):
        if self.current_token_type() == "STRING_CONST":
            return self.current_token

    def _is_alnum_or_underscore(self, char):
        return char.isalnum() or char == "_"

    def _is_string_const_delimeter(self, char):
        return char == "\""
