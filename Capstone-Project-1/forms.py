from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, PasswordField, EmailField
from models import User, Task, Assignment, db
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange, Optional, URL, AnyOf, NoneOf, Regexp



class LoginForm(FlaskForm):

  username = StringField("Username", validators=[DataRequired(message="Username is required"), Length(min=3, max=100, message="Username must be at least 3 characters long")])
  password = PasswordField("Password", validators=[DataRequired(message="Password is required"), Length(min=6, max=50, message="Password length must be between 6 and 50 characters")])

class SignupForm(FlaskForm):

  first_name = StringField("First Name", validators=[DataRequired(message="First name is required")])
  last_name = StringField("Last Name", validators=[DataRequired(message="Last name is required")])
  username = StringField("Username", validators=[DataRequired(message="Username is required"), Length(min=3, max=100, message="Username must be at least 3 characters long")])
  password = PasswordField("Password", validators=[DataRequired(message="Password is required"), Length(min=6, max=50, message="Password length must be between 6 and 50 characters")])
  email = EmailField("Email", validators=[DataRequired(message="Email is required"), Email()])
  phone = StringField("Phone Number", validators=[DataRequired(message="Phone number is required"), Length(min=10, max=10, message="Phone number should be entered as plain digits with no other characters")])
    


