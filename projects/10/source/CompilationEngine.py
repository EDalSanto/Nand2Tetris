class CompilationEngine():
    INDENT_SPACE_SIZE = 2
    TERMINAL_TOKEN_TYPES = [ "STRING_CONST", "INT_CONST", "IDENTIFIER", "SYMBOL"]
    TERMINAL_KEYWORDS = [ "boolean", "class", "void", "int" ]
    CLASS_VAR_DEC_TOKENS = [ "static", "field" ]
    SUBROUTINE_TOKENS = [ "function", "method", "constructor" ]
    STATEMENT_TOKENS = [ 'do', 'let', 'while', 'return', 'if' ]
    STARTING_TOKENS = {
        'var_dec': 'var',
        'parameter_list': '(',
        'subroutine_body': '{',
        'expression_list': '(',
        'expression': '='
    }
    TERMINATING_TOKENS = {
        'class': '}',
        'class_var_dec': ';',
        'subroutine': '}',
        'parameter_list': ')',
        'expression_list': ')',
        'statements': '}',
        'do': ';',
        'let': ';',
        'while': '}',
        'if': '}',
        'var_dec': ';',
        'return': ';',
        'expression': [';', ')']
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

        while self.tokenizer.has_more_tokens:
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
        self._write_current_outer_tag(indent=indent, body="classVarDec")
        self._write_current_terminal_token(indent=indent)

        while self.tokenizer.current_token != self.TERMINATING_TOKENS['class_var_dec']:
            self.tokenizer.advance()
            self._write_current_terminal_token(indent=indent)

        self._write_current_outer_tag(indent=indent, body="/classVarDec")

    def compile_subroutine(self, indent):
        self._write_current_outer_tag(indent=indent, body="subroutineDec")
        self._write_current_terminal_token(indent=indent)

        while self.tokenizer.current_token != self.TERMINATING_TOKENS['subroutine']:
            self.tokenizer.advance()

            if self.tokenizer.current_token == self.STARTING_TOKENS['parameter_list']:
                self.compile_parameter_list(indent + self.INDENT_SPACE_SIZE)
            elif self.tokenizer.current_token == self.STARTING_TOKENS['subroutine_body']:
                self.compile_subroutine_body(indent + self.INDENT_SPACE_SIZE)
            else:
                self._write_current_terminal_token(indent=indent)

        self._write_current_outer_tag(indent=indent, body="/subroutineDec")

    def compile_parameter_list(self, indent):
        # write starting (
        self._write_current_terminal_token(indent=indent - self.INDENT_SPACE_SIZE)
        self._write_current_outer_tag(indent=indent, body="parameterList")

        while self.tokenizer.next_token != self.TERMINATING_TOKENS['parameter_list']:
            self.tokenizer.advance()
            self._write_current_terminal_token(indent=indent)

        self._write_current_outer_tag(indent=indent, body="/parameterList")
        # advance to closing )
        self.tokenizer.advance()
        # write closing )
        self._write_current_terminal_token(indent=indent - self.INDENT_SPACE_SIZE)

    def compile_subroutine_body(self, indent):
        self._write_current_outer_tag(indent=indent, body="subroutineBody")
        # write opening {
        self._write_current_terminal_token(indent=indent)

        while self.tokenizer.current_token != self.TERMINATING_TOKENS['subroutine']:
            self.tokenizer.advance()

            if self.tokenizer.current_token == self.STARTING_TOKENS['var_dec']:
                self.compile_var_dec(indent=indent + self.INDENT_SPACE_SIZE)
            elif self.tokenizer.current_token in self.STATEMENT_TOKENS:
                self.compile_statements(indent=indent + self.INDENT_SPACE_SIZE)
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

    def compile_statements(self, indent):
        self._write_current_outer_tag(indent=indent, body="statements")

        # statements last thing expected by compiler in subroutine
        while self.tokenizer.current_token != self.TERMINATING_TOKENS['subroutine']:
            if self.tokenizer.current_token == "if":
                self.compile_if(indent=indent + self.INDENT_SPACE_SIZE)
            elif self.tokenizer.current_token == "do":
                self.compile_do(indent=indent + self.INDENT_SPACE_SIZE)
            elif self.tokenizer.current_token == "let":
                self.compile_let(indent=indent + self.INDENT_SPACE_SIZE)
            elif self.tokenizer.current_token == "while":
                self.compile_while(indent=indent + self.INDENT_SPACE_SIZE)
            elif self.tokenizer.current_token == "return":
                self.compile_return(indent=indent + self.INDENT_SPACE_SIZE)

            self.tokenizer.advance()

        self._write_current_outer_tag(indent=indent+self.INDENT_SPACE_SIZE, body="/statements")
        self._write_current_terminal_token(indent=indent)

    def compile_do(self, indent):
        self._write_current_outer_tag(indent=indent, body="doStatement")
        self._write_current_terminal_token(indent=indent)

        while self.tokenizer.current_token != self.TERMINATING_TOKENS['do']:
            self.tokenizer.advance()

            if self.tokenizer.current_token == self.STARTING_TOKENS['expression_list']:
                self._write_current_terminal_token(indent=indent)
                self.compile_expression_list(indent=indent+self.INDENT_SPACE_SIZE)
            else:
                self._write_current_terminal_token(indent=indent)

        self._write_current_outer_tag(indent=indent, body="/doStatement")

    def compile_let(self, indent):
        self._write_current_outer_tag(indent=indent, body="letStatement")
        self._write_current_terminal_token(indent=indent)

        while self.tokenizer.current_token != self.TERMINATING_TOKENS['let']:
            self.tokenizer.advance()

            if self.tokenizer.current_token == self.STARTING_TOKENS['expression']:
                self._write_current_terminal_token(indent=indent)
                self.compile_expression(indent=indent+self.INDENT_SPACE_SIZE)
            else:
                self._write_current_terminal_token(indent=indent)

        self._write_current_outer_tag(indent=indent, body="/letStatement")

    def compile_while(self, indent):
        self._write_current_outer_tag(indent=indent, body="whileStatement")
        # write keyword while
        self._write_current_terminal_token(indent=indent)
        # compile expression in ()
        self.tokenizer.advance()
        self._write_current_terminal_token(indent=indent)
        self.compile_expression(indent=indent+self.INDENT_SPACE_SIZE)

        while self.tokenizer.current_token != self.TERMINATING_TOKENS['while']:
            self.tokenizer.advance()

            if self.tokenizer.current_token in self.STATEMENT_TOKENS:
                self.compile_statements(indent=indent)
            else:
                self._write_current_terminal_token(indent=indent)

        self._write_current_outer_tag(indent=indent, body="/whileStatement")

    def compile_if(self, indent):
        self._write_current_outer_tag(indent=indent, body="ifStatement")
        # write keyword if
        self._write_current_terminal_token(indent=indent)
        # compile expression in ()
        self.tokenizer.advance()
        self._write_current_terminal_token(indent=indent)
        self.compile_expression(indent=indent+self.INDENT_SPACE_SIZE)

        while self.tokenizer.current_token != self.TERMINATING_TOKENS['if']:
            self.tokenizer.advance()

            if self.tokenizer.current_token in self.STATEMENT_TOKENS:
                self.compile_statements(indent=indent)
            else:
                self._write_current_terminal_token(indent=indent)

        self._write_current_outer_tag(indent=indent, body="/ifStatement")

    def compile_return(self, indent):
        self._write_current_outer_tag(indent=indent, body="returnStatement")
        # write return
        self._write_current_terminal_token(indent=indent)

        if self.tokenizer.next_token != self.TERMINATING_TOKENS['return']:
            # expression
            self.compile_expression(indent=indent + self.INDENT_SPACE_SIZE)
        else: # write ; for void
            self.tokenizer.advance()
            self._write_current_terminal_token(indent=indent)

        # write end
        self._write_current_outer_tag(indent=indent, body="/returnStatement")

    def compile_expression(self, indent):
        self._write_current_outer_tag(indent=indent, body="expression")

        while self.tokenizer.next_token not in self.TERMINATING_TOKENS['expression']:
            self.tokenizer.advance()
            self.compile_term(indent=indent+self.INDENT_SPACE_SIZE)

        self._write_current_outer_tag(indent=indent, body="/expression")
        # write terminal token
        self.tokenizer.advance()
        self._write_current_terminal_token(indent=indent - self.INDENT_SPACE_SIZE)

    def compile_term(self, indent):
        if self.tokenizer.current_token_type() == 'SYMBOL':
            self._write_current_terminal_token(indent=indent)
        else:
            self._write_current_outer_tag(indent=indent, body="term")
            self._write_current_terminal_token(indent=indent)
            self._write_current_outer_tag(indent=indent, body="/term")

    def compile_expression_list(self, indent):
        self._write_current_outer_tag(indent=indent, body="expressionList")

        while self.tokenizer.next_token != self.TERMINATING_TOKENS['expression_list']:
            self.tokenizer.advance()

            if self.tokenizer.current_token == ",":
                self._write_current_terminal_token(indent=indent)
            else: # expression
                self._write_current_outer_tag(indent=indent + self.INDENT_SPACE_SIZE, body="expression")

                # should be look ahead or another expression terminator
                self.compile_term(indent=indent+self.INDENT_SPACE_SIZE+self.INDENT_SPACE_SIZE)

                self._write_current_outer_tag(indent=indent + self.INDENT_SPACE_SIZE, body="/expression")


        self._write_current_outer_tag(indent=indent, body="/expressionList")
        # write terminal token
        self.tokenizer.advance()
        self._write_current_terminal_token(indent=indent - self.INDENT_SPACE_SIZE)

    def _write_current_outer_tag(self, indent, body):
        spaces = (indent - self.INDENT_SPACE_SIZE) * " "
        self.output_file.write("{}<{}>\n".format(spaces, body))


    def _write_current_terminal_token(self, indent):
       spaces = indent * " "

       self.output_file.write(
           "{}<{}> {} </{}>\n".format(
               spaces,
               self.tokenizer.current_token_type().lower(),
               self.tokenizer.current_token,
               self.tokenizer.current_token_type().lower()
           )
       )


