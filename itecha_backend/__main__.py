import datetime
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
    testcases = db.Column(db.Text)
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
            "testcases": json.loads(problem.testcases),
        }
    )


@app.route("/problems", methods=["POST"])
def create_problems() -> str:
    problem_dict: dict = json.loads(request.data)
    if "testcases" in problem_dict:
        problem_dict["testcases"] = json.dumps(problem_dict["testcases"])
    problem = Problem(**problem_dict)
    db.session.add(problem)
    db.session.commit()
    return ("", 204)


@app.route("/problems/<id>", methods=["PUT"])
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


@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE")
    return response


if __name__ == "__main__":
    app.run(port=17362, debug=True)
