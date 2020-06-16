from custom_exceptions import ParenthesesError, UnallowedCharacterError, MissingOperationArgumentError, InvalidExpressionError
from queue import LifoQueue, Queue

verbose = True
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
        if verbose: print("omit_whitespaces, start:\t\t\t " + self.expr)
        self.expr = self.expr.replace(" ", "")
        if verbose: print("omit_whitespaces, end:\t\t\t\t " + self.expr)

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
        if verbose: print("change_unary_minus, start:\t\t\t " + self.expr)
        for i in range(0, len(self.expr) - 1):
            if self.expr[i] == "(" and self.expr[i+1] == "-":
                self.expr = self.expr[:i+1] + "0" + self.expr[i+1:]
        if verbose: print("change_unary_minus, end:\t\t\t " + self.expr)

    # this function checks if every operator is surrounded with 2 digits after getting rid of unary minuses
    def check_operator_neighbours(self):
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
        if verbose: print("add_missing_parentheses, start:\t\t " + self.expr)

        mul_div_index = 0
        while mul_div_index < len(self.expr):
            if self.expr[mul_div_index] == "*" or self.expr[mul_div_index] == "/":
                # wrap left argument
                if verbose: print("add_missing_parentheses, mul/div, wrap left argument, start" + self.expr)
                if 0 <= mul_div_index - 1 and not self.expr[mul_div_index - 1] == ")":
                    left_index = mul_div_index - 1
                    while left_index > 0 and is_digit(self.expr[left_index]):
                        left_index += -1
                    self.expr = self.expr[:left_index + 1] + "(" + self.expr[left_index + 1:mul_div_index] + ")" + self.expr[mul_div_index:]
                    mul_div_index += 2
                if verbose: print("add_missing_parentheses, mul/div, wrap left argument, end" + self.expr)

                # wrap right argument
                if verbose: print("add_missing_parentheses, mul/div, wrap right argument, start" + self.expr)
                if mul_div_index + 1 <= len(self.expr) and not self.expr[mul_div_index + 1] == "(":
                    right_index = mul_div_index + 1
                    while right_index < len(self.expr) and is_digit(self.expr[right_index]):
                        right_index += 1
                    self.expr = self.expr[:mul_div_index + 1] + "(" + self.expr[mul_div_index + 1:right_index] + ")" + self.expr[right_index:]
                    mul_div_index += 2
                if verbose: print("add_missing_parentheses, mul/div, wrap right argument, end" + self.expr)
            mul_div_index += 1

        # wrap left, right argument and mul/div operator
        mul_div_index = 0
        while mul_div_index < len(self.expr):
            if self.expr[mul_div_index] == "*" or self.expr[mul_div_index] == "/":
                if verbose: print("add_missing_parentheses, mul/div, wrap left, right argument and mul/div operator, start" + self.expr)
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
                self.expr = self.expr[:left_index+1] + "(" + self.expr[left_index+1:right_index] + ")" + self.expr[right_index:]
                mul_div_index += 1
                if verbose: print("add_missing_parentheses, mul/div, wrap left, right argument and mul/div operator, end" + self.expr)
            mul_div_index += 1

        add_substr_index = 0
        while add_substr_index < len(self.expr):
            if self.expr[add_substr_index] == "+" or self.expr[add_substr_index] == "-":
                # wrap left argument
                if verbose: print("add_missing_parentheses, add/substr, wrap left argument, start" + self.expr)
                if 0 <= add_substr_index - 1 and not self.expr[add_substr_index - 1] == ")":
                    left_index = add_substr_index - 1
                    while left_index >= 0 and is_digit(self.expr[left_index]):
                        left_index += -1
                    self.expr = self.expr[:left_index + 1] + "(" + self.expr[left_index + 1:add_substr_index] + ")" + self.expr[add_substr_index:]
                    add_substr_index += 2
                if verbose: print("add_missing_parentheses, add/substr, wrap left argument, end" + self.expr)

                # wrap right argument
                if verbose: print("add_missing_parentheses, add/substr, wrap right argument, start" + self.expr)
                if add_substr_index + 1 <= len(self.expr) and not self.expr[add_substr_index + 1] == "(":
                    right_index = add_substr_index + 1
                    while right_index < len(self.expr) and is_digit(self.expr[right_index]):
                        right_index += 1
                    self.expr = self.expr[:add_substr_index + 1] + "(" + self.expr[add_substr_index + 1:right_index] + ")" + self.expr[right_index:]
                    add_substr_index += 2
                if verbose: print("add_missing_parentheses, add/substr, wrap right argument, end" + self.expr)

            add_substr_index += 1

        # wrap left, right argument and add/substr operator
        add_substr_index = 0
        while add_substr_index < len(self.expr):
            if self.expr[add_substr_index] == "+" or self.expr[add_substr_index] == "-":
                if verbose: print("add_missing_parentheses, add/substr, wrap left, right argument and add/substr operator, start" + self.expr)
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
                self.expr = self.expr[:left_index + 1] + "(" + self.expr[left_index + 1:right_index] + ")" + self.expr[right_index:]
                add_substr_index += 1
                if verbose: print("add_missing_parentheses, add/substr, wrap left, right argument and add/substr operator, end" + self.expr)
            add_substr_index += 1
        if verbose: print("add_missing_parentheses, end:\t\t " + self.expr)

    def remove_redundant_parentheses(self):
        if verbose: print("remove_redundant_parentheses, start: " + self.expr)
        # remove things like (1)
        index = 1
        while index < len(self.expr) - 1:
            if is_digit(self.expr[index]) and self.expr[index - 1] == "(":
                left_parenth_index = index - 1
                while not self.expr[index] == ")":
                    index += 1
                right_parenth_index = index
                if is_number(self.expr[left_parenth_index + 1:right_parenth_index - 1]):
                    self.expr = self.expr[:left_parenth_index] + self.expr[left_parenth_index + 1:right_parenth_index] + self.expr[right_parenth_index + 1:]
                    index += -1
            index += 1
        # remove things like ()
        index = 0
        while index < len(self.expr) - 1:
            if self.expr[index] == "(" and self.expr[index+1] == ")":
                self.expr = self.expr[:index] + self.expr[index+2:]
            index += 1
        # remove parenthesis wrapping whole expression
        if self.expr[0] == "(":
            index = 1
            parenth_counter = 1
            while index < len(self.expr):
                if self.expr[index] == "(":
                    parenth_counter += 1
                elif self.expr[index] == ")":
                    parenth_counter += -1
                if parenth_counter == 0 and index == len(self.expr):
                    self.expr = self.expr[1:len(self.expr) - 1]
                    if self.expr[0] == "(":
                        index = 1
                        parenth_counter = 1
                index += 1

        if verbose: print("remove_redundant_parentheses, end:\t " + self.expr)

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
        return self.expr

