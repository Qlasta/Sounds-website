import os

import requests
from api_manager import generate_random_sound, authorize, download_sound
from flask import Flask, redirect, url_for, request, render_template, flash
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import SubmitField, StringField
from flask_bootstrap import Bootstrap
import os
sound_info = {}

# Authorizing for downloading from api
headers_for_download = authorize()


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECURE_KEY']
Bootstrap(app)

# Guess form configuration
class GuessForm(FlaskForm):
    guess = StringField(label = "Enter your guess", validators=[DataRequired()])
    submit = SubmitField(label='SUBMIT')


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["GET", "POST"])
def generate():
    global sound_info
    form = GuessForm()
    if request.method == "POST":

        # Checks user answer with random sound tags
        answer = form.guess.data
        if answer in sound_info["tags"]:
            win = 1
        else:
            win = 0
        print(answer)
        return render_template("index.html", tags=sound_info["tags"], descr=sound_info["description"], win=win)
    else:

        # Generates random sound and downloads it, holds sound info
        try:
            sound_info = generate_random_sound()
        except requests.exceptions.HTTPError:
            sound_info = generate_random_sound()
        file_name = sound_info["name"]
        download_sound(sound_info["id"], file_name, headers_for_download)
        print(file_name)
        print(sound_info["tags"])
        return render_template("index.html", sound=file_name, form=form)

if __name__ == "__main__":
    app.run(debug=True)