from flask import Flask, send_file
from flask import request
from flask import render_template
from src.utils.ask_question_to_pdf import ask_question_to_pdf
import json

app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/image")
def serve_image():
    return send_file("static/description.jpg", mimetype="image/jpeg")


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


@app.route("/indice", methods=["POST"])
def indice():
    data = json.loads(request.data)
    app.logger.info(data)
    question = data["question"]
    fgt = (
        "peux-tu me donner un indice incomplet sans me donner la réponse (en moins de 30 caractères) ?"
        + "/n"
        + question
        + "/n"
        + "j'insiste sur le fait que l'indice que tu donnes ne doive pas répondre à la question"
    )
    app.logger.info(fgt)
    return {"answer": ask_question_to_pdf(fgt)}
