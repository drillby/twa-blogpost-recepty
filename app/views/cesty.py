import datetime

from flask import render_template

from app import app


@app.route("/")
def index():
    year = datetime.datetime.now().year
    return render_template("index.html", year=year)


@app.route("/about")
def about():
    return render_template("base.html")
