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

class QuestionForm(FlaskForm):
    title = StringField('Question name', validators=[DataRequired()])
    par = IntegerField('Value of question', validators=[DataRequired()])
    text = TextAreaField('Question', validators=[DataRequired()])
    ans = StringField('Possible answers', validators=[DataRequired()])

class CategoryForm(FlaskForm):
    title = StringField('Category name', validators=[DataRequired()])
    description = TextAreaField('Description of category', validators=[DataRequired()])
