class JackTokenizer():
    """
    goes through a .jack input file and produces a stream of tokens
    ignores all whitespace and comments
    """
    def __init__(self, input_file):
        self.input_file = input_file
        self.current_token = None
        self.has_more_tokens = True

    def advance(self):
        return
