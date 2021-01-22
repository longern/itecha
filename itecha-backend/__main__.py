import sys
import traceback
from io import StringIO

from flask import Flask, request

app = Flask(__name__)

PROBLEMS = [
    {"id": 1, "title": "A+B problem", "content": "输入两个数a和b，输出他们的和"},
    {"id": 2, "title": "A*B problem", "content": "输入两个数a和b，输出他们的乘积"},
]


@app.route("/problems", methods=["GET"])
def problems():
    return PROBLEMS


@app.route("/python-executor", methods=["POST"])
def python_executor():
    code = request.data

    buffer = StringIO()
    sys.stdout = buffer
    sys.stderr = buffer

    try:
        exec(code, {})
    except Exception:
        traceback.print_exc()
    output = buffer.getvalue().encode()

    # Restore the original stdout
    sys.stdout = sys.__stdout__
    sys.stdout = sys.__stderr__

    return output


@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE")
    return response


if __name__ == "__main__":
    app.run(port=17362, debug=True)
