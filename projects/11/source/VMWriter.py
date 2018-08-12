class VMWriter():
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

    def write_pop(self, segment, index):
        """
        writes a vm pop command
        segments: CONST, ARG, LOCAL, STATIC, THIS, THAT, POINTER, TEMP
        index: int
        """

    def write_arithmetic(self, command):
        """
        writes a vm arithmetic-logical command
        commands: ADD, SUB, NEG, EQ, GT, LT, AND, OR, NOT
        """

    def write_label(self, label):
        """
        writes a VM label comand
        label: string
        """

    def write_goto(self, label):
        """
        writes a VM goto comand
        label: string
        """

    def write_if(self, label):
        """
        writes a VM if-goto comand
        label: string
        """

    def write_call(self, name, num_args):
        """
        writes a VM call command
        name: string, name of subroutine
        num_args: int, number of arguments to subroutine
        """

    def write_function(self, name, num_locals):
        """
        writes a VM call command
        name: string, name of subroutine
        num_locals: int, number of locals for function
        """

    def write_return(self):
        """
        writes a vm return command
        """

