from flask import Flask
from flask import request
from flask import render_template
from src.utils.ask_question_to_pdf import ask_question_to_pdf

app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/image")
def image():
    return "<p>l</p>"


@app.route("/prompt", methods=["GET", "PATCH", "DELETE", "POST"])
def prompt():
    return {"answer": ask_question_to_pdf(request.form["prompt"])}
