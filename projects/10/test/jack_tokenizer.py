import unittest
from JackTokenizer import JackTokenizer

class TestJackTokenizer(unittest.TestCase):
    input = """\
            if (x < 0) {
                let state = "negative";
            }
            """

    def test_advance(self):
        # it gets the next token
        self.assertEqual('foo', input)

if __name__ == "__main__":
    unittest.main()
