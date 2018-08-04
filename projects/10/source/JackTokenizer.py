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
        'false'
        'null',
        'this',
        'let',
        'do',
        'if',
        'else',
        'while',
        'return'
    ]

    """
    goes through a .jack input file and produces a stream of tokens
    ignores all whitespace and comments
    """
    def __init__(self, input_file):
        self.input_file = input_file
        self.current_token = None
        self.next_token = None
        self.has_more_tokens = True

    def advance(self):
        # read first char
        char = self.input_file.read(1)

        # skip all whitespace and comments
        while char.isspace() or char == "/":
            if char.isspace():
                char = self.input_file.read(1)
            elif char == "/":
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
                char = self.input_file.read(1)

            # go back 1 char that was peek ahead
            self.input_file.seek(self.input_file.tell() - 1)
        else: # symbol
            token = char

        if self.current_token:
            self.current_token = self.next_token
            self.next_token = token
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
