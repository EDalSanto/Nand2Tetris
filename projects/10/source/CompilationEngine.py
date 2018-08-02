class CompilationEngine():
    INDENT_SPACE_SIZE = 2
    TERMINAL_TOKEN_TYPES = [ "STRING_CONST", "INT_CONST", "IDENTIFIER", "SYMBOL"]
    NON_TERMINAL_TOKEN_TYPES = [ "KEYWORD" ]
    TERMINAL_KEYWORDS = [ "boolean", "class" ]
    CLASS_VAR_DEC_TOKENS = [ "static", "field" ]

    """
    compiles a jack source file from a jack tokenizer into xml form in output_file
    """

    def __init__(self, tokenizer, output_file):
        self.tokenizer = tokenizer
        self.output_file = output_file

    def compile_class(self, indent=2):
        """
        everything needed to compile a class, the basic unit of compilation
        """
        terminating_token = "}"
        self._write_current_outer_tag(indent=indent, body="class")
        # maybe class token should already be read here to match other compileXXX?

        while self.tokenizer.current_token != terminating_token:
            self.tokenizer.advance()

            if self.tokenizer.current_token_type() in self.TERMINAL_TOKEN_TYPES:
                self._write_current_terminal_token(indent=indent)
            elif self.tokenizer.current_token_type() in self.NON_TERMINAL_TOKEN_TYPES:
                if self.tokenizer.current_token in self.CLASS_VAR_DEC_TOKENS:
                    self.compile_class_var_dec(indent=indent + self.INDENT_SPACE_SIZE)
                elif self.tokenizer.current_token in self.TERMINAL_KEYWORDS:
                    self._write_current_terminal_token(indent=indent)

        self._write_current_outer_tag(indent=indent, body="/class")

    def compile_class_var_dec(self, indent):
        terminating_token = ";"
        self._write_current_outer_tag(indent=indent, body="classvarDec")
        self._write_current_terminal_token(indent=indent)

        while self.tokenizer.current_token != terminating_token:
            self.tokenizer.advance()
            self._write_current_terminal_token(indent=indent)

        self._write_current_outer_tag(indent=indent, body="/classvarDec")

    def compile_subroutine(self, indent):
        terminating_token = "}"
        # logic for subroutine

    def compile_parameter_list(self, indent):
        terminating_token = ")"
        # logic for paramter list

    def compile_var_dec(self, indent):
        terminating_token = ";"
        # logic for var dec

    def compile_statements(self, indent):
        terminating_token = "}"
        # logic for statements

    def compile_do(self, indent):
        terminating_token = ";"
        # logic for do

    def compile_let(self, indent):
        terminating_token = ";"
        # logic for let

    def compile_while(self, indent):
        terminating_token = "}"
        # logic for while

    def compile_return(self, indent):
        terminating_token = ";"
        # logic for return

    def compile_if(self, indent):
        terminating_token = ";"
        # logic for if

    def compile_expression(self, indent):
        terminating_token = "?"
        # logic for expression

    def compile_term(self, indent):
        # ?

    def compile_expression_list(self, indent):
        # ?

    def _write_current_outer_tag(self, indent, body):
        spaces = (indent - self.INDENT_SPACE_SIZE) * " "
        self.output_file.write("{}<{}>\n".format(spaces, body))


    def _write_current_terminal_token(self, indent):
       spaces = indent * " "

       self.output_file.write(
           "{}<{}>{}</{}>\n".format(
               spaces,
               self.tokenizer.current_token_type().lower(),
               self.tokenizer.current_token,
               self.tokenizer.current_token_type().lower()
           )
       )


