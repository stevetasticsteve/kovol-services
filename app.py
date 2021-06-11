from flask import Flask
from flask import render_template

from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired

from phonemics import kovol_phonemics

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


@app.route("/verb-prediction")
def verb_prediction():
    return render_template('verb_prediction.html')


class PhonemicsForm(FlaskForm):
    phonemics = TextAreaField("Phonemic text", validators=[DataRequired()])
    submit = SubmitField("Submit")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)
