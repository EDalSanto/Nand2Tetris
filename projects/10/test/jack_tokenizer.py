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
        # it gets the first token
        tokenizer.advance()
        self.assertEqual('if', tokenizer.current_token)
        # it gets the second token
        tokenizer.advance()
        self.assertEqual('(', tokenizer.current_token)
        # it gets the third token
        tokenizer.advance()
        self.assertEqual('x', tokenizer.current_token)
        # it gets the fourth token
        tokenizer.advance()
        self.assertEqual('<', tokenizer.current_token)
        # it gets the fifth token
        tokenizer.advance()
        self.assertEqual('0', tokenizer.current_token)
        # it gets the sixth token
        tokenizer.advance()
        self.assertEqual(')', tokenizer.current_token)
        # it gets the seventh token
        tokenizer.advance()
        self.assertEqual('{', tokenizer.current_token)


if __name__ == "__main__":
    unittest.main()
