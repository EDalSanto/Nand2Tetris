class CompilationEngine():
    """

    """
    def __init__(self, tokenizer, output_file):
        self.tokenizer = tokenizer
        self.output_file = output_file
        self.indent = 2

    def compile_class(self):
        """
        everything needed to compile file class
        """
        # get initial class token
        self.tokenizer.advance()
        # write
        self.output_file.write("<class>\n")

        while self.tokenizer.advance():
            spaces = self.indent * " "

            if self.tokenizer.identifier():
                self.output_file.write(
                    "{}<identifier>{}</identifier>\n".format(spaces, self.tokenizer.identifier())
                )
            elif self.tokenizer.symbol():
                self.output_file.write(
                    "{}<symbol>{}</symbol>\n".format(spaces, self.tokenizer.symbol())
                )

        # write closing
        self.output_file.write("</class>\n")
