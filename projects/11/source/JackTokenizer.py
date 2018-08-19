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
    COMMENT_OPERATORS = ["/", "*"]
    STRING_CONST_DELIMITER = '"'

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
        # initialize char
        char = self.input_file.read(1)
        # skip whitespace and comments
        char = self._skip_whitespace_and_comments(starting_char=char)

        # get token
        if self._is_string_const_delimeter(char):
            token = self._get_string_const(starting_char=char)
        elif char.isalnum():
            token = self._get_alnum_underscore(starting_char=char)
        else: # symbol
            token = char

        # set tokens
        if self.current_token:
            self.current_token = self.next_token
            self.next_token = token
            self.tokens_found.append(token)
        else: # initial setup
            self.current_token = token
            self.next_token = token
            self.tokens_found.append(token)
            # get next token
            self.advance()

        if self._current_token_empty():
            self.has_more_tokens = False

    def class_token_reached(self):
        return self.current_token == 'class'

    def token_type_of(self, token):
        if token[0] == "\"":
            return "STRING_CONST"
        elif token in self.KEYWORDS:
            return "KEYWORD"
        elif token.isnumeric():
            return "INT_CONST"
        elif token.isalnum():
            return "IDENTIFIER"
        else:
            return "SYMBOL"

    def null(self):
        if self.current_token == 'null':
            return self.current_token

    def boolean(self):
        if self.current_token in ['true', 'false']:
            return self.current_token

    def keyword(self):
        if self.token_type_of(self.current_token) == "KEYWORD":
            return self.current_token

    def identifier(self):
        if self.token_type_of(self.current_token) == "IDENTIFIER":
            return self.current_token

    def string_const(self):
        if self.token_type_of(self.current_token) == "STRING_CONST":
            # remove " that denote string const
            return self.current_token.replace('"', '')

    def _current_token_empty(self):
        return len(self.current_token) == 0

    def _get_alnum_underscore(self, starting_char):
        token = ''
        char = starting_char
        # get rest of token
        while self._is_alnum_or_underscore(char):
            # keep track of what was last read
            last_pos = self.input_file.tell()
            token += char
            char = self.input_file.read(1)

        # go back 1 char that was peek ahead to determine if no longer alnum / underscore
        self.input_file.seek(last_pos)
        return token

    def _get_string_const(self, starting_char):
        char = starting_char
        token = ''

        # add initial "
        token += char
        char = self.input_file.read(1)

        # get rest of token up to ending "
        while not self._is_string_const_delimeter(char):
            token += char
            char = self.input_file.read(1)

        # get last "
        token += char
        return token

    def _skip_whitespace_and_comments(self, starting_char):
        char = starting_char

        while char.isspace() or char in self.COMMENT_OPERATORS:
            if char.isspace():
                # read 1 char bc we don't know what's next
                char = self.input_file.read(1)
            elif char in self.COMMENT_OPERATORS:
                # make sure comment and not operator
                last_pos = self.input_file.tell()
                # read rest of line
                rest_of_line = self.input_file.readline()
                if not self._is_start_of_comment(char, rest_of_line):
                    # go back
                    self.input_file.seek(last_pos)
                    # no whitespace / comments left to parse
                    break
                else:
                    # read next char
                    char = self.input_file.read(1)
            continue
        return char

    def _is_alnum_or_underscore(self, char):
        return char.isalnum() or char == "_"

    def _is_string_const_delimeter(self, char):
        return char == "\""

    def _is_start_of_comment(self, char, rest_of_line):
       # comment of form: // or */
       single_line_comment = rest_of_line[0] == self.COMMENT_OPERATORS[0]
       # comment of form: /**
       multi_line_comment = char == self.COMMENT_OPERATORS[0] and rest_of_line[0:2] == "**"
       # comment of form:  * comment
       part_of_multi_line_comment = self._part_of_multiline_comment()
       return single_line_comment or multi_line_comment or part_of_multi_line_comment

    def _part_of_multiline_comment(self):
        if not self.tokens_found:
            return True
        elif self.tokens_found[-1] == ';':
            return True
        else:
            return False
