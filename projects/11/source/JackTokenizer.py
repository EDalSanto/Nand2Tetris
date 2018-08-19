from JackToken import JackToken

class JackTokenizer():
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
            token = JackToken(self._get_string_const(starting_char=char))
        elif char.isalnum():
            token = JackToken(self._get_alnum_underscore(starting_char=char))
        else: # symbol
            token = JackToken(char)

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

        if self.current_token.is_empty():
            self.has_more_tokens = False

    def class_token_reached(self):
        if not self.current_token:
            return False
        else:
            return self.current_token.is_class()

    def null(self):
        if self.current_token.is_null():
            return self.current_token.text

    def boolean(self):
        if self.current_token.is_boolean():
            return self.current_token.text

    def keyword(self):
        if self.current_token.is_keyword():
            return self.current_token.text

    def identifier(self):
        if self.current_token.is_identifier():
            return self.current_token.text

    def string_const(self):
        if self.current_token.is_string_const():
            # remove " that denote string const
            return self.current_token.text.replace('"', '')

    def part_of_expression_list(self):
        if len(self.tokens_found) < 3:
            return False

        past_token = self.tokens_found[-3]
        return past_token.is_expression_list_delimiter() or past_token.is_expression_list_starter()

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
