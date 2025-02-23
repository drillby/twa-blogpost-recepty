import hashlib
import random
from io import BytesIO

import pyzxcvbn
import vercel_blob
from flask import flash, redirect, render_template, request, url_for
from flask_login import UserMixin, current_user, login_required, login_user, logout_user
from PIL import Image, ImageDraw

from app import app, db, login_manager

from ..models.models import Recipe, RecipeImage, User, UserLikedRecipes


@app.context_processor
def inject_user():
    if not current_user.is_authenticated:
        return {"user_info": None}
    user_info = {
        "id": current_user.id,
        "username": current_user.username,
        "profile_picture_url": current_user.profile_picture_url,
    }
    return {"user_info": user_info}


def generate_avatar(identifier, size=8, scale=32, output_size=256):
    # Vytvoření hash z identifikátoru
    hash_digest = hashlib.md5(identifier.encode()).hexdigest()
    random.seed(int(hash_digest, 16))

    # Barva na základě hashe
    color = (
        int(hash_digest[0:2], 16),
        int(hash_digest[2:4], 16),
        int(hash_digest[4:6], 16),
    )

    # Vytvoření prázdného obrázku
    img = Image.new("RGB", (size, size), "white")
    draw = ImageDraw.Draw(img)

    # Generování symetrického vzoru
    for x in range(size // 2 + 1):
        for y in range(size):
            if random.choice([True, False]):
                draw.point((x, y), fill=color)
                draw.point((size - x - 1, y), fill=color)

    # Zvětšení na požadovanou velikost
    img = img.resize((output_size, output_size), Image.NEAREST)
    return img


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = (
            db.session.query(User).filter_by(username=request.form["username"]).first()
        )
        if user and user.check_password(request.form["password"]):
            login_user(user)
            return redirect(url_for("index"))
        else:
            flash("Nesprávné přihlašovací údaje", "danger")
            return redirect(url_for("login"))
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    elif request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        # Kontrola, zda uživatel s daným emailem neexistuje
        user = db.session.query(User).filter_by(email=email).first()
        if user:
            flash("Uživatel s tímto emailem již existuje", "danger")
            return redirect(url_for("register"))

        # Kontrola, zda uživatel s daným username neexistuje
        user = db.session.query(User).filter_by(username=username).first()
        if user:
            flash("Uživatel s tímto uživatelským jménem již existuje", "danger")
            return redirect(url_for("register"))

        # Kontrola síly hesla
        result = pyzxcvbn.zxcvbn(password)
        if result["score"] < 2:
            flash("Heslo je příliš slabé", "danger")
            return redirect(url_for("register"))

        profile_picture = generate_avatar(username)
        img_data = BytesIO()
        profile_picture.save(img_data, format="PNG")
        img_bytes = img_data.getvalue()
        profile_picture_res = vercel_blob.put(
            f"profile_pictures/{username}.png", img_bytes
        )
        profile_picture_url = profile_picture_res["url"]

        user = User(username, email, password, profile_picture_url)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for("index"))

    else:
        return render_template("register.html")


@app.route("/logout", methods=["POST", "GET"])
@login_required
def logout():
    if not current_user.is_authenticated:
        return redirect(url_for("index"))
    logout_user()
    return redirect(url_for("index"))


@app.route("/account-settings", methods=["GET", "POST"])
@login_required
def account_settings():
    if request.method == "POST":
        # logika pro zmenu nastaveni uctu
        pass
    else:
        return render_template("account-settings.html")


# test user
# jenna39
# heslo123
@app.route("/profile/<int:id>")
def profile(id):
    user = db.session.query(User).get(id)
    if user is None:
        return redirect(url_for("index"))

    user_info = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "profile_picture_url": user.profile_picture_url,
        "created_at": user.created_at,
    }

    # recipes with images
    recipes = (
        db.session.query(Recipe)
        .filter(Recipe.author_id == id)
        .options(db.joinedload(Recipe.images))  # Načtení obrázků receptu
        .all()
    )
    recipes_dict = [
        {
            "id": recipe.id,
            "title": recipe.title,
            "image_url": recipe.images[0].image_url if recipe.images else None,
        }
        for recipe in recipes
    ]

    user_info["recipes"] = recipes_dict

    if current_user.is_authenticated and current_user.id == id:
        # user_liked_recipes with images by user_id
        user_liked_recipes = (
            db.session.query(Recipe)
            .join(UserLikedRecipes, Recipe.id == UserLikedRecipes.recipe_id)
            .filter(UserLikedRecipes.user_id == id)
            .options(db.joinedload(Recipe.images))  # Načtení obrázků
            .all()
        )
        user_liked_recipes_dict = [
            {
                "id": recipe.id,
                "title": recipe.title,
                "image_url": (recipe.images[0].image_url if recipe.images else None),
            }
            for recipe in user_liked_recipes
        ]
    else:
        user_liked_recipes_dict = []

    user_info["liked_recipes"] = user_liked_recipes_dict
    # return user_info
    return render_template("profile.html", user=user_info)
