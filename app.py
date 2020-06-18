import traceback
from flask import Flask, request, abort
from custom_exceptions import ParenthesesError, UnallowedCharacterError, MissingOperationArgumentError, InvalidExpressionError
from endpoint_handlers import RequestValidator, ExpressionEvaluator

app = Flask(__name__)

SERVER_PORT = "5000"

@app.route('/evaluate', methods=["POST"])
def evaluate_endpoint():
    try:
        rv = RequestValidator(request)
        expr = rv.validate_request()
        ee = ExpressionEvaluator(expr)
        return ee.evaluate_expr()
    except KeyError:
        return abort(400, "Probably wrong json data has been provided in the request")
    except ParenthesesError:
        return abort(400, "Wrong parentheses")
    except UnallowedCharacterError:
        return abort(400, "Characters other than {+,-,*,/,0-9,(,)} in the expression")
    except MissingOperationArgumentError:
        return abort(400, "The expression is missing one or more arguments for an operator")
    except InvalidExpressionError:
        return abort(400, "There is some problem with the expression")
    except ZeroDivisionError:
        return abort(400, "You can't divide by zero")
    except Exception as e:
        return abort(400, "Unknown problem has occured; exception details\n" + traceback.print_exc())


if __name__ == '__main__':
    app.run(port=SERVER_PORT, threaded=True)
