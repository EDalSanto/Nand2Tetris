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
        self.current_token = ""
        self.current_token_type = None
        self.has_more_tokens = True

    def advance(self):
        if self.has_more_tokens:
            char = self.input_file.read(1)

            # guard clause to check if done
            if not char:
                self.has_more_tokens = False
                self.current_token = None
                return

            # skip all whitespace
            while char.isspace():
                char = self.input_file.read(1)
                continue

            # process found token
            token = ""
            # double quotes that start string const
            if char == "\"":
                token += char
                char = self.input_file.read(1)

                while char != "\"":
                    token += char
                    char = self.input_file.read(1)

                # get last "
                token += char

                self.current_token_type = "STRING_CONST"
            elif char.isalnum():
                # get full word -> alnum or underscore
                while char.isalnum() or char == "_":
                    token += char
                    char = self.input_file.read(1)
                # go back 1 char that was peek ahead
                self.input_file.seek(self.input_file.tell() - 1)

                # set current token type
                if token in self.KEYWORDS:
                    self.current_token_type = "KEYWORD"
                elif token[0].isnumeric():
                    self.current_token_type = "INT_CONST"
                else:
                    self.current_token_type = "IDENTIFIER"
            else:
                # else set current c as current token
                token = char
                self.current_token_type = "SYMBOL"

            self.current_token = token

