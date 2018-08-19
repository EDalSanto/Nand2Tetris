from SymbolTable import SymbolTable
from VMWriter import VMWriter
from LabelCounter import LabelCounter
from Operator import Operator

class CompilationEngine():
    """
    compiles a jack source file from a jack tokenizer into xml form in output_file
    NOTE: ASSUMES ERROR FREE CODE -> a todo could be to add error handling
    """
    SYMBOL_KINDS = {
        'parameter_list': 'argument',
        'var_dec': 'local'
    }
    STARTING_TOKENS = {
        'var_dec': ['var'],
        'parameter_list': ['('],
        'subroutine_body': ['{'],
        'expression_list': ['('],
        'expression': ['=', '[', '('],
        'array': [ '[' ],
        'conditional': ['if', 'else']
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
        'expression': [';', ')', ']', ','],
        'array': [']']
    }
    TOKENS_THAT_NEED_LABELS = ['if', 'while']

    def __init__(self, tokenizer, output_file):
        self.tokenizer = tokenizer
        self.output_file = output_file
        self.class_symbol_table = SymbolTable()
        self.subroutine_symbol_table = SymbolTable()
        self.vm_writer = VMWriter(output_file)
        self.label_counter = LabelCounter(labels=self.TOKENS_THAT_NEED_LABELS)
        self.class_name = None

    def compile_class(self):
        """
        everything needed to compile a class, the basic unit of compilation
        """
        # skip everything up to class start
        while not self.tokenizer.class_token_reached():
            self.tokenizer.advance()
        # since compilation unit is a class makes sense to store this as instance variable
        self.class_name = self.tokenizer.next_token.text

        while self.tokenizer.has_more_tokens:
            self.tokenizer.advance()

            if self.tokenizer.current_token.starts_class_var_dec():
                self.compile_class_var_dec()
            elif self.tokenizer.current_token.starts_subroutine():
                self.compile_subroutine()

    def compile_class_var_dec(self):
        """
        example: field int x;
        """
        symbol_kind = self.tokenizer.keyword()

        # get symbol type
        self.tokenizer.advance()
        symbol_type = self.tokenizer.keyword()

        # get all identifiers
        while self._not_terminal_token_for('class_var_dec'):
            self.tokenizer.advance()

            if self.tokenizer.identifier():
                # add symbol to class
                symbol_name = self.tokenizer.identifier()
                self.class_symbol_table.define(
                    name=symbol_name,
                    kind=symbol_kind,
                    symbol_type=symbol_type
                )

    def compile_subroutine(self):
        """
        example: methoid void dispose() { ...
        """
        # new subroutine means new subroutine scope
        self.subroutine_symbol_table.reset()

        # get subroutine name
        self.tokenizer.advance()
        self.tokenizer.advance()
        subroutine_name = self.tokenizer.current_token.text

        # compile parameter list
        self.tokenizer.advance()
        self.compile_parameter_list()

        # compile body
        self.tokenizer.advance()
        self.compile_subroutine_body(subroutine_name=subroutine_name)

        # rest counts from subroutine
        self.label_counter.reset_counts()

    def compile_subroutine_body(self, subroutine_name):
        # skip start
        self.tokenizer.advance()
        # get all locals
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
        while self._not_terminal_token_for('subroutine'):
            self.compile_statements()

    def compile_parameter_list(self):
        """
        example: dispose(int a, int b)
        returns number of params found
        """
        ### symbol table
        while self._not_terminal_token_for('parameter_list'):
            self.tokenizer.advance()

            # symbol table
            if self.tokenizer.next_token.is_identifier():
                symbol_kind = self.SYMBOL_KINDS['parameter_list']
                symbol_type = self.tokenizer.current_token.text
                symbol_name = self.tokenizer.next_token.text
                self.subroutine_symbol_table.define(
                    name=symbol_name,
                    kind=symbol_kind,
                    symbol_type=symbol_type
                )

    # 'var' type varName (',' varName)* ';'
    def compile_var_dec(self):
        """
        example: var int a;
        """
        # skip var
        self.tokenizer.advance()
        # get symbol type
        symbol_type = self.tokenizer.current_token.text
        # count number of vars, i.e., var int i, sum = 2
        num_vars = 0

        # get all vars
        while self._not_terminal_token_for('var_dec'):
            self.tokenizer.advance()

            if self.tokenizer.identifier():
                num_vars += 1
                symbol_kind = self.SYMBOL_KINDS['var_dec']
                symbol_name = self.tokenizer.identifier()
                self.subroutine_symbol_table.define(
                    name=symbol_name,
                    kind=symbol_kind,
                    symbol_type=symbol_type
                )
        # return vars processed
        return num_vars

    def compile_statements(self):
        """
        call correct statement
        """
        # TODO: way to make this global for class?
        statement_compile_methods = {
            'if': self.compile_if,
            'do': self.compile_do,
            'let': self.compile_let,
            'while': self.compile_while,
            'return': self.compile_return
        }

        while self._not_terminal_token_for('subroutine'):
            if self.tokenizer.current_token.is_statement_token():
                statement_type = self.tokenizer.current_token.text
                statement_compile_methods[statement_type]()

            self.tokenizer.advance()

    def compile_do(self):
        """
        example: do square.dispose();
        """
        # get to caller
        self.tokenizer.advance()
        # set caller_name
        caller_name = self.tokenizer.current_token.text
        # look up in symbol table
        symbol = self._find_symbol_in_symbol_tables(symbol_name=caller_name)
        # skip .
        self.tokenizer.advance()
        # subroutine name
        self.tokenizer.advance()
        # set subroutine name
        subroutine_name = self.tokenizer.current_token.text

        if symbol: # user defined Method
            # push value onto local segment
            segment = 'local'
            index = symbol['index']
            symbol_type = symbol['type']
            self.vm_writer.write_push(segment=segment, index=index)
        else: # i.e, OS call
            symbol_type = caller_name

        subroutine_call_name = symbol_type + '.' + subroutine_name
        # start expression list
        self.tokenizer.advance()
        # get arguments in expession list
        num_args = self.compile_expression_list()
        # method call
        if symbol:
            # calling object passed as implicit argument
            num_args += 1
        # write call
        self.vm_writer.write_call(name=subroutine_call_name, num_args=num_args)
        # pop off return of previous call we don't care about
        self.vm_writer.write_pop(segment='temp', index='0')

    # 'let' varName ('[' expression ']')? '=' expression ';'
    def compile_let(self):
        """
        example: let direction = 0;
        """
        # get symbol to store expression evaluation
        self.tokenizer.advance()
        symbol_name = self.tokenizer.current_token.text
        symbol = self._find_symbol_in_symbol_tables(symbol_name=symbol_name)

        # array assignment?
        array_assignment = self._starting_token_for(keyword_token='array', position='next')
        if array_assignment:
            # get to index expression
            self.tokenizer.advance()
            self.tokenizer.advance()
            # compile it
            self.compile_expression()
            self.vm_writer.write_push(segment=symbol['kind'], index=symbol['index'])
            # add two addresses
            self.vm_writer.write_arithmetic(command='+')

        # go past =
        while not self.tokenizer.current_token.text == '=':
            self.tokenizer.advance()
        # compile all expressions
        while self._not_terminal_token_for('let'):
            self.tokenizer.advance()
            self.compile_expression()

        if not array_assignment:
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
        self.vm_writer.write_label(
            label='WHILE_EXP{}'.format(self.label_counter.get('while'))
        )

        # advance to expression start (
        self.tokenizer.advance()
        self.tokenizer.advance()

        # compile expression in ()
        self.compile_expression()

        # NOT expression so for easily handling of termination and if-goto
        self.vm_writer.write_unary(command='~')
        self.vm_writer.write_ifgoto(
            label='WHILE_END{}'.format(self.label_counter.get('while'))
        )

        while self._not_terminal_token_for('while'):
            self.tokenizer.advance()

            if self._statement_token():
                self.compile_statements()

        # write goto
        self.vm_writer.write_goto(
            label='WHILE_EXP{}'.format(self.label_counter.get('while'))
        )
        # write end label
        self.vm_writer.write_label(
            label='WHILE_END{}'.format(self.label_counter.get('while'))
        )
        # add while to labels count
        self.label_counter.increment('while')

    def compile_if(self):
        """
        example: if (True) { ... } else { ... }
        """
        # advance to expression start
        self.tokenizer.advance()
        self.tokenizer.advance()
        # compile expression in ()
        self.compile_expression()
        # write ifgoto to if statement
        self.vm_writer.write_ifgoto(label='IF_TRUE{}'.format(self.label_counter.get('if')))
        # write goto if false (else)
        self.vm_writer.write_goto(label='IF_FALSE{}'.format(self.label_counter.get('if')))
        # write if label
        self.vm_writer.write_label(label='IF_TRUE{}'.format(self.label_counter.get('if')))
        # body of if
        self.compile_conditional_body()
        # else?
        if self._starting_token_for(keyword_token='conditional', position='next'):
            # past closing {
            self.tokenizer.advance()
            # goto if end if this path wasn't hit
            self.vm_writer.write_goto(
                label='IF_END{}'.format(self.label_counter.get('if'))
            )
            # if false
            self.vm_writer.write_label(
                label='IF_FALSE{}'.format(self.label_counter.get('if'))
            )
            # compile else
            self.compile_conditional_body()
            # define IF_END
            self.vm_writer.write_label(
                label='IF_END{}'.format(self.label_counter.get('if'))
            )
        else: # no else present
            # go to end of if
            self.vm_writer.write_label(
                label='IF_FALSE{}'.format(self.label_counter.get('if'))
            )

    def compile_conditional_body(self):
        while self._not_terminal_token_for('if'):
            self.tokenizer.advance()

            if self._statement_token():
                if self.tokenizer.current_token.is_if():
                    # add ifto labels count
                    self.label_counter.increment('if')
                    # compile nested if
                    self.compile_statements()
                    # subtract for exiting nesting
                    self.label_counter.decrement('if')
                else:
                    self.compile_statements()

    # term (op term)*
    def compile_expression(self):
        """
        many examples..i,e., x = 4
        """
        # ops get compiled at end in reverse order in which they were added
        ops = []

        while self._not_terminal_token_for('expression'):
            if self._subroutine_call():
                self.compile_subroutine_call()
            elif self._array_expression():
                self.compile_array_expression()
            elif self.tokenizer.current_token.text.isdigit():
                self.vm_writer.write_push(
                    segment='constant',
                    index=self.tokenizer.current_token.text
                )
            elif self.tokenizer.identifier():
                self.compile_symbol_push()
            elif self.tokenizer.current_token.is_operator() and not self._part_of_expression_list():
                ops.insert(0, Operator(token=self.tokenizer.current_token.text, category='bi'))
            elif self.tokenizer.current_token.is_unary_operator():
                ops.insert(0, Operator(token=self.tokenizer.current_token.text, category='unary'))
            elif self.tokenizer.string_const():
                self.compile_string_const()
            elif self.tokenizer.boolean(): # boolean case
                self.compile_boolean()
            elif self._starting_token_for('expression'): # nested expression
                # skip starting (
                self.tokenizer.advance()
                self.compile_expression()
            elif self.tokenizer.null():
                self.vm_writer.write_push(segment='constant', index=0)

            self.tokenizer.advance()

        # compile_ops
        for op in ops:
            self.compile_op(op)

    def compile_op(self, op):
        """
        example: +, /, etc.
        """
        if op.unary():
            self.vm_writer.write_unary(command=op.token)
        elif op.multiplication():
            self.vm_writer.write_call(name='Math.multiply', num_args=2)
        elif op.division():
            self.vm_writer.write_call(name='Math.divide', num_args=2)
        else:
            self.vm_writer.write_arithmetic(command=op.token)

    def compile_boolean(self):
        """
        'true' and 'false'
        """
        self.vm_writer.write_push(segment='constant', index=0)

        if self.tokenizer.boolean() == 'true':
            # negate true
            self.vm_writer.write_unary(command='~')

    def compile_string_const(self):
        """
        example: "Hello World"
        """
        # handle string const
        string_length = len(self.tokenizer.string_const())
        self.vm_writer.write_push(segment='constant', index=string_length)
        self.vm_writer.write_call(name='String.new', num_args=1)
        # build string from chars
        for char in self.tokenizer.string_const():
            if not char == self.tokenizer.STRING_CONST_DELIMITER:
                ascii_value_of_char = ord(char)
                self.vm_writer.write_push(segment='constant', index=ascii_value_of_char)
                self.vm_writer.write_call(name='String.appendChar', num_args=2)

    def compile_symbol_push(self):
        """
        example: x
        """
        symbol = self._find_symbol_in_symbol_tables(symbol_name=self.tokenizer.identifier())
        segment = symbol['kind']
        index = symbol['index']
        self.vm_writer.write_push(segment=segment, index=index)

    def compile_array_expression(self):
        """
        example: let x = a[j], a[4]
        """
        symbol_name = self.tokenizer.current_token.text
        symbol = self._find_symbol_in_symbol_tables(symbol_name=symbol_name)
        # get to index expression
        self.tokenizer.advance()
        self.tokenizer.advance()
        # compile
        self.compile_expression()
        # push onto local array symbol
        self.vm_writer.write_push(segment='local', index=symbol['index'])
        # add two addresses: identifer and expression result
        self.vm_writer.write_arithmetic(command='+')
        # pop address onto pointer 1 / THAT
        self.vm_writer.write_pop(segment='pointer', index=1)
        # push value onto stack
        self.vm_writer.write_push(segment='that', index=0)

    def compile_subroutine_call(self):
        """
        example: Memory.peek(8000)
        """
        subroutine_name = ''

        while not self._starting_token_for('expression_list'):
            subroutine_name += self.tokenizer.current_token.text
            self.tokenizer.advance()
        # get num of args
        num_args = self.compile_expression_list()
        # write_call after pushing arguments onto stack
        self.vm_writer.write_call(name=subroutine_name, num_args=num_args)

    # (expression (',' expression)* )?
    def compile_expression_list(self):
        """
        separeted out of compile_expression because of edge cases from normal expression
        example: (x, y, x + 5)
        """
        num_args = 0

        if self._empty_expression_list():
            return num_args

        # start expressions
        self.tokenizer.advance()

        while self._not_terminal_token_for('expression_list'):
            num_args += 1
            self.compile_expression()
            if self._another_expression_coming(): # would be , after compile expression
                self.tokenizer.advance()
        return num_args

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

    def _not_terminal_token_for(self, keyword_token, position='current'):
        if position == 'current':
            return not self.tokenizer.current_token.text in self.TERMINATING_TOKENS[keyword_token]
        elif position == 'next':
            return not self.tokenizer.next_token.text in self.TERMINATING_TOKENS[keyword_token]

    def _starting_token_for(self, keyword_token, position='current'):
        if position == 'current':
            return self.tokenizer.current_token.text in self.STARTING_TOKENS[keyword_token]
        elif position == 'next':
            return self.tokenizer.next_token.text in self.STARTING_TOKENS[keyword_token]

    def _statement_token(self):
        return self.tokenizer.current_token.is_statement_token()

    def _another_expression_coming(self):
        return self.tokenizer.current_token.is_expression_list_delimiter()

    def _find_symbol_in_symbol_tables(self, symbol_name):
        if self.subroutine_symbol_table.find_symbol_by_name(symbol_name):
            return self.subroutine_symbol_table.find_symbol_by_name(symbol_name)
        elif self.class_symbol_table.find_symbol_by_name(symbol_name):
            return self.class_symbol_table.find_symbol_by_name(symbol_name)

    def _empty_expression_list(self):
        return self._start_of_expression_list() and self._next_ends_expression_list()

    def _start_of_expression_list(self):
        return self.tokenizer.current_token.text in self.STARTING_TOKENS['expression_list']

    def _next_ends_expression_list(self):
        return self.tokenizer.next_token.text in self.TERMINATING_TOKENS['expression_list']

    def _subroutine_call(self):
        return self.tokenizer.identifier() and self.tokenizer.next_token.is_subroutine_call_delimiter()

    def _array_expression(self):
        return self.tokenizer.identifier() and self._starting_token_for(keyword_token='array', position='next')

    def _part_of_expression_list(self):
        return self.tokenizer.part_of_expression_list()
