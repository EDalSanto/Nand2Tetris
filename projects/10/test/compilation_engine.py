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
        self.maxDiff = None
        ## IT RETURNS A COMPILED CLASS
        source_code = "class Foo {}"
        self.set_up(source_code)

        expected_compiled = (
            "<class>\n"
            "  <keyword> class </keyword>\n"
            "  <identifier> Foo </identifier>\n"
            "  <symbol> { </symbol>\n"
            "  <symbol> } </symbol>\n"
            "</class>\n"
        )
        self.assertEqual(self.output_file.read(), expected_compiled)

        ## IT RETURNS A COMPILED CLASS WITH CLASS VARIABLE
        source_code = (
            "class Foo {\n"
            "  static boolean test;\n"
            "}\n"
        )
        self.set_up(source_code)

        expected_compiled = (
            "<class>\n"
            "  <keyword> class </keyword>\n"
            "  <identifier> Foo </identifier>\n"
            "  <symbol> { </symbol>\n"
            "  <classvarDec>\n"
            "    <keyword> static </keyword>\n"
            "    <keyword> boolean </keyword>\n"
            "    <identifier> test </identifier>\n"
            "    <symbol> ; </symbol>\n"
            "  </classvarDec>\n"
            "  <symbol> } </symbol>\n"
            "</class>\n"
        )
        self.assertEqual(self.output_file.read(), expected_compiled)

        ## IT RETURNS A COMPILED CLASS WITH A CLASS VAR AND FUNCTION
        source_code = (
            "class Foo {\n"
            "  static boolean test;\n"
            "\n"
            "  function void main(int x) {\n"
            "    var SquareGame game;\n"
            "    let game = game;\n"
            "    do game.run();\n"
            "    return;\n"
            "  }\n"
            "}\n"
        )
        self.set_up(source_code)

        expected_compiled = (
            "<class>\n"
            "  <keyword> class </keyword>\n"
            "  <identifier> Foo </identifier>\n"
            "  <symbol> { </symbol>\n"
            "  <classvarDec>\n"
            "    <keyword> static </keyword>\n"
            "    <keyword> boolean </keyword>\n"
            "    <identifier> test </identifier>\n"
            "    <symbol> ; </symbol>\n"
            "  </classvarDec>\n"
            "  <subroutineDec>\n"
            "    <keyword> function </keyword>\n"
            "    <keyword> void </keyword>\n"
            "    <identifier> main </identifier>\n"
            "    <symbol> ( </symbol>\n"
            "    <parameterList>\n"
            "      <keyword> int </keyword>\n"
            "      <identifier> x </identifier>\n"
            "    </parameterList>\n"
            "    <symbol> ) </symbol>\n"
            "    <subroutineBody>\n"
            "      <symbol> { </symbol>\n"
            "      <varDec>\n"
            "        <keyword> var </keyword>\n"
            "        <identifier> SquareGame </identifier>\n"
            "        <identifier> game </identifier>\n"
            "        <symbol> ; </symbol>\n"
            "      </varDec>\n"
            "      <statements>\n"
            "        <letStatement>\n"
            "          <keyword> let </keyword>\n"
            "          <identifier> game </identifier>\n"
            "          <symbol> = </symbol>\n"
            "          <expression>\n"
            "            <term>\n"
            "              <identifier> game </game>\n"
            "            </term>\n"
            "          </expression>\n"
            "          <symbol> ; </symbol>\n"
            "        </letStatement>\n"
            "        <doStatement>\n"
            "          <keyword> do </keyword>\n"
            "          <identifier> game </identifier>\n"
            "          <symbol> . </symbol>\n"
            "          <identifier> run </identifier>\n"
            "          <symbol> ( </symbol>\n"
            "          <expressionList>\n"
            "          </expressionList>\n"
            "          <symbol> ) </symbol>\n"
            "          <symbol> ; </symbol>\n"
            "        </doStatement>\n"
            "      </statements>\n"
            "      <keyword> return </keyword>\n"
            "      <symbol> ; </symbol>\n"
            "      <symbol> } </symbol>\n"
            "    </subroutineBody>\n"
            "  </subroutineDec>\n"
            "</class>\n"
        )

        self.assertEqual(self.output_file.read(), expected_compiled)


if __name__ == "__main__":
    unittest.main()
