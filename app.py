from flask import Flask
from flask import render_template

from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, TextField
from wtforms.validators import DataRequired

from phonemics import kovol_phonemics
from kovol_verbs.kovol_verbs import PredictedKovolVerb
from kovol_verbs import get_verb_data

app = Flask(__name__)
app.config["SECRET_KEY"] = "password"


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
        data, errors = kovol_phonemics.phonetics_to_orthography(data, hard_fail=False)
    return render_template("phonemics.html", form=form, data=data, errors=errors)


@app.route("/verb-prediction", methods=["GET", "POST"])
def verb_prediction():
    verb = None
    form = VerbPredictionForm()
    if form.validate_on_submit():
        first_remote_past = form.first_remote_past.data
        first_recent_past = form.first_recent_past.data
        verb = PredictedKovolVerb(first_remote_past, first_recent_past)
    return render_template("verb_prediction/verb_prediction.html", form=form, verb=verb)


@app.route("/verb-prediciton/batch-compare")
def batch_prediction_comparison():
    verbs = get_verb_data.get_data_from_csv()
    incorrectly_predicted_verbs = []
    correctly_predicted_verbs = []
    for v in verbs:
        pv = PredictedKovolVerb(v.remote_past_1s, v.recent_past_1s, english=v.english)
        pv.get_prediction_errors(v)
        if pv.errors:
            incorrectly_predicted_verbs.append((pv, v))
        else:
            correctly_predicted_verbs.append(v)
    accuracy = (len(correctly_predicted_verbs), len(incorrectly_predicted_verbs))
    return render_template(
        "verb_prediction/prediction-comparison.html",
        incorrectly_predicted_verbs=incorrectly_predicted_verbs,
        correctly_predicted_verbs=correctly_predicted_verbs,
        accuracy=accuracy,
    )


class PhonemicsForm(FlaskForm):
    phonemics = TextAreaField("Phonemic text", validators=[DataRequired()])
    submit = SubmitField("Submit")


class VerbPredictionForm(FlaskForm):
    first_remote_past = TextField("1st person remote_past", validators=[DataRequired()])
    first_recent_past = TextField("1st person recent past", validators=[DataRequired()])
    submit = SubmitField("Submit")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)
