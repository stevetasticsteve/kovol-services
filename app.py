from flask import Flask
from flask import request
from flask import render_template

from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, TextField
from wtforms.validators import DataRequired

import click
import sys
import os

# favour the local version of kovol-language-tools
sys.path.insert(0, os.path.join(os.getcwd(), "kovol-language-tools"))

from kovol_language_tools.phonemics import phonetics_to_orthography
from kovol_language_tools.verbs import (
    PredictedKovolVerb,
    HansenPredictedKovolVerb,
    get_data_from_csv,
)


app = Flask(__name__)
app.config["SECRET_KEY"] = "password"
app.debug = True


@click.command()
@click.option("--rules", default="steve")
def run_kovol_services(rules):
    global prediction_rules
    prediction_rules = rules
    app.run()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/phonemics", methods=["GET", "POST"])
def phonemics():
    data = None
    errors = None
    form = PhonemicsForm()
    if form.validate_on_submit():
        data = form.phonemics.data
        data, errors = phonetics_to_orthography(data, hard_fail=False)
    return render_template("phonemics.html", form=form, data=data, errors=errors)


@app.route("/verbs/prediction", methods=["GET", "POST"])
def verb_prediction():
    verb = None
    form = VerbPredictionForm()
    if form.validate_on_submit():
        first_remote_past = form.first_remote_past.data
        first_recent_past = form.first_recent_past.data
        verb = PredictedKovolVerb(first_remote_past, first_recent_past)
    return render_template("verbs/verb_prediction.html", form=form, verb=verb)


@app.route("/verbs")
def verb_index():
    return render_template("verbs/verb_index.html")


@app.route("/verbs/batch-predict")
def batch_prediction_comparison():
    verbs = get_csv_data()
    incorrectly_predicted_verbs = []
    correctly_predicted_verbs = []

    verbs = filter_verbs(verbs)

    for v in verbs:
        if prediction_rules == "philip":
            pv = HansenPredictedKovolVerb(
                v.remote_past_3p,
                english=v.english,
            )
        else:
            pv = PredictedKovolVerb(
                v.remote_past_1s, v.recent_past_1s, english=v.english
            )
        pv.get_prediction_errors(v)
        if pv.errors:
            incorrectly_predicted_verbs.append((pv, v))
        else:
            correctly_predicted_verbs.append(pv)
    accuracy = (len(correctly_predicted_verbs), len(incorrectly_predicted_verbs))
    return render_template(
        "verbs/prediction-comparison.html",
        incorrectly_predicted_verbs=incorrectly_predicted_verbs,
        correctly_predicted_verbs=correctly_predicted_verbs,
        accuracy=accuracy,
    )


@app.route("/verbs/verb-display")
def display_verbs():
    verbs = get_csv_data()
    verbs = filter_verbs(verbs)

    return render_template("verbs/verb_display.html", verbs=verbs)


def filter_verbs(verbs):
    filters = list(request.args)
    for v in verbs:
        v.predict_root(rules=prediction_rules)

    if "end" in filters:
        verbs = [v for v in verbs if v.root.endswith(request.args.get("end"))]
    if "start" in filters:
        verbs = [v for v in verbs if v.root.startswith(request.args.get("start"))]
    if "contains" in filters:
        verbs = [v for v in verbs if request.args.get("contains") in v.root]
    if "lv" in filters:
        verbs = [v for v in verbs if request.args.get("lv") in v.verb_vowels()]

    return verbs


def get_csv_data():
    try:
        verbs = get_data_from_csv("kovol_verbs/elicited_verbs.csv")
    except FileNotFoundError:
        verbs = get_data_from_csv("kovol_verbs/elicited_verbs_example.csv")
    finally:
        return verbs


class PhonemicsForm(FlaskForm):
    phonemics = TextAreaField("Phonemic text", validators=[DataRequired()])
    submit = SubmitField("Submit")


class VerbPredictionForm(FlaskForm):
    first_remote_past = TextField("1st person remote_past", validators=[DataRequired()])
    first_recent_past = TextField("1st person recent past", validators=[DataRequired()])
    submit = SubmitField("Submit")


if __name__ == "__main__":
    run_kovol_services()
