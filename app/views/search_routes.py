import datetime
import random

from faker import Faker
from flask import redirect, render_template, request, url_for

from app import app, db

from ..models.models import Recipe, RecipeImage, User, UserLikedRecipes


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


@app.route("/generate-test-data")
def generate_test_data():
    if app.config["TESTING"] == "False":
        return "Testovací data mohou být generována pouze v testovacím prostředí"

    user = request.args.get("user", 0, type=int)
    recipe = request.args.get("recipe", 0, type=int)

    fake = Faker()
    users = []
    recipes = []

    # Vytvoření uživatelů
    for _ in range(user):
        user = User(
            username=fake.user_name(),
            email=fake.email(),
            password=fake.password(),  # Default heslo pro všechny (hash se generuje v User modelu)
            profile_picture_url=fake.image_url(),
        )
        db.session.add(user)
        users.append(user)

    db.session.commit()  # Uložíme uživatele do DB, aby měly ID

    # Vytvoření receptů
    for _ in range(recipe):
        recipe = Recipe(
            title=fake.sentence(nb_words=4),
            author_id=random.choice(users).id,
            instructions=fake.text(),
            ingredients=fake.text(),
            tag=random.choice(
                [
                    "dezerty",
                    "hlavni_jidla",
                    "napoje",
                    "polevky",
                    "predkrmy",
                    "snidane",
                    "svaciny",
                    "vecere",
                ]
            ),
        )
        db.session.add(recipe)
        recipes.append(recipe)

    db.session.commit()  # Uložíme recepty do DB, aby měly ID

    # Přidání obrázků k receptům
    for recipe in recipes:
        num_images = random.randint(1, 5)
        for _ in range(num_images):
            image = RecipeImage(recipe_id=recipe.id, image_url=fake.image_url())
            db.session.add(image)

    db.session.commit()

    # Přidání oblíbených receptů
    for user in users:
        liked_recipes = random.sample(
            recipes, k=random.randint(1, min(5, len(recipes)))
        )
        for recipe in liked_recipes:
            like_entry = UserLikedRecipes(user_id=user.id, recipe_id=recipe.id)
            db.session.add(like_entry)

    db.session.commit()
    return "Testovací data byla vygenerována"
