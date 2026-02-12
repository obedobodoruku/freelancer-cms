from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, DateField, SelectField
from wtforms.validators import Email, EqualTo, Length, DataRequired, ValidationError, Regexp, Optional
from app.models import User
from datetime import date

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=5, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=4)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("This username already exists")
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("This email already taken")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=4)])
    remember = BooleanField("Remember me")
    submit = SubmitField("Login")


class CreateClientForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    phone = StringField("Phone", validators=[Optional(), Regexp(
            r'^\+?[0-9\s\-]+$',
            message="Invalid phone number format"
        )])
    note = TextAreaField("Note", validators=[Optional()])
    submit = SubmitField("Create Client")

class EditClientForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    phone = StringField("Phone", validators=[Optional(), Regexp(
            r'^\+?[0-9\s\-]+$',
            message="Invalid phone number format"
        )])
    note = TextAreaField("Note", validators=[Optional()])
    submit = SubmitField("Update Client")

class CreateProjectForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[Optional()])
    start_date = DateField("Start Date", default=date.today, validators=[DataRequired()], format="%Y-%m-%d")
    deadline = DateField("Deadline", validators=[Optional()], format="%Y-%m-%d")
    status = SelectField("Status", choices=[("pending", "Pending"), ("active", "Active"), ("completed", "Completed")], default="pending", validators=[DataRequired()])
    submit = SubmitField("Create Project")

class EditProjectForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[Optional()])
    start_date = DateField("Start Date", default=date.today, validators=[DataRequired()], format="%Y-%m-%d")
    deadline = DateField("Deadline", validators=[Optional()], format="%Y-%m-%d")
    status = SelectField("Status", choices=[("pending", "Pending"), ("active", "Active"), ("completed", "Completed")], default="pending", validators=[DataRequired()])
    submit = SubmitField("Update Project")

class CreateProjectTask(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    status = SelectField("Status", choices=[("todo", "Todo"), ("in-progress", "In-progress"), ("done", "Done")], default="todo", validators=[DataRequired()])
    due_date = DateField("Due date", validators=[Optional()], format="%Y-%m-%d")
    submit = SubmitField("Add task")

class EditTaskForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    status = SelectField("Status", choices=[("todo", "Todo"), ("in-progress", "In-progress"), ("done", "Done")], default="todo", validators=[DataRequired()])
    due_date = DateField("Due date", validators=[Optional()], format="%Y-%m-%d")
    submit = SubmitField("Update task")