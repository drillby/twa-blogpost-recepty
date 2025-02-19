import datetime

from flask import redirect, render_template, request, url_for

from app import app, db

from ..models.models import Recipe, RecipeImage, User


@app.route("/search")
def search():
    query = request.args.get("query")
    if not query:
        return redirect(url_for("index"))
    res = []
    return render_template("search-results.html", res=res, query=query)


@app.route("/")
def index():
    year = datetime.datetime.now().year

    recipes = []

    recipes_featured = []

    return render_template(
        "index.html", year=year, recipes=recipes, recipes_featured=recipes_featured
    )
