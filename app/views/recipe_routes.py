from io import BytesIO

import vercel_blob
from flask import flash, redirect, render_template, request, url_for, jsonify
from flask_login import current_user, login_required

from app import app, db

from ..models.models import Recipe, RecipeImage, UserLikedRecipes




# create template filter
@app.template_filter("format_images")
def format_images(images):
    images = [image.image_url for image in images]
    return images


@app.route("/recipe/<int:id>")
@login_required
def recipe_detail(id):
    recipe = Recipe.query.get_or_404(id)

    related_recipes = (
        Recipe.query.filter(Recipe.tag == recipe.tag, Recipe.id != recipe.id)
        .limit(4)
        .all()
    )

    # Check if the current user has liked the recipe
    is_favorited = UserLikedRecipes.query.filter_by(user_id=current_user.id, recipe_id=id).first() is not None

    return render_template(
        "recipe-detail.html",
        recipe=recipe,
        related_recipes=related_recipes,
        is_favorited=is_favorited,  # Pass favorite status to template
    )



@app.route("/toggle-favorite/<int:recipe_id>", methods=["POST"])
@login_required
def toggle_favorite(recipe_id):

    user_id = current_user.id
    recipe = Recipe.query.get_or_404(recipe_id)

    # Check if the recipe is already liked by the user
    liked_recipe = UserLikedRecipes.query.filter_by(user_id=user_id, recipe_id=recipe_id).first()

    if liked_recipe:
        # If already liked, remove from favorites
        db.session.delete(liked_recipe)
        db.session.commit()
        return jsonify({"status": "removed"})
    else:
        #If user adding his own recipe, return error
        if recipe.author_id == user_id:
            return jsonify({"status": "error", "message": "Nemůžete přidat vlastní recept do oblíbených"}), 400
        # If not liked, add to favorites
        new_like = UserLikedRecipes(user_id=user_id, recipe_id=recipe_id)
        db.session.add(new_like)
        db.session.commit()
        return jsonify({"status": "added"})



@login_required
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
        if (
            not recipe_name
            or not ingredients
            or not steps
            or not category
            or not pictures
        ):
            flash("Všechna pole musí být vyplněná!", "danger")
            return redirect(url_for("add_recipe"))

        # logged in user
        user_id = current_user.id
        # Vytvoření nového receptu
        new_recipe = Recipe(
            title=recipe_name,
            ingredients=ingredients,
            instructions=steps,
            tag=category,
            author_id=user_id,
        )
        db.session.add(new_recipe)
        db.session.commit()

        # Uložení obrázků
        for index, picture in enumerate(pictures):
            if picture and allowed_file(picture.filename):
                try:
                    img_data = BytesIO()
                    picture.save(img_data)
                    img_data.seek(
                        0
                    )  # reset pozice streamu pro načtení všech bajtů obrázku
                    img_bytes = img_data.read()
                    file_extension = picture.filename.split(".")[-1]
                    image_path = (
                        f"recipe-images/{new_recipe.id}-{index + 1}.{file_extension}"
                    )

                    # Nahrání obrázku na Vercel Blob Storage
                    image_res = vercel_blob.put(image_path, img_bytes)
                    image_url = image_res["url"]

                    recipe_image = RecipeImage(
                        recipe_id=new_recipe.id, image_url=image_url
                    )
                    db.session.add(recipe_image)
                except Exception as e:
                    flash(f"Chyba při nahrávání obrázku: {str(e)}", "danger")
                    return redirect(url_for("add_recipe"))
            else:
                flash("Nepovolený formát souboru!", "danger")
                return redirect(url_for("add_recipe"))

        db.session.commit()
        flash("Recept byl úspěšně přidán.", "success")
        return redirect(url_for("recipe_detail", id=new_recipe.id))

    return render_template("add-recipe.html")


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
