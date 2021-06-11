from flask import Flask
from flask import render_template
from flask import url_for


app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/phonemics")
def phonemics():
    return render_template('phonemics.html')

@app.route("/verb-prediction")
def verb_prediction():
    return render_template('verb_prediction.html')


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)
