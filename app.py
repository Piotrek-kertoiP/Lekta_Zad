from flask import Flask, request, abort

from endpoint_handlers import evaluate_expr

app = Flask(__name__)

SERVER_PORT = "5000"

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/evaluate', methods=["POST"])
def evaluate_endpoint():
    try:
        return evaluate_expr(request)
    except KeyError:
        return abort(400)


if __name__ == '__main__':
    app.run(port=SERVER_PORT)
