import datetime
import hashlib
import json
import logging
import os
import re
import sys
import time
import traceback
from functools import wraps
from io import StringIO

from flask import Flask, request
from flask.helpers import send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, gen_salt, generate_password_hash
from werkzeug.exceptions import (
    HTTPException,
    BadRequest,
    Unauthorized,
    UnprocessableEntity,
)

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv(
    "SECRET_KEY", "f5xl2fa-=5-lt1n!ucyzv%kz(t=2p4u#tqr$7!vj*a*wmiufr#"
)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120))


class Problem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text, nullable=False)
    default_code = db.Column(db.Text)
    testcases = db.Column(db.Text)
    hidden_code = db.Column(db.Text)
    submissions = db.relationship("Submission", back_populates="problem")


class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Text)
    creator_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    creator = db.relationship("User")
    creator_ip = db.Column(db.String(20))
    problem_id = db.Column(db.Integer, db.ForeignKey("problem.id"))
    problem = db.relationship("Problem", back_populates="submissions")
    create_time = db.Column(
        db.TIMESTAMP(), nullable=False, server_default=db.text("CURRENT_TIMESTAMP")
    )


@app.route("/login", methods=["POST"])
def login():
    body: dict = request.json
    logging.info("Logging username: %s", body.get("username"))

    if not body.get("username"):
        raise UnprocessableEntity([{"field": "username", "message": "Empty username."}])

    user = User.query.filter_by(username=body.get("username")).first()

    if not user:  # User not found
        raise UnprocessableEntity([{"field": "username", "message": "User not found."}])

    if not check_password_hash(user.password, body.get("password")):
        raise UnprocessableEntity(
            [{"field": "password", "message": "Incorrect password."}]
        )

    timestamp = int(time.time())
    salt = gen_salt(8)
    token = hashlib.sha256(
        f"{user.id}{timestamp}{salt}{app.config['SECRET_KEY']}".encode()
    ).hexdigest()

    return {"token": f"{user.id},{timestamp},{salt},{token}"}


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        match = re.match(
            "Bearer ([^,]*),([^,]*),([^,]*),([^,]*)",
            request.headers.get("Authorization", ""),
        )
        if not match:
            raise Unauthorized()

        user_id, timestamp, salt, token = match.groups()
        expected_token = hashlib.sha256(
            f"{user_id}{timestamp}{salt}{app.config['SECRET_KEY']}".encode()
        ).hexdigest()
        if token != expected_token or time.time() - timestamp >= 86400:
            raise Unauthorized()

        return func(*args, **kwargs)

    return wrapper


@app.route("/users", methods=["POST"])
def create_user() -> str:
    user_dict: dict = json.loads(request.data)
    if "username" not in user_dict or "password" not in user_dict:
        raise BadRequest()
    user = User(
        username=user_dict["username"],
        password=generate_password_hash(user_dict["password"]),
    )
    db.session.add(user)
    db.session.commit()
    return ("", 204)


@app.route("/users/<id>", methods=["GET"])
def user(id: str) -> str:
    user = User.query.filter_by(id=id).first()
    if not user:
        return ("Not Found", 404)
    return json.dumps(
        {
            "id": user.id,
            "username": user.username,
        }
    )


@app.route("/problems/<id>", methods=["GET"])
def problem(id: str) -> str:
    problem = Problem.query.filter_by(id=id).first()
    if not problem:
        return ("Not Found", 404)
    return json.dumps(
        {
            "id": problem.id,
            "title": problem.title,
            "content": problem.content,
            "default_code": problem.default_code,
            "testcases": json.loads(problem.testcases),
            "hidden_code": problem.hidden_code,
        }
    )


@app.route("/problems", methods=["POST"])
@login_required
def create_problems() -> str:
    problem_dict: dict = json.loads(request.data)
    if "testcases" in problem_dict:
        problem_dict["testcases"] = json.dumps(problem_dict["testcases"])
    problem = Problem(**problem_dict)
    db.session.add(problem)
    db.session.commit()
    return ("", 204)


@app.route("/problems/<id>", methods=["PUT"])
@login_required
def update_problems(id: str) -> str:
    problem_dict: dict = json.loads(request.data)
    if "testcases" in problem_dict:
        problem_dict["testcases"] = json.dumps(problem_dict["testcases"])
    problem = Problem.query.get(id)
    for key, value in problem_dict.items():
        if key != "id":
            setattr(problem, key, value)
    db.session.commit()
    return json.dumps(
        {"id": problem.id, "title": problem.title, "content": problem.content}
    )


@app.route("/problems", methods=["GET"])
def list_problems() -> str:
    return json.dumps(
        {
            "data": [
                {"id": problem.id, "title": problem.title, "content": problem.content}
                for problem in Problem.query.all()
            ]
        }
    )


@app.route("/submissions", methods=["POST"])
def create_submission() -> str:
    submission_dict = json.loads(request.data)
    submission = Submission(creator_ip=request.remote_addr, **submission_dict)
    print(submission_dict)
    db.session.add(submission)
    db.session.commit()
    return ("", 204)


@app.route("/submissions", methods=["GET"])
def list_submissions() -> str:
    return json.dumps(
        {
            "data": [
                {
                    "id": submission.id,
                    "problem_id": submission.problem_id,
                    "code": submission.code,
                    "creator_ip": submission.creator_ip,
                    "create_time": submission.create_time.replace(
                        tzinfo=datetime.timezone.utc
                    ).isoformat(),
                }
                for submission in Submission.query.all()
            ]
        }
    )


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


@app.route("/", defaults={"path": "index.html"})
@app.route("/<path:path>")
def index(path):
    return send_from_directory("static", path, as_attachment=False)


@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE")
    return response


@app.errorhandler(HTTPException)
def handle_exception(exception: HTTPException):
    return (
        {"name": exception.__class__.__name__, "message": exception.description},
        exception.code,
    )


if __name__ == "__main__":
    app.run(port=17362, debug=True)
