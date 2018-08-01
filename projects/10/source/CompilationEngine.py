class CompilationEngine():
    """

    """
    def __init__(self, tokenizer, output_file):
        self.tokenizer = tokenizer
        self.output_file = output_file

    def compile_class(self, indent=2, terminating_token="}", outer="class", inner="class"):
        """
        everything needed to compile file class
        """
        outer_spaces = (indent - 2) * " "
        inner_spaces = indent * " "
        # write outer tag
        self.output_file.write("{}<{}>\n".format(outer_spaces, outer))
        # write inner keyword
        self.output_file.write("{}<keyword>{}</keyword>\n".format(inner_spaces, inner))

        while self.tokenizer.current_token != terminating_token:
            self.tokenizer.advance()

            if self.tokenizer.identifier():
                self.output_file.write(
                    "{}<identifier>{}</identifier>\n".format(inner_spaces, self.tokenizer.identifier())
                )
            elif self.tokenizer.symbol():
                self.output_file.write(
                    "{}<symbol>{}</symbol>\n".format(inner_spaces, self.tokenizer.symbol())
                )
            elif self.tokenizer.keyword():
                # self.compile_keyword()
                # class_var_dec
                if self.tokenizer.keyword() in [ "static", "field" ]:
                    # write outer
                    self.compile_class(indent=indent + 2, terminating_token=";", outer="classvarDec", inner=self.tokenizer.keyword())
                elif self.tokenizer.keyword() == "boolean":
                    self.output_file.write("{}<keyword>boolean</keyword>\n".format(inner_spaces))

        # write closing of outer
        self.output_file.write("{}</{}>\n".format(outer_spaces, outer))
