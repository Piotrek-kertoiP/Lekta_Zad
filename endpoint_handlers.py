from custom_exceptions import ParenthesesError, UnallowedCharacterError, MissingOperationArgumentError, InvalidExpressionError

'''These are functions that may be commonly used'''
def is_operator(char):
    if char == "+" or char == "-" or char == '/' or char == "*":
        return True
    return False

def is_digit(char):
    if "0" <= char <= "9":
        return True
    return False

def is_number(string):
    for char in string:
        if not is_digit(char):
            return False
    return True

'''Class RequestValidator checks if expression is proper and prepares it for evaluation using Reverse Polish Notation'''
class RequestValidator:
    def __init__(self, request):
        self.expr = request.json["expression"]

    def omit_whitespaces(self):
        self.expr = self.expr.replace(" ", "")

    def check_parentheses(self):
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

    # this function changes unary minus like (-1) to (0-1); we'll check it later if it's proper unary minus (not (-*))
    def change_unary_minus(self):
        for i in range(0, len(self.expr) - 1):
            if self.expr[i] == "(" and self.expr[i+1] == "-":
                self.expr = self.expr[:i+1] + "0" + self.expr[i+1:]

    # this function checks if every operator is surrounded with 2 digits after getting rid of unary minuses
    def check_operator_neighbours(self):
        print(self.expr)
        # check first and last character to avoid indexing out of bounds
        expr_len = len(self.expr)
        first_char = self.expr[0]
        last_char = self.expr[expr_len - 1]
        if is_operator(first_char) or is_operator(last_char):
            return False
        # check the inner part
        for i in range(1, len(self.expr)-1):
            if is_operator(self.expr[i]) and (is_operator(self.expr[i-1]) or is_operator(self.expr[i+1])):
                return False
        return True

    def add_missing_parentheses(self):
        # todo
        pass

    def validate_request(self):
        self.omit_whitespaces()
        if not self.check_parentheses():
            raise ParenthesesError
        if not self.check_for_unallowed_characters():
            raise UnallowedCharacterError
        self.change_unary_minus()
        if not self.check_operator_neighbours():
            raise MissingOperationArgumentError
        self.add_missing_parentheses()
        print("validate_request: " + self.expr)
        return self.expr


class ExpressionEvaluator:
    def __init__(self, expr):
        self.expr = expr
        self.operator_stack = []
        self.numbers_stack = []

    def evaluate_expr(self):
        print("evaluate_expr: " + self.expr)
        return self.expr
