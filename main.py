from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from forms import AdminForm, AddProjectForm, EmailForm
import smtplib
from email.mime.text import MIMEText
import os

EMAIL = os.environ.get("SEND_EMAIL")
EMAIL_PASSCODE = os.environ.get("EMAIL_PASSCODE")


app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("FLASK_KEY")
Bootstrap5(app)

admin_password = os.environ.get("ADMIN_PASSWORD")


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_URI", "sqlite:///posts.db")
db.init_app(app)


class Project(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    website_url: Mapped[str] = mapped_column(String, unique=False, nullable=True)
    github_url: Mapped[str] = mapped_column(String, unique=False, nullable=True)


with app.app_context():
    db.create_all()


# home page of website
@app.route("/")
def home():
    # new_project = Project(
    #     name="Testing",
    #     description="We don't really know",
    # )
    # db.session.add(new_project)
    # db.session.commit()
    list_of_projects = Project.query.all()
    return render_template("index.html", project_list=list_of_projects)


# form to add project
@app.route("/add-project", methods=["GET", "POST"])
def add_project():
    project_form = AddProjectForm()
    if project_form.validate_on_submit() and project_form.password.data == admin_password:
        new_project = Project(
            name=project_form.project_name.data,
            description=project_form.project_description.data,
            website_url=project_form.project_url.data,
            github_url=project_form.project_github.data
        )
        db.session.add(new_project)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add_project.html", form=project_form)


# displays project list with edit and delete functions
@app.route("/project-list", methods=["GET", "POST"])
def project_list():
    projects_to_delete = Project.query.all()
    return render_template("projects.html", projects=projects_to_delete)


# form to edit projects
@app.route("/edit/<int:project_id>", methods=["GET", "POST"])
def edit_project(project_id):
    project_to_edit = db.get_or_404(Project, project_id)
    edit_form = AddProjectForm(
        project_name=project_to_edit.name,
        project_description=project_to_edit.description,
        project_url=project_to_edit.website_url,
        project_github=project_to_edit.github_url
    )
    if edit_form.validate_on_submit() and edit_form.password.data == admin_password:
        project_to_edit.name = edit_form.project_name.data
        project_to_edit.description = edit_form.project_description.data
        project_to_edit.website_url = edit_form.project_url.data
        project_to_edit.github_url = edit_form.project_github.data
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add_project.html", form=edit_form)


# form to delete project
@app.route("/delete/<int:project_id>", methods=["GET", "POST"])
def delete_project(project_id):
    project_to_delete = db.get_or_404(Project, project_id)
    delete_form = AdminForm()
    if delete_form.validate_on_submit() and delete_form.password.data == admin_password:
        db.session.delete(project_to_delete)
        db.session.commit()
        return redirect(url_for("project_list"))
    return render_template("admin_password.html", form=delete_form)


# form to email me
@app.route("/email", methods=["GET", "POST"])
def email():
    email_form = EmailForm()
    if email_form.validate_on_submit():
        message = f"This is a message from portfolio website   Email: {email_form.email.data}   Message: {email_form.message.data}"
        msg = MIMEText(message, "plain", "utf-8")
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(EMAIL, EMAIL_PASSCODE)
            connection.sendmail(
                from_addr=EMAIL,
                to_addrs=os.environ.get("MY_EMAIL"),
                msg=msg.as_string()
            )
        return redirect(url_for("home"))
    return render_template("email.html", form=email_form)


if __name__ == "__main__":
    app.run(debug=False)
