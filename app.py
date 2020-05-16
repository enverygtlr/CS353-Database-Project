from flask import Flask, render_template, request, session
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_session import Session
import psycopg2

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

bootstrap = Bootstrap(app)
moment = Moment(app)

app.config["SESSION PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
notes =[]

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    name = None
    form = NameForm()
    if session.get("notes") is None:
        session["notes"] = []

    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
    creators = ["Batuhan", "Berk", "Bombar", "Enver"]
    if request.method == "POST":
        note = request.form.get("note")
        session["notes"].append(note)
    return render_template('index.html', form=form, name=name, creators = creators, notes = session["notes"])

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name= name)

