from flask import Flask
from flask import render_template

from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, TextField
from wtforms.validators import DataRequired

from phonemics import kovol_phonemics
from kovol_verbs import PredictedKovolVerb

app = Flask(__name__)
app.config['SECRET_KEY'] = 'password'


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/phonemics", methods=['GET', 'POST'])
def phonemics():
    data = None
    form = PhonemicsForm()
    if form.validate_on_submit():
        data = form.phonemics.data
        data = kovol_phonemics.phonetics_to_orthography(data)
    return render_template('phonemics.html', form=form, data=data)


@app.route("/verb-prediction", methods=['GET', 'POST'])
def verb_prediction():
    verb = None
    form = VerbPredictionForm()
    if form.validate_on_submit():
        first_remote_past = form.first_remote_past.data
        first_recent_past = form.first_recent_past.data
        verb = PredictedKovolVerb(first_remote_past, first_recent_past)
    return render_template('verb_prediction.html', form=form, verb=verb)


class PhonemicsForm(FlaskForm):
    phonemics = TextAreaField("Phonemic text", validators=[DataRequired()])
    submit = SubmitField("Submit")


class VerbPredictionForm(FlaskForm):
    first_remote_past = TextField("1st person remote_past", validators=[DataRequired()])
    first_recent_past = TextField("1st person recent past", validators=[DataRequired()])
    submit = SubmitField("Submit")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)
