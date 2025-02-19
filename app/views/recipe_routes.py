from flask import redirect, render_template, request, url_for

from app import app, db

from ..models.models import Recipe, RecipeImage, User


@app.route("/recipe/<int:id>")
def recipe_detail(id):
    recipe = {}

    return render_template("recipe-detail.html", recipe=recipe)


@app.route("/add-recipe", methods=["GET", "POST"])
def add_recipe():
    if request.method == "POST":
        # logika pro pridani receptu
        pass
    else:
        return render_template("add-recipe.html")
