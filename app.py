from flask import Flask
from flask import request
from flask import render_template

from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, TextField, RadioField
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
def run_kovol_services():
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
    stanley_form = StanleyVerbPredictionForm()
    hansen_form = HansenVerbPredictionForm()

    if stanley_form.stanley_submit.data and stanley_form.validate_on_submit():
        past_1s = stanley_form.first_remote_past.data
        recent_1s = stanley_form.first_recent_past.data
        verb = PredictedKovolVerb(past_1s, recent_1s)

    if hansen_form.hansen_submit.data and hansen_form.validate_on_submit():
        future_3p = hansen_form.future_3p.data
        verb = HansenPredictedKovolVerb(future_3p)
        
    return render_template(
        "verbs/verb_prediction.html",
        stanley_form=stanley_form,
        hansen_form=hansen_form,
        verb=verb,
    )


@app.route("/verbs")
def verb_index():
    return render_template("verbs/verb_index.html")


@app.route("/verbs/batch-predict", methods=["GET", "POST"])
def batch_prediction_comparison():
    verbs = get_csv_data()
    incorrectly_predicted_verbs = []
    correctly_predicted_verbs = []
    form = PredictionSelectionForm()

    prediction_rules = "hansen"
    if form.validate():
        if form.radio.data == "Stanley":
            prediction_rules = "stanley"

    verbs = filter_verbs(verbs, prediction_rules)

    for v in verbs:
        if prediction_rules == "hansen":
            pv = HansenPredictedKovolVerb(
                v.future_3p,
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
        form=form,
    )


@app.route("/verbs/verb-display", methods=["GET", "POST"])
def display_verbs():
    verbs = get_csv_data()

    form = PredictionSelectionForm()
    prediction_rules = "hansen"

    if form.validate():
        if form.radio.data == "Stanley":
            prediction_rules = "stanley"
    verbs = filter_verbs(verbs, prediction_rules)

    return render_template("verbs/verb_display.html", verbs=verbs, form=form)


def filter_verbs(verbs, rules):
    filters = list(request.args)
    for v in verbs:
        v.predict_root(rules=rules)

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


class StanleyVerbPredictionForm(FlaskForm):
    first_remote_past = TextField("1st person past", validators=[DataRequired()])
    first_recent_past = TextField("1st person recent", validators=[DataRequired()])
    stanley_submit = SubmitField("Go")


class HansenVerbPredictionForm(FlaskForm):
    future_3p = TextField("3rd person future", validators=[DataRequired()])
    hansen_submit = SubmitField("Go")


class PredictionSelectionForm(FlaskForm):
    radio = RadioField(
        "Label",
        choices=[("Hansen", "Hansen prediction"), ("Stanley", "Stanley prediction")],
        default="Hansen",
    )


if __name__ == "__main__":
    run_kovol_services()
