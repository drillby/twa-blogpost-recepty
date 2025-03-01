import vercel_blob
from flask import redirect, render_template, request, url_for, flash
from werkzeug.utils import secure_filename

from app import app, db

from ..models.models import Recipe, RecipeImage, User, UserLikedRecipes
from io import BytesIO

@app.route("/recipe/<int:id>")
def recipe_detail(id):
    recipe = {}

    return render_template("recipe-detail.html", recipe=recipe)


@app.route("/add-recipe", methods=["GET", "POST"])
def add_recipe():
    if request.method == "POST":
        # logika pro pridani receptu
        recipe_name = request.form.get("recipeName")
        ingredients = request.form.get("ingredients")
        steps = request.form.get("steps")
        category = request.form.get("category")
        pictures = request.files.getlist("pictures")

        # Validace vstupů
        if not recipe_name or not ingredients or not steps or not category or not pictures:
            flash("Všechna pole musí být vyplněná!", "danger")
            return redirect(url_for("add_recipe"))

        # Přiřazení statického ID uživatele
        user_id = 11  # Statické ID uživatele

        # Vytvoření nového receptu
        new_recipe = Recipe(name=recipe_name, ingredients=ingredients, steps=steps, category=category, user_id=user_id)
        db.session.add(new_recipe)
        db.session.commit()

        # Uložení obrázků
        for index, picture in enumerate(pictures):
             if picture:
                img_data = BytesIO()
                picture.save(img_data)
                img_bytes = img_data.getvalue()
                file_extension = picture.filename.split(".")[-1]
                image_res = vercel_blob.put(f"recipe-images/{new_recipe.id}-{index}.{file_extension}", img_bytes)
                image_url = image_res["url"]
                
                recipe_image = RecipeImage(recipe_id=new_recipe.id, image_url=image_url)
                db.session.add(recipe_image)
                db.session.commit()
        
        flash("Recept byl úspěšně přidán.", "success")
        return redirect(url_for("recipe_detail", id=new_recipe.id))
    
    return render_template("add-recipe.html")
