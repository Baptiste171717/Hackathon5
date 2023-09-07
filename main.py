import os

from flask import Flask
from flask import request
from flask import flash
from flask import redirect
from flask import url_for
from flask import render_template
from src.utils.ask_question_to_pdf import ask_question_to_pdf
from werkzeug.utils import secure_filename


app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/nouveau")
def nouveau1():
    return render_template("upload_document.html")


@app.route("/action_page", methods=["POST"])
def upload():
    UPLOAD_FOLDER = "src/utils"
    file = request.files["filename"]
    file.save(os.path.join(os.path.dirname(__file__), UPLOAD_FOLDER, "filename.pdf"))
    return redirect("/")


@app.route("/image")
def image():
    return "<p>l</p>"


@app.route("/prompt", methods=["GET", "PATCH", "DELETE", "POST"])
def prompt():
    # print(ask_question_to_pdf("Are you a teacher"))
    question = request.form["prompt"]
    return {"answer": ask_question_to_pdf(question)}


@app.route("/question", methods=["GET"])
def question():
    question = "Pose moi une question sur le texte"
    print(question)
    return {"answer": ask_question_to_pdf(question)}


@app.route("/answer", methods=["POST"])
def answer():
    app.logger.info(request.form)
    question = request.form["question"]
    answer = request.form["prompt"]
    fgt = (
        "question:"
        + question
        + "\n"
        + "réponse:"
        + answer
        + "\n"
        + "Ma réponse est-elle juste?"
    )
    app.logger.info(fgt)
    return {"answer": ask_question_to_pdf(fgt)}
