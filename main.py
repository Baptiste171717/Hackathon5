from flask import Flask, send_file
import os
from flask import request

# from flask import flash
from flask import redirect

# from flask import url_for
from flask import render_template
from src.utils.ask_question_to_pdf import ask_question_to_pdf, find_doc
import json

app = Flask(__name__)


@app.route("/document_choice")
def choose_file():
    return render_template("choose_file.html", Liste_pdf=find_doc())


chosen_file = "filename.pdf"


@app.route("/choose_files", methods=["POST"])
def chose_file():
    global chosen_file
    chosen_file = request.form["files"]
    return redirect("/")


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/nouveau")
def nouveau1():
    return render_template("upload_document.html")


@app.route("/action_page", methods=["POST"])
def upload():
    UP = "src/utils"
    file = request.files["filename"]
    file.save(os.path.join(os.path.dirname(__file__), UP, file.filename))
    return redirect("/document_choice")


@app.route("/image")
def serve_image():
    return send_file("static/description.jpg", mimetype="image/jpeg")


@app.route("/prompt", methods=["GET", "PATCH", "DELETE", "POST"])
def prompt():
    # print(ask_question_to_pdf("Are you a teacher"))
    question = request.form["prompt"]
    return {"answer": ask_question_to_pdf(question, chosen_file)}


@app.route("/question", methods=["GET"])
def question():
    question = "Pose moi une question sur le texte"
    print(question)
    return {"answer": ask_question_to_pdf(question, chosen_file)}


@app.route("/answer", methods=["POST"])
def answer():
    app.logger.info(request.form)
    question = request.form["question"]
    answer = request.form["prompt"]
    command = (
        "question:"
        + question
        + "\n"
        + "réponse:"
        + answer
        + "\n"
        + "Ma réponse est-elle juste?"
    )
    app.logger.info(command)
    return {"answer": ask_question_to_pdf(command, chosen_file)}


@app.route("/indice", methods=["POST"])
def indice():
    data = json.loads(request.data)
    app.logger.info(data)
    question = data["question"]
    command = (
        "peux-tu me donner un indice incomplet sans me donner "
        + "la réponse (en moins de 30 caractères) ?"
        + "/n"
        + question
        + "/n"
        + "j'insiste sur le fait que l'indice que tu "
        + "donnes ne doive pas répondre à la question"
    )
    app.logger.info(command)
    return {"answer": ask_question_to_pdf(command)}
