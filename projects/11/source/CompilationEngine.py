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
        '&',
        '|',
        '<',
        '>',
        '='
    ]
    UNARY_OPERATORS = [ '-', '~' ]

    def __init__(self, tokenizer, output_file):
        self.tokenizer = tokenizer
        self.output_file = output_file
        self.class_symbol_table = SymbolTable()
        self.subroutine_symbol_table = SymbolTable()
        self.vm_writer = VMWriter(output_file)
        self.labels_count = {'if': 0, 'while': 0}
        self.class_name = None

    def compile_class(self):
        """
        everything needed to compile a class, the basic unit of compilation
        """

        while self.tokenizer.has_more_tokens:
            self.tokenizer.advance()

            if self.tokenizer.identifier():
                # since compilation unit is a class makes sense to store this as instance variable
                self.class_name = self.tokenizer.identifier()
            elif self.tokenizer.current_token in self.CLASS_VAR_DEC_TOKENS:
                self.compile_class_var_dec()
            elif self.tokenizer.current_token in self.SUBROUTINE_TOKENS:
                self.compile_subroutine()

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

    def compile_subroutine(self):
        """
        example: methoid void dispose() { ...
        """
        # reset subroutine symbols
        self.subroutine_symbol_table.reset()

        while self._not_terminal_token_for('subroutine'):
            self.tokenizer.advance()

            if self._starting_token_for(position='next', keyword_token='parameter_list'):
                subroutine_name = self.tokenizer.current_token
            elif self._starting_token_for(position='current', keyword_token='parameter_list'):
                self.compile_parameter_list()
            elif self._starting_token_for('subroutine_body'):
                self.compile_subroutine_body(subroutine_name=subroutine_name)
        # reset counters -> should be scoped to subroutine and nesting level for flow control
        # create Object
        # self.labels_counter.reset()
        self.labels_count = {'if': 0, 'while': 0}

    def compile_subroutine_body(self, subroutine_name):
        # get all locals
        self.tokenizer.advance()
        num_locals = 0
        while self._starting_token_for('var_dec'):
            num_locals += self.compile_var_dec()
            self.tokenizer.advance()

        # write function command
        self.vm_writer.write_function(
            name='{}.{}'.format(self.class_name, subroutine_name),
            num_locals=num_locals
        )

        # compile all statements
        # while starting token for statement
        while self.tokenizer.current_token in ['do', 'let', 'if', 'while', 'return']:
            self.compile_statements()

    def compile_parameter_list(self):
        """
        example: dispose(int a, int b)
        returns number of params found
        """
        ### symbol table
        kind = 'argument'

        while self._not_terminal_token_for(position='next', keyword_token='parameter_list'):
            self.tokenizer.advance()
            # symbol table
            if self.tokenizer.token_type_of(self.tokenizer.next_token) == "IDENTIFIER":
                # get type
                symbol_type = self.tokenizer.current_token
                name = self.tokenizer.next_token
                self.subroutine_symbol_table.define(name=name, kind=kind, symbol_type=symbol_type)
        # advance to closing )
        self.tokenizer.advance()

    # 'var' type varName (',' varName)* ';'
    def compile_var_dec(self):
        """
        example: var int a;
        """
        ### symbol table
        # all var decs are local variables
        kind = 'local'

        # get symbol type
        self.tokenizer.advance()
        symbol_type = self.tokenizer.keyword() or self.tokenizer.identifier()

        # count number of vars, i.e., var int i, sum = 2
        num_vars = 0

        # get all identifiers
        while self._not_terminal_token_for('var_dec'):
            self.tokenizer.advance()
            if self.tokenizer.identifier():
                # add symbol to class
                name = self.tokenizer.identifier()
                self.subroutine_symbol_table.define(name=name, kind=kind, symbol_type=symbol_type)
                num_vars += 1
        # return vars processed
        return num_vars

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

    def compile_do(self):
        """
        example: do square.dispose();
        """
        # get to caller
        self.tokenizer.advance()
        caller_name = self.tokenizer.current_token
        # look up in symbol table
        symbol = self._find_symbol_in_symbol_tables(symbol_name=caller_name)
        # get rest of subroutine call
        # skip .
        self.tokenizer.advance()
        # subroutine name
        self.tokenizer.advance()
        subroutine_name = self.tokenizer.current_token

        if symbol: # always method?
            # push value onto local segment
            segment = 'local'
            index = symbol['index']
            symbol_type = symbol['type']
            self.vm_writer.write_push(segment=segment, index=index)
        else: # i.e, OS call
            symbol_type = caller_name

        name = symbol_type + '.' + subroutine_name
        # start expression list
        self.tokenizer.advance()
        num_args = self.compile_expression_list()
        # method call
        if symbol:
            num_args += 1
        # write call
        self.vm_writer.write_call(name=name, num_args=num_args)
        # pop off return of previous call we don't care about
        self.vm_writer.write_pop(segment='temp', index='0')

    # LEAVING UNDRY FOR NOW TO SEE WHAT NEXT PROJECT BRINGS

    # 'let' varName ('[' expression ']')? '=' expression ';'
    def compile_let(self):
        """
        example: let direction = 0;
        """
        # get symbol to store expression evaluation
        self.tokenizer.advance()
        symbol_name = self.tokenizer.current_token
        symbol = self._find_symbol_in_symbol_tables(symbol_name=symbol_name)
        # check if array assignment
        array = self.tokenizer.next_token == '['
        if array:
            # get to index expression
            self.tokenizer.advance()
            self.tokenizer.advance()
            # compile it
            self.compile_expression()
            self.vm_writer.write_push(segment='local', index=symbol['index'])
            # add two addresses
            self.vm_writer.write_arithmetic(command='+')

        # go past =
        while not self.tokenizer.current_token == '=':
            self.tokenizer.advance()
        # compile all expressions
        while self._not_terminal_token_for('let'):
            self.tokenizer.advance()
            self.compile_expression()

        if not array:
            # store expression evaluation in symbol location
            self.vm_writer.write_pop(segment=symbol['kind'], index=symbol['index'])
        else: # array unloading
            # pop return value onto temp
            self.vm_writer.write_pop(segment='temp', index='0')
            # pop address of array slot onto THAT
            self.vm_writer.write_pop(segment='pointer', index='1')  # pointer 1 => array
            # push value on temp back onto stack
            self.vm_writer.write_push(segment='temp', index='0')
            # set that
            self.vm_writer.write_pop(segment='that', index='0')

    # 'while' '(' expression ')' '{' statements '}'
    def compile_while(self):
        """
        example: while (x > 0) { ... }
        """
        # write while label
        self.vm_writer.write_label(label='WHILE_EXP{}'.format(self.labels_count['while']))

        # advance to expression start (
        self.tokenizer.advance()

        # compile expression in ()
        self.compile_expression()

        # not expression so for easily handling of termination and if-goto
        self.vm_writer.write_unary(command='~')
        self.vm_writer.write_ifgoto(label='WHILE_END{}'.format(self.labels_count['while']))

        while self._not_terminal_token_for('while'):
            self.tokenizer.advance()

            if self._statement_token():
                self.compile_statements()

        # write goto
        self.vm_writer.write_goto(label='WHILE_EXP{}'.format(self.labels_count['while']))
        # write end label
        self.vm_writer.write_label(label='WHILE_END{}'.format(self.labels_count['while']))

        # add while to labels count
        self.labels_count['while'] += 1

    def compile_if(self):
        """
        example: if (True) { ... } else { ... }
        """
        # advance to expression start
        self.tokenizer.advance()

        # compile expression in ()
        self.compile_expression()
        # not expression so for easily handling of termination and if-goto
