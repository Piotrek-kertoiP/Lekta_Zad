from flask import Flask
from flask import request
from endpoint_handlers import evaluate_expr

app = Flask(__name__)
SERVER_PORT = "5555"


@app.route('/evaluate', methods=["POST"])
def evaluate_endpoint():
    return evaluate_expr(request.json)


if __name__ == '__main__':
    app.run(port=SERVER_PORT)
