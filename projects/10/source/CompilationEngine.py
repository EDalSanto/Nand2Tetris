class CompilationEngine():
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
        'expression': ['=', '[', '(']
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
        'expression': [';', ')', ']', ',']
    }
    OPERATORS = [
        '+',
        '-',
        '*',
        '/',
        '&amp;',
        '|',
        '&lt;',
        '&gt;',
        '='
    ]
    UNARY_OPERATORS = [ '-', '~' ]

    """
    compiles a jack source file from a jack tokenizer into xml form in output_file
    """

    def __init__(self, tokenizer, output_file):
        self.tokenizer = tokenizer
        self.output_file = output_file

    def compile_class(self):
        """
        everything needed to compile a class, the basic unit of compilation
        """
        self._write_current_outer_tag(body="class")

        while self.tokenizer.has_more_tokens:
            self.tokenizer.advance()

            if self.tokenizer.current_token_type() in self.TERMINAL_TOKEN_TYPES or self.tokenizer.current_token in self.TERMINAL_KEYWORDS:
                self._write_current_terminal_token()
            elif self.tokenizer.current_token in self.CLASS_VAR_DEC_TOKENS:
                self.compile_class_var_dec()
            elif self.tokenizer.current_token in self.SUBROUTINE_TOKENS:
                self.compile_subroutine()

        self._write_current_outer_tag(body="/class")

    def compile_class_var_dec(self):
        self._write_current_outer_tag(body="classVarDec")
        self._write_current_terminal_token()

        while self.tokenizer.current_token != self.TERMINATING_TOKENS['class_var_dec']:
            self.tokenizer.advance()
            self._write_current_terminal_token()

        self._write_current_outer_tag(body="/classVarDec")

    def compile_subroutine(self):
        self._write_current_outer_tag(body="subroutineDec")
        self._write_current_terminal_token()

        while self.tokenizer.current_token != self.TERMINATING_TOKENS['subroutine']:
            self.tokenizer.advance()

            if self.tokenizer.current_token == self.STARTING_TOKENS['parameter_list']:
                self.compile_parameter_list()
            elif self.tokenizer.current_token == self.STARTING_TOKENS['subroutine_body']:
                self.compile_subroutine_body()
            else:
                self._write_current_terminal_token()

        self._write_current_outer_tag(body="/subroutineDec")

    def compile_parameter_list(self):
        # write starting (
        self._write_current_terminal_token()
        self._write_current_outer_tag(body="parameterList")

        while not self.tokenizer.next_token == self.TERMINATING_TOKENS['parameter_list']:
            self.tokenizer.advance()
            self._write_current_terminal_token()

        self._write_current_outer_tag(body="/parameterList")
        # advance to closing )
        self.tokenizer.advance()
        # write closing )
        self._write_current_terminal_token()

    # '{' varDec* statements '}'
    def compile_subroutine_body(self):
        self._write_current_outer_tag(body="subroutineBody")
        # write opening {
        self._write_current_terminal_token()

        while not self.tokenizer.current_token == self.TERMINATING_TOKENS['subroutine']:
            self.tokenizer.advance()

            if self.tokenizer.current_token == self.STARTING_TOKENS['var_dec']:
                self.compile_var_dec()
            elif self.tokenizer.current_token in self.STATEMENT_TOKENS:
                self.compile_statements()
            else:
                self._write_current_terminal_token()

        # write closing }
        self._write_current_terminal_token()
        self._write_current_outer_tag(body="/subroutineBody")

    # 'var' type varName (',' varName)* ';'
    def compile_var_dec(self):
        self._write_current_outer_tag(body="varDec")
        self._write_current_terminal_token()

        while not self.tokenizer.current_token == self.TERMINATING_TOKENS['var_dec']:
            self.tokenizer.advance()
            self._write_current_terminal_token()

        self._write_current_outer_tag(body="/varDec")

    def compile_statements(self):
        self._write_current_outer_tag(body="statements")

        while not self.tokenizer.current_token == self.TERMINATING_TOKENS['subroutine']:
            if self.tokenizer.current_token == "if":
                self.compile_if()
            elif self.tokenizer.current_token == "do":
                self.compile_do()
            elif self.tokenizer.current_token == "let":
                self.compile_let()
            elif self.tokenizer.current_token == "while":
                self.compile_while()
            elif self.tokenizer.current_token == "return":
                self.compile_return()

            self.tokenizer.advance()

        self._write_current_outer_tag(body="/statements")

    def compile_do(self):
        self._write_current_outer_tag(body="doStatement")
        self._write_current_terminal_token()

        while not self.tokenizer.current_token == self.TERMINATING_TOKENS['do']:
            self.tokenizer.advance()

            if self.tokenizer.current_token == self.STARTING_TOKENS['expression_list']:
                self.compile_expression_list()
            else:
                self._write_current_terminal_token()

        self._write_current_outer_tag(body="/doStatement")

    # 'let' varName ('[' expression ']')? '=' expression ';'
    def compile_let(self):
        self._write_current_outer_tag(body="letStatement")
        # write let keyword
        self._write_current_terminal_token()

        while not self.tokenizer.current_token == self.TERMINATING_TOKENS['let']:
            self.tokenizer.advance()

            if self.tokenizer.current_token in self.STARTING_TOKENS['expression']:
                # write =
                self._write_current_terminal_token()
                self.compile_expression()
            else:
                self._write_current_terminal_token()

        self._write_current_outer_tag(body="/letStatement")

    # 'while' '(' expression ')' '{' statements '}'
    def compile_while(self):
        self._write_current_outer_tag(body="whileStatement")
        # write keyword while
        self._write_current_terminal_token()

        # write (
        self.tokenizer.advance()
        self._write_current_terminal_token()

        # compile expression in ()
        self.compile_expression()

        while not self.tokenizer.current_token == self.TERMINATING_TOKENS['while']:
            self.tokenizer.advance()

            if self.tokenizer.current_token in self.STATEMENT_TOKENS:
                self.compile_statements()
            else:
                self._write_current_terminal_token()
        # write terminal token
        self._write_current_terminal_token()

        self._write_current_outer_tag(body="/whileStatement")

    def compile_if(self):
        self._write_current_outer_tag(body="ifStatement")
        # write keyword if
        self._write_current_terminal_token()

        # write (
        self.tokenizer.advance()
        self._write_current_terminal_token()

        # compile expression in ()
        self.compile_expression()

        while not self.tokenizer.current_token == self.TERMINATING_TOKENS['if']:
            self.tokenizer.advance()

            if self.tokenizer.current_token in self.STATEMENT_TOKENS:
                self.compile_statements()
            else:
                self._write_current_terminal_token()

        # compile else
        if self.tokenizer.next_token == "else":
            self._write_current_terminal_token()
            # skip closing {
            self.tokenizer.advance()
            # write else
            self._write_current_terminal_token()
            while not self.tokenizer.current_token == self.TERMINATING_TOKENS['if']:
                self.tokenizer.advance()

                if self.tokenizer.current_token in self.STATEMENT_TOKENS:
                    self.compile_statements()
                else:
                    self._write_current_terminal_token()

        # write terminal token
        self._write_current_terminal_token()
        self._write_current_outer_tag(body="/ifStatement")

    # term (op term)*
    def compile_expression(self):
        self._write_current_outer_tag(body="expression")

        # check starting
        if self.tokenizer.current_token == "(" and self.tokenizer.next_token == "-":
            unary_negative = True
        else:
            unary_negative = False
        self.tokenizer.advance()

        while self.tokenizer.current_token not in self.TERMINATING_TOKENS['expression']:
            if self.tokenizer.current_token in self.OPERATORS and not unary_negative:
                self._write_current_terminal_token()
                self.tokenizer.advance()
            else:
                self.compile_term()

        self._write_current_outer_tag(body="/expression")
        self._write_current_terminal_token()

    def compile_expression_in_expression_list(self):
        self._write_current_outer_tag(body="expression")

        # go till , or (
        while self.tokenizer.current_token not in self.TERMINATING_TOKENS['expression']:
            if self.tokenizer.current_token in [',']:
                self.tokenizer.advance()

            if self.tokenizer.current_token in self.OPERATORS:
                self._write_current_terminal_token()
                self.tokenizer.advance()
            else:
                self.compile_term()

        self._write_current_outer_tag(body="/expression")
        # only write , if multiple
        if self.tokenizer.current_token == ",":
            self._write_current_terminal_token()
            self.tokenizer.advance() # advance here to avoid next check

    # (expression (',' expression)* )?
    def compile_expression_list(self):
        # write (
        self._write_current_terminal_token()
        self._write_current_outer_tag(body="expressionList")

        # skip initial (
        self.tokenizer.advance()

        if not self.tokenizer.current_token == self.TERMINATING_TOKENS['expression_list']:
            while not self.tokenizer.current_token == self.TERMINATING_TOKENS['expression_list']:
                self.compile_expression_in_expression_list()
        # write )
        self._write_current_outer_tag(body="/expressionList")
        self._write_current_terminal_token()

    # integerConstant | stringConstant | keywordConstant | varName |
    # varName '[' expression']' | subroutineCall | '(' expression ')' | unaryOp term
    def compile_term(self):
        self._write_current_outer_tag(body="term")

        while self.tokenizer.current_token not in self.TERMINATING_TOKENS['expression']:
            if self.tokenizer.current_token == self.STARTING_TOKENS['expression_list']:
                if self.tokenizer.part_of_subroutine_call():
                    self.compile_expression_list()
                else: # expression
                    # write starting
                    self._write_current_terminal_token()
                    self.compile_expression()
            elif self.tokenizer.current_token in self.STARTING_TOKENS['expression']:
                # write starting
                self._write_current_terminal_token()
                self.compile_expression()
            elif self.tokenizer.current_token in self.UNARY_OPERATORS:
                self._write_current_terminal_token()

                if self.tokenizer.next_token in self.STARTING_TOKENS['expression']:
                    self.tokenizer.advance()
                    self.compile_term()
                    break
                else:
                    # write inner term - ghetto
                    self.tokenizer.advance()
                    self._write_current_outer_tag(body="term")
                    self._write_current_terminal_token()
                    self._write_current_outer_tag(body="/term")
            else:
                self._write_current_terminal_token()

            # remove ghetto
            # if next token is op and prev isn't start of expression symbol
            if self.tokenizer.next_token in self.OPERATORS and self.tokenizer.current_token != '(':
                self.tokenizer.advance()
                break

            self.tokenizer.advance()

        self._write_current_outer_tag(body="/term")

    def compile_return(self):
        self._write_current_outer_tag(body="returnStatement")

        # write return
        self._write_current_terminal_token()
#        self.tokenizer.advance()

        if not self.tokenizer.next_token == self.TERMINATING_TOKENS['return']:
            self.compile_expression()
        else: # write ; for void
            self.tokenizer.advance()
            self._write_current_terminal_token()

        # write end
        self._write_current_outer_tag(body="/returnStatement")


    def _write_current_outer_tag(self, body):
        self.output_file.write("<{}>\n".format(body))


    def _write_current_terminal_token(self):
       if self.tokenizer.current_token_type() == "STRING_CONST":
           tag_name = "stringConstant"
       elif self.tokenizer.current_token_type() == "INT_CONST":
           tag_name = "integerConstant"
       else:
            tag_name = self.tokenizer.current_token_type().lower()

       if self.tokenizer.current_token_type() == "STRING_CONST":
           value = self.tokenizer.current_token.replace("\"", "")
       else:
           value = self.tokenizer.current_token

       self.output_file.write(
           "<{}> {} </{}>\n".format(
               tag_name,
               value,
               tag_name
           )
       )