class ExpressionEvaluator:
    def __init__(self, expr):
        self.expr = expr
        self.stack = LifoQueue()     # stack for operators and parentheses
        self.output = Queue()        # FIFO queue implemented as a list

    def evaluate_expr(self):
        # this function is implementation of Reverse Polish Notation algorithm
        index = 0
        while index < len(self.expr):
            if is_digit(self.expr[index]):
                num_start = index
                index += 1
                while index < len(self.expr) and is_digit(self.expr[index]):
                    index += 1
                num_end = index - 1
                if is_number(self.expr[num_start:num_end]):
                    if num_end > num_start:
                        print("making integer from: " + self.expr[num_start:num_end])
                        number = int(self.expr[num_start:num_end])
                        self.output.put(number)
                else:
                    raise InvalidExpressionError
            '''elif self.expr[index] == "+" or self.expr[index] == "-" or self.expr[index] == "*" or self.expr[index] == "(":
                self.stack.put(self.expr[index])
            elif self.expr[index] == "/":
                operator = self.stack.get()
                self.output.put(operator)
                self.stack.put(self.expr[index])
            elif self.expr[index] == ")":
                operator = self.stack.get()
                self.output.put(operator)
                open_parenth = self.stack.get()
                if not open_parenth == "(":
                    raise ParenthesesError
            else:
                raise UnallowedCharacterError'''
            index += 1

        #while not self.stack.empty():
        #    element = self.stack.get()
        #    self.output.put(element)

        print(list(self.output.queue))
        return self.expr + "\n"
