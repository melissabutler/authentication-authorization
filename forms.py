from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Length

class RegisterUserForm(FlaskForm):
    """ Form for adding User"""
    username = StringField("Username", validators=[InputRequired(), Length(min=1, max=20)])
    password = PasswordField("Password", validators=[InputRequired()])
    email = EmailField("Email", validators=[InputRequired(), Length(min=1, max=50)])
    first_name = StringField("First Name", validators=[InputRequired(), Length(min=1,max=30)])
    last_name = StringField("Last Name", validators=[InputRequired(), Length(min=1,max=30)])


class LoginForm(FlaskForm):
    """ Form for logging in user"""
    username = StringField("Username", validators=[InputRequired(), Length(min=1, max=20)])
    password = PasswordField("Password", validators=[InputRequired()])

class FeedbackForm(FlaskForm):
    """ Form for inputting feedback """
    title = StringField("Title", validators=[InputRequired(), Length(min=1, max=100)])
    content = TextAreaField("Content", validators=[InputRequired()])
