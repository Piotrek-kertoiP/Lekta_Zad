from custom_exceptions import ParenthesisError, UnallowedCharacterError

class RequestValidator:

    def __init__(self, request):
        self.expr = request.json["expression"]

    def omit_whitespaces(self):
        self.expr.replace(chr(127), "")
        for i in range(0, 32):
            self.expr.replace(chr(i), "")

    def check_parenthesis(self):
        counter = 0
        for char in self.expr:
            if char == "(":
                counter += 1
            if char == ")":
                counter += -1
            if counter < 0:
                return False
        if counter != 0:
            return False
        return True

    def check_for_unallowed_characters(self):
        for char in self.expr:
            if not ((47 <= ord(char) <= 57) or (40 <= ord(char) <= 43) or (ord(char) == 45) or (ord(char) == 32)):
                return False
        return True

    def validate_request(self):

        if not self.check_parenthesis():
            raise ParenthesisError
        if not self.check_for_unallowed_characters():
            raise UnallowedCharacterError
        self.omit_whitespaces()

        print(self.expr)
        return self.expr








def any_parenthesis(expr):
    return True


def get_leftmost_parenthesis(expr):
    pass


def evaluate_expr(expr):

    '''while any_parenthesis(expr):
        index_from = 0
        index_to = 0
        leftmost_parenthesis = ""
        [leftmost_parenthesis, index_from, index_to] = get_leftmost_parenthesis(expr)'''

    return "suma podstawy rowna sie kwadratowi obu ramion\n"
