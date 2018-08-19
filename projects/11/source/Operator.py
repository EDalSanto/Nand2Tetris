class Operator():
    def __init__(self, token, category):
        self.token = token
        self.category = category

    def unary(self):
        return self.category == 'unary'

    def multiplication(self):
        return self.token == '*'

    def division(self):
        return self.token == '/'
