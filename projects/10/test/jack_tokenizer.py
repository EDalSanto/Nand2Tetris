import unittest
from io import StringIO

# add source files to path
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from source.JackTokenizer import JackTokenizer

class TestJackTokenizer(unittest.TestCase):
    # setup input_file and source
    source_code = """\
    if (x < 0) {
        let state = "negative";
    }"""
    input_file = StringIO()
    input_file.write(source_code)
    input_file.seek(0)

    def test_advance(self):
        tokenizer = JackTokenizer(self.input_file)
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

        self.assertEqual(tokens, expected_tokens)


if __name__ == "__main__":
    unittest.main()
