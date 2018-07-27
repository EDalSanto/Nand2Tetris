class JackTokenizer():
    """
    goes through a .jack input file and produces a stream of tokens
    ignores all whitespace and comments
    """
    def __init__(self, input_file):
        self.input_file = input_file
        self.current_token = ""
        self.has_more_tokens = True

    def advance(self):
        if self.has_more_tokens:
            token_found = False
            self.current_token = ""

            while not token_found:
                # read 1 char
                c = self.input_file.read(1)
                # if whitespace or new line continue
                if c.isspace():
                    continue

                # if alphanumeric, add to current_token until word done
                if c.isalnum():
                    while c.isalnum():
                        self.current_token += c
                        c = self.input_file.read(1)
                else:
                    # else set current c as current token
                    self.current_token = c

                token_found = True
