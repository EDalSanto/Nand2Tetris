from JackTokenizer import JackTokenizer
from CompilationEngine  import CompilationEngine
import sys
import os
import glob

class JackCompiler():
    @classmethod
    def run(cls, input_file, output_file):
        tokenizer = JackTokenizer(input_file)
        compiler = CompilationEngine(tokenizer, output_file)
        compiler.compile_class()

    @classmethod
    def output_file_for(cls, input_file, ext_name='.vm'):
        file_name = os.path.basename(input_file).split(".")[0]
        dir_name = os.path.dirname(input_file).replace('./', '')
        # create subdirectory for compiled
        try:
            os.mkdir("./compiled/{}".format(dir_name))
        except OSError:
            print("res directory already exists. continuing")

        # for testing locally
        return "./compiled/{}/{}{}".format(dir_name, file_name, ext_name)
        # actual format expected for Coursera grader
        # return dir_name + "/" + file_name + ext_name

if __name__ == "__main__" and len(sys.argv) == 2:
    arg = sys.argv[1]

    # determine output file names
    if os.path.isfile(arg):
        files = [arg]
    elif os.path.isdir(arg):
        jack_path = os.path.join(arg, "*.jack")
        files = glob.glob(jack_path)

    # create output directory - MAY NEED TO REMOVE
    try:
        os.mkdir("./compiled")
    except OSError:
        print("output directory already exists. continuing")

    for input_file_name in files:
        output_file_name = JackCompiler.output_file_for(input_file_name)
        output_file = open(output_file_name, 'w')
        input_file = open(input_file_name, 'r')
        JackCompiler.run(input_file, output_file)
