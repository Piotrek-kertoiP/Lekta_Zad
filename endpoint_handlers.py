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
        i = 1
        while i < len(self.expr) - 1:
            if is_digit(self.expr[i]) and self.expr[i - 1] == "(":
                left_parenth_index = i - 1
                while not self.expr[i] == ")":
                    i += 1
                right_parenth_index = i
                if is_number(self.expr[left_parenth_index + 1:right_parenth_index - 1]):
                    self.expr = self.expr[:left_parenth_index] + self.expr[left_parenth_index + 1:right_parenth_index] + self.expr[right_parenth_index + 1:]
                    i += -1
            i += 1
        # remove things like ()
        i = 0
        while i < len(self.expr) - 1:
            if self.expr[i] == "(" and self.expr[i+1] == ")":
                self.expr = self.expr[:i] + self.expr[i+2:]
            i += 1
        # remove parenthesis wrapping whole expression
        if self.expr[0] == "(":
            i = 1
            parenth_counter = 1
            while i < len(self.expr):
                if self.expr[i] == "(":
                    parenth_counter += 1
                elif self.expr[i] == ")":
                    parenth_counter += -1
                if parenth_counter == 0 and i == len(self.expr):
                    self.expr = self.expr[1:len(self.expr) - 1]
                    if self.expr[0] == "(":
                        i = 1
                        parenth_counter = 1
                i += 1
        # remove double parenthesis like ((xyz))
        '''checked_chars = 0
        while checked_chars < len(self.expr) - 3:
            if self.expr[checked_chars] == "(":
                if verbose: print("remove_double_parentheses, start:\t " + self.expr)
                index = checked_chars + 1
                parenth_start = checked_chars
                parenth_counter = 1
                while index < len(self.expr) and not parenth_counter == 0:
                    if self.expr[index] == "(":
                        parenth_counter += 1
                    elif self.expr[index] == ")":
                        parenth_counter += -1
                    if parenth_counter == 0:
                        parenth_end = index
                        if self.expr[parenth_start + 1] == "(" and self.expr[parenth_end - 1] == ")":       #todo: bug here
                            self.expr = self.expr[:parenth_start] + self.expr[parenth_start + 1:parenth_end - 1] + self.expr[parenth_end:]
                            continue
                            # we checked 1 char but we also shortened the string so checked_chars remains the same
                        else:
                            checked_chars += 1
                    index += 1
                
                if verbose: print("remove_double_parentheses, end:\t\t " + self.expr)
            else:
                checked_chars += 1'''
        i = 1
        while i < len(self.expr) - 1:
            if verbose: print("remove_redundant_parentheses, end:\t " + self.expr)
            if self.expr[i] == "(" and self.expr[i - 1] == "(":
                parenth_start = i
                j = i + 1
                parenth_counter = 1
                while not parenth_counter == 0:
                    if self.expr[j] == "(":
                        parenth_counter += 1
                    if self.expr[j] == ")":
                        parenth_counter += -1
                    j += 1
                parenth_end = j - 1
                if j < len(self.expr) and self.expr[j] == ")":
                    self.expr = self.expr[:parenth_start - 1] + self.expr[parenth_start:parenth_end] + self.expr[parenth_end + 1:]
                    i += -1
            i += 1
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
        self.output = Queue()        # FIFO queue

    def print_logs(self, found_item):
        print("found: " + found_item)
        print("stack = " + str(list(self.stack.queue)))
        print("output = " + str(list(self.output.queue)))

    def convert_to_RPN(self):
        # this function is implementation of Reverse Polish Notation algorithm
        index = 0
        while index < len(self.expr):
            if is_digit(self.expr[index]):
                num_start = index
                index += 1
                while index < len(self.expr) and is_digit(self.expr[index]):
                    index += 1
                index += -1
                num_end = index
                if num_end > num_start:
                    number = int(self.expr[num_start:num_end+1])
                    self.output.put(number)
                elif num_end == num_start:
                    number = int(self.expr[num_start])
                    self.output.put(number)

                if verbose: self.print_logs(str(number))
            elif self.expr[index] == "(":
                self.stack.put(self.expr[index])

                if verbose: self.print_logs(self.expr[index])
            elif self.expr[index] == ")":
                while not self.stack.empty():
                    operator = self.stack.get()
                    if not operator == "(":
                        self.output.put(operator)
                    else:
                        break
                else:
                    raise InvalidExpressionError

                if verbose: self.print_logs(self.expr[index])
            elif self.expr[index] == "+" or self.expr[index] == "-":
                if self.stack.empty():
                    self.stack.put(self.expr[index])
                elif self.stack.get() == "(":
                    self.stack.put("(")
                    self.stack.put(self.expr[index])
                else:
                    self.stack.put(self.expr[index])

                if verbose: self.print_logs(self.expr[index])
            elif self.expr[index] == "*" or self.expr[index] == "/":
                if self.stack.empty():
                    self.stack.put(self.expr[index])
                else:
                    stack_top = self.stack.get()
                    if stack_top == "+" or stack_top == "-" or stack_top == "(" or stack_top == ")":
                        self.stack.put(stack_top)
                        self.stack.put(self.expr[index])
                    else:
                        self.output.put(stack_top)
                        self.stack.put(self.expr[index])

                if verbose: self.print_logs(self.expr[index])
            else:
                raise UnallowedCharacterError
            index += 1

        while not self.stack.empty():
            element = self.stack.get()
            self.output.put(element)
        print(list(self.output.queue))

    def compute_RPN(self):
        while not self.output.empty():
            print("output = " + str(list(self.output.queue)))
            print("stack = " + str(list(self.stack.queue)))

            element = self.output.get()
            if not is_operator(element):
                self.stack.put(element)
            else:
                right_argument = self.stack.get()
                left_argument = self.stack.get()
                if element == "+":
                    result = left_argument + right_argument
                elif element == "-":
                    result = left_argument - right_argument
                elif element == "*":
                    result = left_argument * right_argument
                elif element == "/":
                    result = left_argument / right_argument
                self.stack.put(result)
        print("output = " + str(list(self.output.queue)))
        print("stack = " + str(list(self.stack.queue)))

        print("self.stack.qsize() = " + str(self.stack.qsize()))
        print("self.output.qsize() = " + str(self.output.qsize()))
        if not (self.stack.qsize() == 1 and self.output.qsize() == 0):
            raise InvalidExpressionError

        return self.stack.get()

    def evaluate_expr(self):
        self.convert_to_RPN()   #converts expression as string to queue in Reversed Polish Notation
        result = self.compute_RPN()
        return str(result) + "\n"

