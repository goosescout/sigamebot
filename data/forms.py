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


class GameForm(FlaskForm):
    category = StringField('Name of Category', validators=[DataRequired()])
    description = TextAreaField('Description of Category', validators=[DataRequired()])
    submit = SubmitField('Add Category')
    text = TextAreaField('Wording of Question', validators=[DataRequired()])
    par = IntegerField('Value of Question', validators=[DataRequired()])
    answers = StringField('Possible answers on Question', validators=[DataRequired()])
    time = IntegerField('Time to answer on Question', validators=[DataRequired()])
    text_1 = TextAreaField('Wording of Question', validators=[DataRequired()])
    par_1 = IntegerField('Value of Question', validators=[DataRequired()])
    answers_1 = StringField('Possible answers on Question', validators=[DataRequired()])
    time_1 = IntegerField('Time to answer on Question', validators=[DataRequired()])
    text_2 = TextAreaField('Wording of Question', validators=[DataRequired()])
    par_2 = IntegerField('Value of Question', validators=[DataRequired()])
    answers_2 = StringField('Possible answers on Question', validators=[DataRequired()])
    time_2 = IntegerField('Time to answer on Question', validators=[DataRequired()])
    text_3 = TextAreaField('Wording of Question', validators=[DataRequired()])
    par_3 = IntegerField('Value of Question', validators=[DataRequired()])
    answers_3 = StringField('Possible answers on Question', validators=[DataRequired()])
    time_3 = IntegerField('Time to answer on Question', validators=[DataRequired()])
    text_4 = TextAreaField('Wording of Question', validators=[DataRequired()])
    par_4 = IntegerField('Value of Question', validators=[DataRequired()])
    answers_4 = StringField('Possible answers on Question', validators=[DataRequired()])
    time_4 = IntegerField('Time to answer on Question', validators=[DataRequired()])
    category_submit = SubmitField('Add Category')
    round_submit = SubmitField('Next round')
    finish_submit = SubmitField('Finish editing game')

class QuestionForm(FlaskForm):
    text = TextAreaField('Wording of Question', validators=[DataRequired()])
    par = IntegerField('Value of Question', validators=[DataRequired()])
    answers = StringField('Possible answers on Question', validators=[DataRequired()])
    time = IntegerField('Time to answer on Question', validators=[DataRequired()])


class SubmitForm(FlaskForm):
    submit = SubmitField('Add Category')
