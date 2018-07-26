class CompilationEngine():
    def __init__(self, tokenizer, output_file):
        self.tokenizer = tokenizer
        self.output_file = output_file

    def compile_class(self):
        """
        everything needed to compile file class
        """
        self.output_file.write("compile!")
        self.output_file.close()
