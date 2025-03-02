import vercel_blob
from flask import redirect, render_template, request, url_for

from app import app, db

from ..models.models import Recipe, RecipeImage, User, UserLikedRecipes


@app.route("/recipe/<int:id>")
def recipe_detail(id):
    recipe = db.session.query(Recipe).get_or_404(id)

    related_recipes = Recipe.query.filter(Recipe.tag == recipe.tag, Recipe.id != recipe.id).limit(4).all()
    
    ##recipe = Recipe.query.get_or_404(id)
    ##upravit related_recipes_id
    recipe_data = {"title": recipe.title,
        "author_name": recipe.author.username,
        "author_image": recipe.author.profile_picture_url
        or url_for("static", filename="images/default-profile.png"),
        "instructions": recipe.instructions,
        "ingredients": recipe.ingredients.split("\n"),  # Rozdělit ingredience na řádky
        "images": [img.image_url for img in recipe.images],
        ##"related_recipes_id": [22],
        ##    related.id for related in db.session.query(Recipe).filter(Recipe.tag == recipe.tag).limit(4)
        "related_recipes_id": [
                     {
                "id": r.id,
                "title": r.title,
                "image": r.images[0].image_url if r.images else None,
            }
            for r in related_recipes
        ],
        }
    return render_template("recipe-detail.html", recipe=recipe_data)


@app.route("/add-recipe", methods=["GET", "POST"])
def add_recipe():
    if request.method == "POST":
        # logika pro pridani receptu
        pass
    else:
        return render_template("add-recipe.html")
