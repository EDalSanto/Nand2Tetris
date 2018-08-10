class SymbolTable():
    """
    Represents the current symbols for a given class or subroutine for the JackCompiler
    """

    def __init__(self):
        self.symbols = {}

    def start_subroutine(self):
        """
        Starts a new subroutine scope, i.e., resets the subroutine's scope
        """
        self.symbols = {}

    def define(self, name, symbol_type, kind):
        """
        defines a new identifier of the given name, type, and kind and assigns it a running index
        """

    def var_count(self, kind):
        """
        returns the number of variables of the given kind already defined in the current scope
        """

    def kind_of(self, name):
        """
        returns the kind of the named identifer in the current scope
        (STATIC, FIELD, ARG, VAR, NONE)
        """

    def type_of(self, name):
        """
        returns the type of the named identifier in the current scope
        """

    def index_of(self, name):
        """
        returns the index assigned to the named identifier
        """
