import unittest
from unittest.mock import patch
from io import StringIO

# add source files to path
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from source.JackAnalyzer import JackAnalyzer
from source.CompilationEngine import CompilationEngine

class TestJackAnalyzer(unittest.TestCase):
    def test_xml_output_file_for(self):
        # it takes a full path to a file and outputs an xml file with that name
        output = JackAnalyzer.xml_output_file_for("foo/bar/Main.jack")
        self.assertEqual(output, "foo/bar/Main.xml")

    def test_run(self):
        # it tells the compiler to compile class
        input_file = StringIO()
        output_file = StringIO()
        with patch.object(CompilationEngine, "compile_class", return_value=None) as mocked_method:
            JackAnalyzer.run(input_file, output_file)

        mocked_method.assert_called_once()

if __name__ == "__main__":
    unittest.main()
