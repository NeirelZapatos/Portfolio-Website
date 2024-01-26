from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, URL, Email
from wtforms import PasswordField, SubmitField, StringField, EmailField
import email_validator


class AdminForm(FlaskForm):
    password = PasswordField(label="Admin Password", validators=[DataRequired()])
    submit = SubmitField(label="Submit")


class AddProjectForm(FlaskForm):
    project_name = StringField(label="Project Name", validators=[DataRequired()])
    project_description = StringField(label="Project Description", validators=[DataRequired()])
    project_url = StringField(label="Project URL")
    project_github = StringField(label="Project Github URL")
    password = PasswordField(label="Admin Password", validators=[DataRequired()])
    submit = SubmitField(label="Submit")


class EmailForm(FlaskForm):
    email = EmailField(label="Email", validators=[Email(granular_message=True)])
    message = StringField(label="Message", validators=[DataRequired()])
    submit = SubmitField(label="Send")
