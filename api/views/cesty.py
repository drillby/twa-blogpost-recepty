from flask import render_template

from api import app


@app.route("/test")
def test():
    return render_template("base.html")
