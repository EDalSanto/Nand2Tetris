import unittest
from io import StringIO

# add source files to path
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from source.JackTokenizer import JackTokenizer
from source.CompilationEngine import CompilationEngine

class TestCompilationEngine(unittest.TestCase):
    def set_up(self, source_code):
        input_file = StringIO()
        input_file.write(source_code)
        input_file.seek(0)
        self.tokenizer = JackTokenizer(input_file)
        self.output_file = StringIO()
        self.compilation_engine = CompilationEngine(self.tokenizer, self.output_file)
        self.compilation_engine.compile_class()
        self.output_file.seek(0)

    def test_compile_class(self):
        ## IT RETURNS A COMPILED CLASS
        source_code = "class Foo {}"
        self.set_up(source_code)

        expected_compiled = (
            "<class>\n"
            "  <identifier>Foo</identifier>\n"
            "  <symbol>{</symbol>\n"
            "  <symbol>}</symbol>\n"
            "</class>\n"
        )
        self.assertEqual(self.output_file.read(), expected_compiled)

if __name__ == "__main__":
    unittest.main()
