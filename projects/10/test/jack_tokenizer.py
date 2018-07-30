import unittest
from io import StringIO

# add source files to path
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from source.JackTokenizer import JackTokenizer

class TestJackTokenizer(unittest.TestCase):
    def test_advance(self):
        ## IT TOKENIZES INPUT

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
            "\"negative\"",
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

        ## IT SETS THE CURRENT TOKEN TYPE
        source_code = "if { 42 \"hi\" x"

        input_file = StringIO()
        input_file.write(source_code)
        input_file.seek(0)

        tokenizer = JackTokenizer(input_file)

        # it works with keyword
        tokenizer.advance()
        self.assertEqual(tokenizer.current_token_type, "KEYWORD")

        # it works with symbol
        tokenizer.advance()
        self.assertEqual(tokenizer.current_token_type, "SYMBOL")

        # it works with INT
        tokenizer.advance()
        self.assertEqual(tokenizer.current_token_type, "INT_CONST")

        # it works with STRING_CONSTANT
        tokenizer.advance()
        self.assertEqual(tokenizer.current_token_type, "STRING_CONST")

        # it works with identifier
        tokenizer.advance()
        self.assertEqual(tokenizer.current_token_type, "IDENTIFIER")

if __name__ == "__main__":
    unittest.main()
