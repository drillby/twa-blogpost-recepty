import vercel_blob
from flask import redirect, render_template, request, url_for, flash
from werkzeug.utils import secure_filename
from io import BytesIO, flash
from werkzeug.utils import secure_filename
from io import BytesIO

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
        new_recipe = Recipe(title=recipe_name, ingredients=ingredients, instructions=steps, tag=category, author_id=user_id)
        db.session.add(new_recipe)
        db.session.commit()

        # Uložení obrázků
        for index, picture in enumerate(pictures):
            if picture and allowed_file(picture.filename):
                try:
                    img_data = BytesIO()
                    picture.save(img_data)
                    img_data.seek(0)  # reset pozice streamu pro načtení všech bajtů obrázku
                    img_bytes = img_data.read()
                    file_extension = picture.filename.split(".")[-1]
                    image_path = f"recipe-images/{new_recipe.id}-{index + 1}.{file_extension}"
                    
                    # Nahrání obrázku na Vercel Blob Storage
                    image_res = vercel_blob.put(image_path, img_bytes)
                    image_url = image_res["url"]
                    
                    recipe_image = RecipeImage(recipe_id=new_recipe.id, image=image_url)
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
    ALLOWED_EXTENSIONS = {'png'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
