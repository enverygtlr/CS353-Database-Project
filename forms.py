from flask_wtf import FlaskForm
from wtforms.fields import *
from wtforms.validators import *

class RegistrationForm(FlaskForm):
    fullname = StringField('Full Name', validators= [DataRequired(), Length(min = 5)])
    email = StringField('Email',validators=[DataRequired()] )
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    typee =  SelectField('Type', validators=[DataRequired()], choices=[('player', 'Normal user'), ('editor', 'Editor'), ('admin', 'Admin')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class PlayBetForm(FlaskForm):
    stake = IntegerField('stake', validators=[NumberRange(3), DataRequired()])

class SuggestionForm(FlaskForm):
    suggestion = TextField('suggestion', validators=[DataRequired()])

class SearchForm(FlaskForm):
    search = TextField('search', validators=[DataRequired()])

class OddForm(FlaskForm):
    odd = FloatField(description='New Odd')
    submit = SubmitField('Change Odd')
    hidden = HiddenField()

    

