from flask import Flask
from flask import request
from flask import render_template

from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, TextField
from wtforms.validators import DataRequired

local_package = True
if local_package:
    import sys
    path_root = '/home/steve/Documents/Computing/Python_projects/python_CLA/kovol-language-tools'
    sys.path.append(path_root)

from kovol_language_tools.phonemics import phonetics_to_orthography
from kovol_language_tools.verbs import PredictedKovolVerb, get_data_from_csv



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
        data, errors = phonetics_to_orthography(data, hard_fail=False)
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
    verbs = get_data_from_csv("kovol_verbs/elicited_verbs.csv")
    incorrectly_predicted_verbs = []
    correctly_predicted_verbs = []
    # Optional query strings can be passed
    root_ending_filter = request.args.get('ending')

    for v in verbs:
        pv = PredictedKovolVerb(v.remote_past_1s, v.recent_past_1s, english=v.english)
        pv.get_prediction_errors(v)
        if root_ending_filter:
            if not pv.root.endswith(root_ending_filter):
                continue
        if pv.errors:
            incorrectly_predicted_verbs.append((pv, v))
        else:
            correctly_predicted_verbs.append(pv)
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
