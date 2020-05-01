from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField, StringField, TextAreaField, IntegerField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import EmailField


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Log in')


class RegisterForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_again = PasswordField('Repeat password', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    about = TextAreaField('About me')
    submit = SubmitField('Log in')


class CategoryForm(FlaskForm):
    category = StringField('Name of Category', validators=[DataRequired()])
    description = TextAreaField('Description of Category', validators=[DataRequired()])


class QuestionForm(FlaskForm):
    text = TextAreaField('Wording of Question', validators=[DataRequired()])
    par = IntegerField('Value of Question', validators=[DataRequired()])
    answers = StringField('Possible answers on Question', validators=[DataRequired()])
    time = IntegerField('Time to answer on Question', validators=[DataRequired()])


class SubmitForm(FlaskForm):
    submit = SubmitField('Add Category')
