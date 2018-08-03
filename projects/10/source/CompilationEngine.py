class CompilationEngine():
    INDENT_SPACE_SIZE = 2
    TERMINAL_TOKEN_TYPES = [ "STRING_CONST", "INT_CONST", "IDENTIFIER", "SYMBOL"]
    TERMINAL_KEYWORDS = [ "boolean", "class" ]
    CLASS_VAR_DEC_TOKENS = [ "static", "field" ]
    SUBROUTINE_TOKENS = [ "function", "method", "constructor" ]
    TERMINATING_TOKENS = {
        'class': '}',
        'class_var_dec': ';',
        'subroutine': '}',
        'parameter_list': ')',
        'statements': '}',
        'do': ';',
        'let': ';',
        'while': ';',
        'if': ';',
        'var_dec': ';',
        'return': ';'
    }

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
        self._write_current_outer_tag(indent=indent, body="class")
        # maybe class token should already be read here to match other compileXXX?

        while self.tokenizer.current_token != self.TERMINATING_TOKENS['class']:
            self.tokenizer.advance()

            if self.tokenizer.current_token_type() in self.TERMINAL_TOKEN_TYPES:
                self._write_current_terminal_token(indent=indent)
            elif self.tokenizer.current_token in self.CLASS_VAR_DEC_TOKENS:
                self.compile_class_var_dec(indent=indent + self.INDENT_SPACE_SIZE)
            elif self.tokenizer.current_token in self.SUBROUTINE_TOKENS:
                self.compile_subroutine(indent=indent + self.INDENT_SPACE_SIZE)
            elif self.tokenizer.current_token in self.TERMINAL_KEYWORDS:
                    self._write_current_terminal_token(indent=indent)

        self._write_current_outer_tag(indent=indent, body="/class")

    def compile_class_var_dec(self, indent):
        self._write_current_outer_tag(indent=indent, body="classvarDec")
        self._write_current_terminal_token(indent=indent)

        while self.tokenizer.current_token != self.TERMINATING_TOKENS['class_var_dec']:
            self.tokenizer.advance()
            self._write_current_terminal_token(indent=indent)

        self._write_current_outer_tag(indent=indent, body="/classvarDec")

    def compile_subroutine(self, indent):
        # logic for compiling subroutine
        self._write_current_outer_tag(indent=indent, body="subroutineDec")
        self._write_current_terminal_token(indent=indent)

        while self.tokenizer.current_token != self.TERMINATING_TOKENS['subroutine']:
            self.tokenizer.advance()
            if self.tokenizer.current_token == '(':
                self.compile_parameter_list(indent + self.INDENT_SPACE_SIZE)
            elif self.tokenizer.current_token == '{':
                self.compile_subroutine_body(indent + self.INDENT_SPACE_SIZE)
            else:
                self._write_current_terminal_token(indent=indent)

        self._write_current_outer_tag(indent=indent, body="/subroutineDec")

    def compile_parameter_list(self, indent):
        self._write_current_terminal_token(indent=indent - self.INDENT_SPACE_SIZE)
        self.tokenizer.advance()
        self._write_current_outer_tag(indent=indent, body="parameterList")

        while self.tokenizer.current_token != self.TERMINATING_TOKENS['parameter_list']:
            self._write_current_terminal_token(indent=indent)
            self.tokenizer.advance()

        self._write_current_outer_tag(indent=indent, body="/parameterList")
        self._write_current_terminal_token(indent=indent - self.INDENT_SPACE_SIZE)

    def compile_subroutine_body(self, indent):
        # logic for compiling subroutine
        self._write_current_outer_tag(indent=indent, body="subroutineBody")
        self._write_current_terminal_token(indent=indent)

        while self.tokenizer.current_token != self.TERMINATING_TOKENS['subroutine']:
            self.tokenizer.advance()

            if self.tokenizer.current_token == 'var':
                self.compile_var_dec(indent + self.INDENT_SPACE_SIZE)
            elif self.tokenizer.current_token == 'return':
                self.compile_return(indent)
            else:
                self._write_current_terminal_token(indent=indent)

        self._write_current_outer_tag(indent=indent, body="/subroutineBody")

    def compile_var_dec(self, indent):
        # logic for var dec
        self._write_current_outer_tag(indent=indent, body="varDec")
        self._write_current_terminal_token(indent=indent)

        while self.tokenizer.current_token != self.TERMINATING_TOKENS['var_dec']:
            self.tokenizer.advance()
            self._write_current_terminal_token(indent=indent)

        self._write_current_outer_tag(indent=indent, body="/varDec")

    def compile_return(self, indent):
        # logic for return => prob need to add expression checker
        self._write_current_terminal_token(indent=indent)

        while self.tokenizer.current_token != self.TERMINATING_TOKENS['return']:
            self.tokenizer.advance()
            self._write_current_terminal_token(indent=indent)

    def compile_statements(self, indent):
        # logic for statements
        return

    def compile_do(self, indent):
        # logic for do
        return

    def compile_let(self, indent):
        # logic for let
        return

    def compile_while(self, indent):
        # logic for while
        return

    def compile_if(self, indent):
        # logic for if
        return

    def compile_expression(self, indent):
        # logic for expression
        return

    def compile_term(self, indent):
        # ?
        return

    def compile_expression_list(self, indent):
        # ?
        return

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


