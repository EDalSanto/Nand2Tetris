import unittest
from io import StringIO

# add source files to path
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from source.JackTokenizer import JackTokenizer

class TestJackTokenizer(unittest.TestCase):
    def setUp(self):
        # setup input_file and source
        source_code = """\
        if (x < 0) {
            let state = "negative";
        }"""
        input_file = StringIO()
        input_file.write(source_code)
        input_file.seek(0)
        # tokenize
        self.tokenizer = JackTokenizer(input_file)

    def test_advance(self):
        ## IT TOKENIZES INPUT
        expected_tokens = [
            "if",
            "(",
            "x",
            "<",
            "0",
            ")",
            "{",
            "let",
            "state",
            "=",
            "\"negative\"",
            ";",
            "}"
        ]
        tokens = []
        while self.tokenizer.has_more_tokens:
            self.tokenizer.advance()
            if self.tokenizer.current_token:
                tokens.append(self.tokenizer.current_token)

        self.assertEqual(tokens, expected_tokens)

    def test_current_token_type(self):
        expected_token_types = [
            "KEYWORD",
            "SYMBOL",
            "IDENTIFIER",
            "SYMBOL",
            "INT_CONST",
            "SYMBOL",
            "SYMBOL",
            "KEYWORD",
            "IDENTIFIER",
            "SYMBOL",
            "STRING_CONST",
            "SYMBOL",
            "SYMBOL"
        ]
        token_types = []
        while self.tokenizer.has_more_tokens:
            self.tokenizer.advance()
            if self.tokenizer.current_token:
                token_types.append(self.tokenizer.current_token_type())

        self.assertEqual(token_types, expected_token_types)


if __name__ == "__main__":
    unittest.main()
