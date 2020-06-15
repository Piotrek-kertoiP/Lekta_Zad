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
        mul_div_index = 0
        while mul_div_index < len(self.expr):
            if self.expr[mul_div_index] == "*" or self.expr[mul_div_index] == "/":
                # wrap left argument
                if 0 <= mul_div_index - 1 and not self.expr[mul_div_index - 1] == ")":
                    left_index = mul_div_index - 1
                    while left_index > 0 and is_digit(self.expr[left_index]):
                        left_index += -1
                    self.expr = self.expr[0:left_index + 1] + "(" + self.expr[left_index + 1:mul_div_index] + ")" + self.expr[mul_div_index:]
                    mul_div_index += 2
                # wrap right argument
                if mul_div_index + 1 <= len(self.expr) and not self.expr[mul_div_index + 1] == "(":
                    right_index = mul_div_index + 1
                    while right_index < len(self.expr) and is_digit(self.expr[right_index]):
                        right_index += 1
                    self.expr = self.expr[0:mul_div_index + 1] + "(" + self.expr[mul_div_index + 1:right_index] + ")" + self.expr[right_index:]
                    mul_div_index += 2
            mul_div_index += 1

        # wrap left, right argument and mul/div operator
        mul_div_index = 0
        while mul_div_index < len(self.expr):
            if self.expr[mul_div_index] == "*" or self.expr[mul_div_index] == "/":
                left_index = mul_div_index - 2
                right_index = mul_div_index + 2
                left_arg_parenth_cntr = 1
                right_arg_parenth_cntr = 1
                while left_index > 0 and not left_arg_parenth_cntr == 0:
                    if self.expr[left_index] == ")":
                        left_arg_parenth_cntr += 1
                    elif self.expr[left_index] == "(":
                        left_arg_parenth_cntr += -1
                    left_index += -1
                while right_index < len(self.expr) and not right_arg_parenth_cntr == 0:
                    if self.expr[right_index] == ")":
                        right_arg_parenth_cntr += -1
                    elif self.expr[right_index] == "(":
                        right_arg_parenth_cntr += 1
                    right_index += 1
                self.expr = self.expr[0:left_index+1] + "(" + self.expr[left_index+1:right_index] + ")" + self.expr[right_index:]
                mul_div_index += 1
            mul_div_index += 1

        add_substr_index = 0
        while add_substr_index < len(self.expr):
            if self.expr[add_substr_index] == "+" or self.expr[add_substr_index] == "-":
                # wrap left argument
                if 0 <= add_substr_index - 1 and not self.expr[add_substr_index - 1] == ")":
                    left_index = add_substr_index - 1
                    while left_index > 0 and is_digit(self.expr[left_index]):
                        left_index += -1
                    self.expr = self.expr[0:left_index + 1] + "(" + self.expr[left_index + 1:add_substr_index] + ")" + self.expr[add_substr_index:]
                    add_substr_index += 2
                # wrap right argument
                if add_substr_index + 1 <= len(self.expr) and not self.expr[add_substr_index + 1] == "(":
                    right_index = add_substr_index + 1
                    while right_index < len(self.expr) and is_digit(self.expr[right_index]):
                        right_index += 1
                    self.expr = self.expr[0:add_substr_index + 1] + "(" + self.expr[add_substr_index + 1:right_index] + ")" + self.expr[right_index:]
                    add_substr_index += 2
            add_substr_index += 1

        # wrap left, right argument and mul/div operator
        add_substr_index = 0
        while add_substr_index < len(self.expr):
            if self.expr[add_substr_index] == "*" or self.expr[add_substr_index] == "/":
                left_index = add_substr_index - 2
                right_index = add_substr_index + 2
                left_arg_parenth_cntr = 1
                right_arg_parenth_cntr = 1
                while left_index > 0 and not left_arg_parenth_cntr == 0:
                    if self.expr[left_index] == ")":
                        left_arg_parenth_cntr += 1
                    elif self.expr[left_index] == "(":
                        left_arg_parenth_cntr += -1
                    left_index += -1
                while right_index < len(self.expr) and not right_arg_parenth_cntr == 0:
                    if self.expr[right_index] == ")":
                        right_arg_parenth_cntr += -1
                    elif self.expr[right_index] == "(":
                        right_arg_parenth_cntr += 1
                    right_index += 1
                self.expr = self.expr[0:left_index + 1] + "(" + self.expr[left_index + 1:right_index] + ")" + self.expr[right_index:]
                add_substr_index += 1
            add_substr_index += 1


    def remove_redundant_parentheses(self):
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
        self.remove_redundant_parentheses()
        print("validate_request: " + self.expr)
        return self.expr



class ExpressionEvaluator:
    def __init__(self, expr):
        self.expr = expr
        self.operator_stack = []
        self.numbers_stack = []

    def evaluate_expr(self):
        print("evaluate_expr: " + self.expr)
        # todo: implement ONP algorithm
        return self.expr + "\n"
