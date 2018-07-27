import unittest

# add source files to path
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from source.JackTokenizer import JackTokenizer

class TestJackTokenizer(unittest.TestCase):
    source_code = """\
                  if (x < 0) {
                      let state = "negative";
                  }
                  """

    def test_advance(self):
        tokenizer = JackTokenizer(self.source_code)
        # it gets the first token
        tokenizer.advance()
        self.assertEqual('if', tokenizer.current_token)
        # it gets the second token
        tokenizer.advance()
        self.assertEqual('(', tokenizer.current_token)
        # it gets the thirdtoken
        tokenizer.advance()
        self.assertEqual('(', tokenizer.current_token)

if __name__ == "__main__":
    unittest.main()
