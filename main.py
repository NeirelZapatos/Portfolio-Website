from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String

app = Flask(__name__)
app.config["SECRET_KEY"] = "R4jBwpb@V!w^7d3"
Bootstrap5(app)


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
    project_list = Project.query.all()
    return render_template("index.html", project_list=project_list)


@app.route("/projects")
def projects():
    return render_template("projects.html")


if __name__ == "__main__":
    app.run(debug=True)
