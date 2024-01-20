from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, URL
from wtforms import PasswordField, SubmitField, StringField

class AddForm(FlaskForm):
    password = PasswordField(label="Admin Password", validators=[DataRequired()])
    submit = SubmitField(label="Submit")


class AddProjectForm(FlaskForm):
    project_name = StringField(label="Project Name", validators=[DataRequired()])
    project_description = StringField(label="Project Description", validators=[DataRequired()])
    project_url = StringField(label="Project URL")
    project_github = StringField(label="Project Github URL")
    password = PasswordField(label="Admin Password", validators=[DataRequired()])
    submit = SubmitField(label="Submit")
