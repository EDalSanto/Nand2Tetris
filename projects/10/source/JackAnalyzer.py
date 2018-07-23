from JackTokenizer import *
import sys
import os
import glob

class JackAnalyzer():
    @classmethod
    def run(cls, input):
        if os.path.isfile(input):
            files = [input]
        elif os.path.isdir(input):
            jack_path = os.path.join(input, "*.jack")
            files = glob.glob(jack_path)

        for file in files:
            tokenizer = JackTokenizer(input)
            output_file = cls.output_file_for(input)
            compiler = CompilationEngine(tokenizer, output_file)
            compiler.compile_class()


    @classmethod
    def output_file_for(cls, file):
        file_name = os.path.basename(file).split(".")[0]
        ext_name = ".xml"
        dir_name = os.path.dirname(file)
        import pdb; pdb.set_trace();
        return dir_name + "/" + file_name + ext_name


if __name__ == "__main__" and len(sys.argv) == 2:
    input = sys.argv[1]
    JackAnalyzer.run(input)