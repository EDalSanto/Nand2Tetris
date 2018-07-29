class JackTokenizer():
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
            # double quotes that start string
            if char == "\"":
                self.current_token_type = "STRING_CONST"

                # get rest of string until closing "
                # skip past first "
                char = self.input_file.read(1)
                while char != "\"":
                    token += char
                    char = self.input_file.read(1)
            elif char.isalnum():
                #self.current_token_type = "
                # get full word
                while char.isalnum():
                    token += char
                    char = self.input_file.read(1)
                # go back 1 char that was peek ahead
                self.input_file.seek(self.input_file.tell() - 1)
            else:
                # else set current c as current token
                token = char

            self.current_token = token


    def current_token_type(self):
        if self.current_token in cls.KEYWORDS:
            return "KEYWORD"
        elif self.current_token in cls.SYMBOLS:
            return "SYMBOLS"
        elif self.current_token.isdigit():
            return "INT_CONSTANT"
#        elif
