class VMWriter():
    ARITHMETIC_LOGICAL_OPERATORS = {
        '+': 'add',
        '-': 'sub',
        '=': 'eq',
        '>': 'gt',
        '<': 'lt',
        '&': 'and',
        '|': 'or'
    }
    UNARY_OPERATORS = {
        '-': 'neg',
        '~': 'not'
    }

    def __init__(self, output_file):
        """
        creates a new .vm file and prepares it for writing
        """
        self.output_file = output_file

    def write_push(self, segment, index):
        """
        writes a vm push command
        segment options: CONST, ARG, LOCAL, STATIC, THIS, THAT, POINTER, TEMP
        index: int
        """
        self.output_file.write('push {} {}\n'.format(segment, index))

    def write_pop(self, segment, index):
        """
        writes a vm pop command
        segments: CONST, ARG, LOCAL, STATIC, THIS, THAT, POINTER, TEMP
        index: int
        """
        self.output_file.write('pop {} {}\n'.format(segment, index))

    def write_arithmetic(self, command):
        """
        writes a vm arithmetic-logical command
        commands: ADD, SUB, EQ, GT, LT, AND, OR
        """
        self.output_file.write(
            '{}\n'.format(self.ARITHMETIC_LOGICAL_OPERATORS[command])
        )

    def write_unary(self, command):
        """
        writes a vm unary command
        commands: NEG, NOT
        """
        self.output_file.write(
            '{}\n'.format(self.UNARY_OPERATORS[command])
        )

    def write_label(self, label):
        """
        writes a VM label comand
        label: string
        """
        self.output_file.write('label {}\n'.format(label))

    def write_goto(self, label):
        """
        writes a VM goto comand
        label: string
        """
        self.output_file.write('goto {}\n'.format(label))

    def write_ifgoto(self, label):
        """
        writes a VM if-goto comand
        label: string
        """
        self.output_file.write('if-goto {}\n'.format(label))

    def write_call(self, name, num_args):
        """
        writes a VM call command
        name: string, name of subroutine
        num_args: int, number of arguments to subroutine
        """
        self.output_file.write(
            'call {} {}\n'.format(name, num_args)
        )

    def write_function(self, name, num_locals):
        """
        writes a VM call command
        name: string, name of subroutine
        num_locals: int, number of locals for function
        """
        self.output_file.write('function {} {}\n'.format(name, num_locals))

    def write_return(self):
        """
        writes a vm return command
        """
        self.output_file.write('return\n')
