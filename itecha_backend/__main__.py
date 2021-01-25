import json
import sys
import traceback
from io import StringIO

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/test.db"
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120))


class Problem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text, nullable=False)


PROBLEMS = [
    {"id": 1, "title": "A+B problem", "content": "输入两个数a和b，输出他们的和"},
    {"id": 2, "title": "A*B problem", "content": "输入两个数a和b，输出他们的乘积"},
]


@app.route("/problems", methods=["GET"])
def problems():
    return PROBLEMS


@app.route("/python-executor", methods=["POST"])
def python_executor() -> bytes:
    request_obj: dict = json.loads(request.data)
    source = request_obj.get("source")
    code_input = request_obj.get("input", "")

    if not code_input.endswith("\n"):
        code_input += "\n"
    input_buffer = StringIO()
    input_buffer.write(code_input)
    input_buffer.seek(0)
    sys.stdin = input_buffer

    output_buffer = StringIO()
    sys.stdout = output_buffer
    sys.stderr = output_buffer

    try:
        exec(source, {})
    except Exception:
        traceback.print_exc()
    output = output_buffer.getvalue().encode()

    # Restore the original stdin and stdout
    sys.stdin = sys.__stdin__
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
