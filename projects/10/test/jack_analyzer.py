import unittest
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from source.JackAnalyzer import JackAnalyzer

class TestJackAnalyzer(unittest.TestCase):
    def test_xml_output_file_for(self):
        # it takes a full path to a file and outputs an xml file with that name
        output = JackAnalyzer.xml_output_file_for("foo/bar/Main.jack")
        self.assertEqual(output, "foo/bar/Main.xml")

if __name__ == "__main__":
    unittest.main()
