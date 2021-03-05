from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

@app.route("/")
def select_survey():
    session["responses"] = []
    session["comments"] = []
    return render_template("select_survey.html", titles=survey.keys())

@app.route("/start")
def start():

    survey_id = request.args["survey_id"]
    correct_survey = survey[survey_id]

    return render_template("survey_start.html", title = correct_survey.title, instructions = correct_survey.instructions, survey_id=survey_id)

@app.route("/<survey_id>/begin", methods = ["POST"])
def begin(survey_id):
    return redirect(f"/{survey_id}/questions/0")

@app.route("/<survey_id>/questions/<int:index>")
def question(survey_id, index):
    current_index = index
    if current_index != len(session["responses"]):
        flash("You're trying to visit an invalid question")
        return redirect(f"/{survey_id}/questions/{len(session['responses'])}")
    current_question = survey[survey_id].questions[current_index]
    return render_template("question.html", question = current_question, survey_id=survey_id)

@app.route("/<survey_id>/answer", methods = ["POST"])
def answer(survey_id):
    responses = session["responses"]
    responses.append(request.form["answer"])
    session["responses"] = responses
    
    comments = session["comments"]
    comments.append(request.form.get("comment", ""))
    session["comments"] = comments

    if len(session["responses"]) < len(survey[survey_id].questions):
        return redirect(f"/{survey_id}/questions/{len(session['responses'])}")
    
    return redirect(f"/{survey_id}/completion")

@app.route("/<survey_id>/completion")
def completion(survey_id):
    
    return render_template("completion.html", questions = survey[survey_id].questions, 
    length = len(survey[survey_id].questions))

