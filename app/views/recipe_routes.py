import vercel_blob
from flask import redirect, render_template, request, url_for, flash
from werkzeug.utils import secure_filename

import os



from app import app, db

from ..models.models import Recipe, RecipeImage, User, UserLikedRecipes


@app.route("/recipe/<int:id>")
def recipe_detail(id):
    recipe = {}

    return render_template("recipe-detail.html", recipe=recipe)


@app.route("/add-recipe", methods=["GET", "POST"])
def add_recipe():
    if request.method == "POST":
        # logika pro pridani receptu
        recipe_name = request.form.get('recipeName')
        ingredients = request.form.get('ingredients')
        steps = request.form.get('steps')
        category = request.form.get('category')
        pictures = request.files.getlist('pictures')

        # Validace vstupů
        if not recipe_name or not ingredients or not steps or not category:
            flash('Všechna pole musí být vyplněná!', 'danger')
            return redirect(url_for('add_recipe'))

        # Přiřazení statického ID uživatele
        user_id = 11  # Statické ID uživatele

        # Vytvoření nového receptu
        new_recipe = Recipe(name=recipe_name, ingredients=ingredients, steps=steps, category=category, user_id=user_id)
        db.session.add(new_recipe)
        db.session.commit()

        # Uložení obrázků
        for index, picture in enumerate(pictures):
            if picture and allowed_file(picture.filename):
                filename = secure_filename(picture.filename)
                file_extension = filename.rsplit('.', 1)[1].lower()
                image_path = f"recipe-images/{new_recipe.id}-{index + 1}.{file_extension}"
                
                # Nahrání obrázku na Vercel Blob Storage
                img_bytes = picture.read()
                profile_picture_res = vercel_blob.put(image_path, img_bytes)
                profile_picture_url = profile_picture_res["url"]
                
                new_image = RecipeImage(recipe_id=new_recipe.id, image_url=profile_picture_url)
                db.session.add(new_image)
            else:
                flash('Nepovolený formát souboru!', 'danger')
                return redirect(url_for('add_recipe'))

        db.session.commit()
        flash('Recept byl úspěšně přidán!', 'success')
        return redirect(url_for('recipe_detail', id=new_recipe.id))
    else:
        return render_template("add-recipe.html")

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS