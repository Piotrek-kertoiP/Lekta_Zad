from flask import Flask, request, abort

from custom_exceptions import ParenthesisError, UnallowedCharacterError
from endpoint_handlers import evaluate_expr, RequestValidator

app = Flask(__name__)

SERVER_PORT = "5000"

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/evaluate', methods=["POST"])
def evaluate_endpoint():
    try:
        rv = RequestValidator(request)
        expr = rv.validate_request()
        return evaluate_expr(expr)
    except KeyError:
        return abort(400, "Probably wrong json data has been provided in the request")
    except ParenthesisError:
        return abort(400, "Wrong parenthesis")
    except UnallowedCharacterError:
        return abort(400, "Characters other than {+,-,*,/,0-9,(,)} in the expression")


if __name__ == '__main__':
    app.run(port=SERVER_PORT)