#        self.vm_writer.write_arithmetic(command='~')

        # write ifgoto to if statement
        self.vm_writer.write_ifgoto(label='IF_TRUE{}'.format(self.labels_count['if']))
        # write goto if false (else)
        self.vm_writer.write_goto(label='IF_FALSE{}'.format(self.labels_count['if']))
        # write if label
        self.vm_writer.write_label(label='IF_TRUE{}'.format(self.labels_count['if']))

        while self._not_terminal_token_for('if'):
            self.tokenizer.advance()

            if self._statement_token():
                if self.tokenizer.current_token == 'if':
                    # add ifto labels count
                    self.labels_count['if'] += 1
                    self.compile_statements()
                    # subtract for nesting
                    self.labels_count['if'] -= 1
                else:
                    self.compile_statements()

        # go to end of if
        self.vm_writer.write_goto(label='IF_END{}'.format(self.labels_count['if']))

        # compile else
        if self.tokenizer.next_token == "else":
            # past closing {
            self.tokenizer.advance()
            # same as above
            self.vm_writer.write_label(label='IF_FALSE{}'.format(self.labels_count['if']))
            while self._not_terminal_token_for('if'):
                self.tokenizer.advance()

                if self._statement_token():
                    if self.tokenizer.current_token == 'if':
                        # add ifto labels count
                        self.labels_count['if'] += 1
                        self.compile_statements()
                    else:
                        self.compile_statements()
        # define IF_END
        self.vm_writer.write_label(label='IF_END{}'.format(self.labels_count['if']))


    # term (op term)*
    def compile_expression(self):
        """
        many examples..i,e., x = 4
        """
        ops = []

        # advance to expression
        if self.tokenizer.current_token == '(':
            self.tokenizer.advance()

        while self._not_terminal_token_for('expression'):
            if self.tokenizer.next_token == '.': # subroutine call
                # write_call after pushing arguments onto stack
                # get name
                subroutine_name = ''
                while not self._starting_token_for('expression_list'):
                    subroutine_name += self.tokenizer.current_token
                    self.tokenizer.advance()
                # get num of args
                num_args = self.compile_expression_list()
                self.vm_writer.write_call(name=subroutine_name, num_args=num_args)
            elif self.tokenizer.current_token.isdigit() and not self.tokenizer.next_token == ']': # not array
                self.vm_writer.write_push(segment='constant', index=self.tokenizer.current_token)
            elif self.tokenizer.current_token.isdigit() and self.tokenizer.next_token == ']': # array
                self.vm_writer.write_push(segment='local', index=self.tokenizer.current_token)
            elif self.tokenizer.identifier() and self.tokenizer.next_token == '[':
                ## compile array
                symbol_name = self.tokenizer.current_token
                symbol = self._find_symbol_in_symbol_tables(symbol_name=symbol_name)
                # get to index expression
                self.tokenizer.advance()
                self.tokenizer.advance()
                # compile it
                self.compile_expression()
                self.vm_writer.write_push(segment='local', index=symbol['index'])
                # add two addresses
                self.vm_writer.write_arithmetic(command='+')
                # pop address onto pointer 1 / THAT
                self.vm_writer.write_pop(segment='pointer', index=1)
                # push value onto stack
                self.vm_writer.write_push(segment='that', index=0)
            elif self.tokenizer.identifier():
                # i.e, push this 0
                # find symbol in symbol table
                symbol = self._find_symbol_in_symbol_tables(self.tokenizer.identifier())
                segment = symbol['kind']
                index = symbol['index']
                self.vm_writer.write_push(segment=segment, index=index)
            elif self.tokenizer.current_token in self.OPERATORS and not self.tokenizer.tokens_found[-3] == ',': # distinguish neg from sub
                ops.insert(0, { 'token': self.tokenizer.current_token, 'category': 'bi' })
            elif self.tokenizer.current_token in self.UNARY_OPERATORS:
                ops.insert(0, { 'token': self.tokenizer.current_token, 'category': 'unary' })
            elif self.tokenizer.string_const():
                # handle string const
                string_length = len(self.tokenizer.string_const())
                self.vm_writer.write_push(segment='constant', index=string_length)
                self.vm_writer.write_call(name='String.new', num_args=1)
                # build string from chars
                for char in self.tokenizer.string_const():
                    if not char == '"':
                        ascii_value_of_char = ord(char)
                        self.vm_writer.write_push(segment='constant', index=ascii_value_of_char)
                        self.vm_writer.write_call(name='String.appendChar', num_args=2)
            elif self.tokenizer.current_token in [ 'true', 'false' ]: # boolean case
                self.vm_writer.write_push(segment='constant', index=0)
                if self.tokenizer.current_token == 'true':
                    # negate true
                    self.vm_writer.write_unary(command='~')
            elif self.tokenizer.current_token == '(': # nested expression
                self.compile_expression()

            self.tokenizer.advance()

        for op in ops:
            self.compile_op(op)

    def compile_op(self, op):
        if op['category'] == 'unary':
            self.vm_writer.write_unary(command=op['token'])
        elif op['token'] == '*':
            self.vm_writer.write_call(name='Math.multiply', num_args=2)
        elif op['token'] == '/':
            self.vm_writer.write_call(name='Math.divide', num_args=2)
        else:
            self.vm_writer.write_arithmetic(command=op['token'])

    # (expression (',' expression)* )?
    def compile_expression_list(self):
        """
        separeted out of compile_expression because of edge cases from normal expression
        example: (x, y, x + 5)
        """
        num_args = 0
        # empty expression list
        if self.tokenizer.next_token in self.TERMINATING_TOKENS['expression_list']:
            return num_args

        while self._not_terminal_token_for('expression_list'):
            num_args += 1
            self.compile_expression()
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

    def _find_symbol_in_symbol_tables(self, symbol_name):
        if self.subroutine_symbol_table.find_symbol_by_name(symbol_name):
            return self.subroutine_symbol_table.find_symbol_by_name(symbol_name)
        elif self.class_symbol_table.find_symbol_by_name(symbol_name):
            return self.class_symbol_table.find_symbol_by_name(symbol_name)
