import unittest
from io import StringIO

# add source files to path
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from source.JackTokenizer import JackTokenizer

class TestJackTokenizer(unittest.TestCase):
    def test_advance(self):
        # setup input_file and source
        source_code = """\
        if (x < 0) {
            let state = "negative";
        }"""
        input_file = StringIO()
        input_file.write(source_code)
        input_file.seek(0)
        # tokenize
        tokenizer = JackTokenizer(input_file)
#        expected_token_types?
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
            "negative",
            ";",
            "}"
        ]
        tokens = []
        while tokenizer.has_more_tokens:
            tokenizer.advance()
            if tokenizer.current_token:
                tokens.append(tokenizer.current_token)

        # test
        self.assertEqual(tokens, expected_tokens)

    def test_current_token_type(self):
        # it identifies keyword
        source_code = "if"

        input_file = StringIO()
        input_file.write(source_code)
        input_file.seek(0)

        # it works with symbol
        source_code = "{"

        # it works with INT
        source_code = 42

        # it works with STRING_CONSTANT
        source_code = "\"hi\""

        # it works with identifier
        source_code = "x"



if __name__ == "__main__":
    unittest.main()
