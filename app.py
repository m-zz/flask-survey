from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []

@app.route("/")
def start():
    return render_template("survey_start.html", title = survey.title, instructions = survey.instructions)

@app.route("/begin", methods = ["POST"])
def begin():
    return redirect("/questions/0")

@app.route("/questions/<int:index>")
def question(index):
    print("hi")
    current_index = index
    current_question = survey.questions[current_index]
    return render_template("question.html", question = current_question)

@app.route("/answer", methods = ["POST"])
def answer():
    responses.append(request.form["answer"])
    print(responses)
    return redirect(f"questions/{len(responses)}")

