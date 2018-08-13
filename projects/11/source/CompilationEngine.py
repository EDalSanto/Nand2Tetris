from SymbolTable import SymbolTable
from VMWriter import VMWriter

class CompilationEngine():
    """
    compiles a jack source file from a jack tokenizer into xml form in output_file
    """

    TERMINAL_TOKEN_TYPES = [ "STRING_CONST", "INT_CONST", "IDENTIFIER", "SYMBOL"]
    TERMINAL_KEYWORDS = [ "boolean", "class", "void", "int" ]
    CLASS_VAR_DEC_TOKENS = [ "static", "field" ]
    SUBROUTINE_TOKENS = [ "function", "method", "constructor" ]
    STATEMENT_TOKENS = [ 'do', 'let', 'while', 'return', 'if' ]
    STARTING_TOKENS = {
        'var_dec': ['var'],
        'parameter_list': ['('],
        'subroutine_body': ['{'],
        'expression_list': ['('],
        'expression': ['=', '[', '(']
    }
    TERMINATING_TOKENS = {
        'class': ['}'],
        'class_var_dec': [';'],
        'subroutine': ['}'],
        'parameter_list': [')'],
        'expression_list': [')'],
        'statements': ['}'],
        'do': [';'],
        'let': [';'],
        'while': ['}'],
        'if': ['}'],
        'var_dec': [';'],
        'return': [';'],
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

    def __init__(self, tokenizer, output_file):
        self.tokenizer = tokenizer
        self.output_file = output_file
        self.class_symbol_table = SymbolTable()
        self.subroutine_symbol_table = SymbolTable()
        self.vm_writer = VMWriter(output_file)

    def compile_class(self):
        """
        everything needed to compile a class, the basic unit of compilation
        """

        while self.tokenizer.has_more_tokens:
            self.tokenizer.advance()

            if self.tokenizer.identifier():
                class_name = self.tokenizer.identifier()
            elif self.tokenizer.current_token in self.CLASS_VAR_DEC_TOKENS:
                self.compile_class_var_dec()
            elif self.tokenizer.current_token in self.SUBROUTINE_TOKENS:
                self.compile_subroutine(class_name)

    def compile_class_var_dec(self):
        """
        example: field int x;
        """
        ### symbol table
        kind = self.tokenizer.current_token

        # get symbol type
        self.tokenizer.advance()
        symbol_type = self.tokenizer.keyword()

        # get all identifiers
        while self._not_terminal_token_for('class_var_dec'):
            self.tokenizer.advance()
            if self.tokenizer.identifier():
                # add symbol to class
                name = self.tokenizer.identifier()
                self.class_symbol_table.define(name=name, kind=kind, symbol_type=symbol_type)

    def compile_subroutine(self, class_name):
        """
        example: methoid void dispose() { ...
        """
        while self._not_terminal_token_for('subroutine'):
            self.tokenizer.advance()

            if self._starting_token_for(position='next', keyword_token='parameter_list'):
                function_name = self.tokenizer.current_token
            elif self._starting_token_for(position='current', keyword_token='parameter_list'):
                num_locals = self.compile_parameter_list()
                self.vm_writer.write_function(
                    name='{}.{}'.format(class_name, function_name),
                    num_locals=num_locals
                )
            elif self._starting_token_for('subroutine_body'):
                self.compile_subroutine_body()


    def compile_parameter_list(self):
        """
        example: dispose(int a, int b)
        returns number of params found
        """
        ### symbol table
        kind = 'argument'

        # count params in function def
        num_locals = 0

        while self._not_terminal_token_for(position='next', keyword_token='parameter_list'):
            self.tokenizer.advance()
            # symbol table
            if self.tokenizer.token_type_of(self.tokenizer.next_token) == "IDENTIFIER":
                # get type
                symbol_type = self.tokenizer.current_token
                name = self.tokenizer.next_token
                self.subroutine_symbol_table.define(name=name, kind=kind, symbol_type=symbol_type)
                num_locals += 1
        # advance to closing )
        self.tokenizer.advance()
        return num_locals

    # '{' varDec* statements '}'
    def compile_subroutine_body(self):
        """
        example: { do square.dispose() };
        """
        while self._not_terminal_token_for('subroutine'):
            self.tokenizer.advance()

            if self._starting_token_for('var_dec'):
                self.compile_var_dec()
            elif self._statement_token() :
                self.compile_statements()

    # 'var' type varName (',' varName)* ';'
    def compile_var_dec(self):
        """
        example: var int a;
        """
        ### symbol table
        # reset subroutine symbols
        self.subroutine_symbol_table.reset()
        # all var decs are local variables
        kind = 'local'

        # get symbol type
        self.tokenizer.advance()
        symbol_type = self.tokenizer.keyword()

        # get all identifiers
        while self._not_terminal_token_for('var_dec'):
            self.tokenizer.advance()
            if self.tokenizer.identifier():
                # add symbol to class
                name = self.tokenizer.identifier()
                self.subroutine_symbol_table.define(name=name, kind=kind, symbol_type=symbol_type)

    def compile_statements(self):
        """
        call correct statement
        """
        while self._not_terminal_token_for('subroutine'):
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

    def compile_statement_body(self, not_terminate_func, condition_func, do_something_special_func):
        """
        way to help DRY up statement body
        maybe a little confusing?
        """
        while not_terminate_func():
            self.tokenizer.advance()

            if condition_func():
                do_something_special_func()

    def compile_do(self):
        """
        example: do square.dispose();
        """
        # experimental
        #def do_terminator_func():
        #    return self._not_terminal_token_for('do')
        #def do_condition_func():
        #    return self._starting_token_for('expression_list')
        #def do_something_special_func():
        #    return self.compile_expression_list()

        #self.compile_statement_body(do_terminator_func, do_condition_func, do_something_special_func)

        # get name for call
        name = ''
        while not self._starting_token_for(position='next', keyword_token='expression_list'):
            self.tokenizer.advance()
            if self.tokenizer.next_token == '.':
                symbol_name = self.tokenizer.current_token
            name += self.tokenizer.current_token
        # conditionally write symbol
        if self.subroutine_symbol_table.find_symbol_by_name(symbol_name):
            symbol = self.subroutine_symbol_table.find_symbol_by_name(symbol_name)
            segment = 'local'
            index = symbol['index']
            self.vm_writer.write_push(segment=segment, index=index)
        elif self.class_symbol_table.find_symbol_by_name(symbol_name):
            symbol = self.class_symbol_table.find_symbol_by_name(symbol_name)
            segment = 'local'
            index = symbol['index']
            self.vm_writer.write_push(segment=segment, index=index)

        # start expression list
        self.tokenizer.advance()
        num_args = self.compile_expression_list()
        self.vm_writer.write_call(name=name, num_args=num_args)
        # pop off return of previous call we don't care about
        self.vm_writer.write_pop(segment='temp', index='0')

    # LEAVING UNDRY FOR NOW TO SEE WHAT NEXT PROJECT BRINGS

    # 'let' varName ('[' expression ']')? '=' expression ';'
    def compile_let(self):
        """
        example: let direction = 0;
        """
        while self._not_terminal_token_for('let'):
            self.tokenizer.advance()

            if self._starting_token_for('expression'):
                self.compile_expression()

    # 'while' '(' expression ')' '{' statements '}'
    def compile_while(self):
        """
        example: while (x > 0) { ... }
        """
        # advance to expression start (
        self.tokenizer.advance()

        # compile expression in ()
        self.compile_expression()

        while self._not_terminal_token_for('while'):
            self.tokenizer.advance()

            if self._statement_token():
                self.compile_statements()

    def compile_if(self):
        """
        example: if (True) { ... } else { ... }
        """
        # advance to expression start
        self.tokenizer.advance()

        # compile expression in ()
        self.compile_expression()

        def not_terminate_func():
            return self._not_terminal_token_for('if')
        def condition_func():
            return self._statement_token()
        def do_something_special_func():
            return self.compile_statements()
        self.compile_statement_body(not_terminate_func, condition_func, do_something_special_func)

        # compile else
        if self.tokenizer.next_token == "else":
            # past closing {
            self.tokenizer.advance()
            # same as above
            self.compile_statement_body(
                not_terminate_func,
                condition_func,
                do_something_special_func
            )

    # term (op term)*
    def compile_expression(self):
        """
        many examples..i,e., x = 4
        """
        # check starting for unary negative
        if self._starting_token_for('expression') and self._next_token_is_negative_unary_operator():
            unary_negative_token = True
        else:
            unary_negative_token = False

        self.tokenizer.advance()

        op = None
        while self._not_terminal_token_for('expression'):
            if self._operator_token() and not unary_negative_token:
                op = self.tokenizer.current_token
                self.tokenizer.advance()
            else:
                self.compile_term()
        if op:
            self.compile_op(op)

    def compile_op(self, op):
        if op == '*':
            self.vm_writer.write_call(name='Math.multiply', num_args=2)
        else:
            self.vm_writer.write_arithmetic(command=op)

    def compile_expression_in_expression_list(self):
        """
        separeted out of compile_expression because of edge cases from normal expression
        example: (x, y, x + 5)
        """
        # go till , or (
        while self._not_terminal_token_for('expression'):
            if self._operator_token():
                self.tokenizer.advance()
            else:
                self.compile_term()
                # term takes care of advancing..


    # (expression (',' expression)* )?
    def compile_expression_list(self):
        """
        separeted out of compile_expression because of edge cases from normal expression
        example: (x, y, x + 5)
        """
        num_args = 0
        while self._not_terminal_token_for('expression_list'):
            self.compile_expression()
            num_args += 1
            # current token could be , or ) to end expression list
            if self._another_expression_coming():
                self.tokenizer.advance()
        return num_args

    # integerConstant | stringConstant | keywordConstant | varName |
    # varName '[' expression ']' | subroutineCall | '(' expression ')' | unaryOp term
    def compile_term(self):
        """
        most compilicated and difficult part of compiler
        TODO: try to simplify
        """
        while self._not_terminal_condition_for_term():
            if self.tokenizer.part_of_subroutine_call():
                self.compile_expression_list()
            elif self._starting_token_for('expression'):
                self.compile_expression()
            elif self.tokenizer.current_token in self.UNARY_OPERATORS:
                if self._starting_token_for(keyword_token='expression', position='next'):
                    self.tokenizer.advance()
                    self.compile_term()
                    break
                else:
                    self.tokenizer.advance()
            else:
                self.vm_writer.write_push(segment='constant', index=self.tokenizer.current_token)
            # i.e., i *
            if self._next_token_is_operation_not_in_expression():
                self.tokenizer.advance()
                break

            self.tokenizer.advance()

    def compile_return(self):
        """
        example: return x; or return;
        """
        if self._not_terminal_token_for(keyword_token='return', position='next'):
            self.compile_expression()
        else: # push constant for void
            self.vm_writer.write_push(segment='constant', index='0')
            self.tokenizer.advance()

        self.vm_writer.write_return()


    def _write_current_outer_tag(self, body):
        self.output_file.write("<{}>\n".format(body))


    def _write_current_terminal_token(self):
        # conform to expected xml
        if self.tokenizer.token_type_of(self.tokenizer.current_token) == "STRING_CONST":
            tag_name = "stringConstant"
        elif self.tokenizer.token_type_of(self.tokenizer.current_token) == "INT_CONST":
            tag_name = "integerConstant"
        else:
            tag_name = self.tokenizer.token_type_of(self.tokenizer.current_token).lower()

        if self.tokenizer.token_type_of(self.tokenizer.current_token) == "STRING_CONST":
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

    def _terminal_token_type(self):
        return self.tokenizer.token_type_of(self.tokenizer.current_token) in self.TERMINAL_TOKEN_TYPES

    def _terminal_keyword(self):
        return self.tokenizer.current_token in self.TERMINAL_KEYWORDS

    def _not_terminal_token_for(self, keyword_token, position='current'):
        if position == 'current':
            return not self.tokenizer.current_token in self.TERMINATING_TOKENS[keyword_token]
        elif position == 'next':
            return not self.tokenizer.next_token in self.TERMINATING_TOKENS[keyword_token]

    def _starting_token_for(self, keyword_token, position='current'):
        if position == 'current':
            return self.tokenizer.current_token in self.STARTING_TOKENS[keyword_token]
        elif position == 'next':
            return self.tokenizer.next_token in self.STARTING_TOKENS[keyword_token]

    def _statement_token(self):
        return self.tokenizer.current_token in self.STATEMENT_TOKENS

    def _operator_token(self, position='current'):
        if position == 'current':
            return self.tokenizer.current_token in self.OPERATORS
        elif position == 'next':
            return self.tokenizer.next_token in self.OPERATORS

    def _next_token_is_negative_unary_operator(self):
        return self.tokenizer.next_token == "-"

    def _another_expression_coming(self):
        return self.tokenizer.current_token == ","

    def _not_terminal_condition_for_term(self):
        # expression happens to cover all bases
        return self._not_terminal_token_for('expression')

    def _next_token_is_operation_not_in_expression(self):
        return self._operator_token(position='next') and not self._starting_token_for('expression')
