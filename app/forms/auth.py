"""At this time, we're not using flask-login.  TODO: implement auth system."""

from flask_wtf import FlaskForm
from wtforms.fields import PasswordField, StringField
from wtforms.validators import InputRequired


class LoginForm(FlaskForm):
    email = StringField(label="Email:", validators=[InputRequired()])
    password = PasswordField(label="Password:", validators=[InputRequired()])


class NewUserForm(FlaskForm):
    username = StringField(label="Username:", validators=[InputRequired()])
    email = StringField(label="Email:", validators=[InputRequired()])
    password = PasswordField(label="Password:", validators=[InputRequired()])
