from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from forms import AddForm, AddProjectForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "R4jBwpb@V!w^7d3"
Bootstrap5(app)

admin_password = "1234"


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///projects.db"
db.init_app(app)


class Project(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    website_url: Mapped[str] = mapped_column(String, unique=True, nullable=True)
    github_url: Mapped[str] = mapped_column(String, unique=True, nullable=True)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    # new_project = Project(
    #     name="Testing",
    #     description="We don't really know",
    # )
    # db.session.add(new_project)
    # db.session.commit()
    project_list = Project.query.all()
    return render_template("index.html", project_list=project_list)


@app.route("/projects")
def projects():
    return render_template("projects.html")


@app.route("/add-project", methods=["GET", "POST"])
def add_project():
    add_form = AddForm()
    if add_form.validate_on_submit():
        if add_form.password.data == admin_password:
            return redirect(url_for("project_details"))
    return render_template("add.html", form=add_form)


@app.route("/project_details", methods=["GET", "POST"])
def project_details():
    project_form = AddProjectForm()
    if project_form.validate_on_submit():
        new_project = Project(
            name=project_form.project_name.data,
            description=project_form.project_description.data
        )
        db.session.add(new_project)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add_project.html", form=project_form)

if __name__ == "__main__":
    app.run(debug=True)
