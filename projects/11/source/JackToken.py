class JackToken():
    KEYWORD_TOKENS = [
        'class',
        'constructor',
        'function',
        'method',
        'field',
        'static',
        'var',
        'int',
        'char',
        'boolean',
        'void',
        'true',
        'false',
        'null',
        'this',
        'let',
        'do',
        'if',
        'else',
        'while',
        'return'
    ]
    CLASS_VAR_DEC_TOKENS = [ 'static', 'field' ]
    SUBROUTINE_TOKENS = [ 'function', 'method', 'constructor' ]
    STATEMENT_TOKENS = [ 'do', 'let', 'while', 'return', 'if' ]
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
    TOKENS_THAT_NEED_LABELS = ['if', 'while']

    def __init__(self, text):
        self.text = text

    def token_type(self):
        if not self.text:
            return None
        elif self.text[0] == "\"":
            return "STRING_CONST"
        elif self.text in self.KEYWORD_TOKENS:
            return "KEYWORD"
        elif self.text.isnumeric():
            return "INT_CONST"
        elif self.text.isalnum():
            return "IDENTIFIER"
        else:
            return "SYMBOL"

    def is_expression_list_delimiter(self):
        return self.text == ','

    def is_expression_list_starter(self):
        return self.text == '('

    def is_subroutine_call_delimiter(self):
        return self.text == '.'

    def is_unary_operator(self):
        return self.text in self.UNARY_OPERATORS

    def is_operator(self):
        return self.text in self.OPERATORS

    def is_if(self):
        return self.text == 'if'

    def is_statement_token(self):
        return self.text in self.STATEMENT_TOKENS

    def starts_class_var_dec(self):
        return self.text in self.CLASS_VAR_DEC_TOKENS

    def starts_subroutine(self):
        return self.text in self.SUBROUTINE_TOKENS

    def is_class(self):
        return self.text == "class"

    def is_string_const(self):
        return self.token_type() == "STRING_CONST"

    def is_identifier(self):
        return self.token_type() == "IDENTIFIER"

    def is_keyword(self):
        return self.token_type() == "KEYWORD"

    def is_boolean(self):
        return self.text in ['true', 'false']

    def is_null(self):
        return self.text == 'null'

    def is_empty(self):
        return len(self.text) == 0
