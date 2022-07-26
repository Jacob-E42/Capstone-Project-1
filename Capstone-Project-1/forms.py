from flask_wtf import FlaskForm
# from routes.helpers import Unique
from wtforms import StringField, PasswordField, EmailField, TextAreaField, RadioField, DateTimeField, BooleanField, SelectField, SelectMultipleField, DateTimeLocalField
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
  phone = StringField("Phone Number", validators=[DataRequired(message="Phone number is required"), Length(min=10, max=12, message="Phone number should be entered as plain digits with no other characters")])
    
class CreateUserForm(FlaskForm):

  first_name = StringField("First Name", validators=[DataRequired(message="First name is required")])
  last_name = StringField("Last Name", validators=[DataRequired(message="Last name is required")])
  username = StringField("Username", validators=[DataRequired(message="Username is required"), Length(min=3, max=100, message="Username must be at least 3 characters long")])
  password = PasswordField("Password", validators=[Optional(), Length(min=6, max=50, message="Password length must be between 6 and 50 characters")])
  email = EmailField("Email", validators=[DataRequired(message="Email is required"), Email()])
  phone = StringField("Phone Number", validators=[DataRequired(message="Phone number is required"), Length(min=10, max=12, message="Phone number should be entered as plain digits with no other characters")])

class EditUserForm(FlaskForm):
  first_name = StringField("First Name", validators=[DataRequired(message="First name is required")])
  last_name = StringField("Last Name", validators=[DataRequired(message="Last name is required")])
  username = StringField("Username", validators=[DataRequired(message="Username is required"), Length(min=3, max=100, message="Username must be at least 3 characters long")])
  email = EmailField("Email", validators=[DataRequired(message="Email is required"), Email()])
  phone = StringField("Phone Number", validators=[DataRequired(message="Phone number is required"), Length(min=10, max=12, message="Phone number should be entered as plain digits with no other characters")])
    
class ChangePasswordForm(FlaskForm):
  previous_password = PasswordField("Previous password", validators=[DataRequired(message="Old password is required"), Length(min=6, max=50, message="Password length must be between 6 and 50 characters")])
  first_password = PasswordField("New password", validators=[DataRequired(message="Password is required"), Length(min=6, max=50, message="Password length must be between 6 and 50 characters")])
  second_password = PasswordField("Confirm New password", validators=[DataRequired(message="Password is required"), EqualTo('first_password', message="The two passwords don't match."), Length(min=6, max=50, message="Password length must be between 6 and 50 characters")])

class CreateTaskForm(FlaskForm):

  title = StringField("Title", validators=[DataRequired(message="Title is required")])
  description = TextAreaField("Description", validators=[])
  resp_type = SelectField("Type", choices=[("personal","Personal"), ("organizational", "Organizational")])
  due_time = DateTimeLocalField("Time Due", format='%Y-%m-%dT%H:%M', validators=[DataRequired(message="A due time is required")])
  is_completed = BooleanField("Completed")

class EditTaskForm(FlaskForm):
  title = StringField("Title", validators=[DataRequired(message="Title is required")])
  description = TextAreaField("Description", validators=[])
  resp_type = SelectField("Type", choices=[("personal","Personal"), ("organizational", "Organizational")])
  due_time = DateTimeLocalField("Date Due", format='%Y-%m-%dT%H:%M', validators=[DataRequired(message="A due time is required")])
  is_completed = BooleanField("Completed")

class AssignTaskForm(FlaskForm):
  assignee_id = SelectField("Assign To", coerce=int)
  remind_daily = BooleanField("Remind Daily")
  notify_admin = BooleanField("Notify Admin When Completed")

class AssignUserForm(FlaskForm):
  task_id = SelectField("Assign Task", coerce=int)
  remind_daily = BooleanField("Remind Daily")
  notify_admin = BooleanField("Notify Admin When Completed")

class EditTaskAssignmentForm(FlaskForm):
  
  remind_daily = BooleanField("Remind Daily")
  notify_admin = BooleanField("Notify Admin When Completed")

class EditUserAssignmentForm(FlaskForm):

  remind_daily = BooleanField("Remind Daily")
  notify_admin = BooleanField("Notify Admin When Completed")

 