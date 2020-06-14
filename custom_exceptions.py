class InvalidExpressionError(Exception):
    pass

class ParenthesesError(InvalidExpressionError):
    pass

class UnallowedCharacterError(InvalidExpressionError):
    pass

class MissingOperationArgumentError(InvalidExpressionError):
    pass


