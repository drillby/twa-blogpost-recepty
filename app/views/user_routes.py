import hashlib
import random
from io import BytesIO

import pyzxcvbn
import vercel_blob
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from PIL import Image, ImageDraw

from app import app, db, oauth

from ..models.models import Recipe, User, UserLikedRecipes


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


@app.route("/login/google")
def login_google():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    return oauth.TWA_Blogpost.authorize_redirect(
        redirect_uri=url_for("auth_google", _external=True)
    )


@app.route("/signin-google")
def auth_google():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    token = oauth.TWA_Blogpost.authorize_access_token()

    userinfo = token.get("userinfo")
    email = userinfo["email"]
    user = db.session.query(User).filter_by(email=email).first()
    if user:
        login_user(user)
        flash("Přihlášení proběhlo úspěšně", "success")
        return redirect(url_for("index"))
    else:
        username = userinfo["name"]
        random_password = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=12)
        )
        user = User(username, email, random_password, userinfo["picture"])
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash(
            "Nastavte si heslo, abyste si mohli v budoucnu vybrat jiný způsob přihlášení než Google",
            "info",
        )
        return redirect(url_for("account_settings"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    if request.method == "POST":
        user = (
            db.session.query(User).filter_by(username=request.form["username"]).first()
        )
        if user and user.check_password(request.form["password"]):
            login_user(user)
            flash("Přihlášení proběhlo úspěšně", "success")
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

        flash("Registrace proběhla úspěšně", "success")

        return redirect(url_for("index"))

    else:
        return render_template("register.html")


@app.route("/logout", methods=["POST", "GET"])
@login_required
def logout():
    logout_user()
    flash("Odhlášení proběhlo úspěšně", "success")
    return redirect(url_for("index"))


@app.route("/account-settings", methods=["GET", "POST"])
@login_required
def account_settings():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        new_password = request.form["password"]
        # check if username changed
        if username != current_user.username:
            user = db.session.query(User).filter_by(username=username).first()
            if user:
                flash("Uživatel s tímto uživatelským jménem již existuje", "danger")
                return redirect(url_for("account_settings"))
        # check if email changed
        if email != current_user.email:
            user = db.session.query(User).filter_by(email=email).first()
            if user:
                flash("Uživatel s tímto emailem již existuje", "danger")
                return redirect(url_for("account_settings"))
        # check if password changed
        if new_password:
            result = pyzxcvbn.zxcvbn(new_password)
            if result["score"] < 2:
                flash("Heslo je příliš slabé", "danger")
                return redirect(url_for("account_settings"))
            current_user.set_password(new_password)
        current_user.username = username
        current_user.email = email
        db.session.commit()
        flash("Změny byly uloženy", "success")
        return redirect(url_for("account_settings"))

    else:
        user = db.session.query(User).get(current_user.id)
        return render_template("account-settings.html", user=user)


# test user
# jenna39
# heslo123
@app.route("/profile/<int:id>")
@login_required
def profile(id):
    user = db.session.query(User).get(id)
    if not user:
        return redirect(url_for("index"))

    if current_user.is_authenticated and current_user.id == id:
        user.liked_recipes = (
            db.session.query(Recipe)
            .join(UserLikedRecipes, Recipe.id == UserLikedRecipes.recipe_id)
            .filter(UserLikedRecipes.user_id == id)
            .options(db.joinedload(Recipe.images))
            .all()
        )
    else:
        user.liked_recipes = []

    return render_template("profile.html", user=user)


@app.route("/delete-account", methods=["POST"])
@login_required
def delete_account():
    user = db.session.query(User).get(current_user.id)
    user.username = f"deleted-{user.id}"
    user.email = f"deleted@domain-{user.id}.com"
    user.set_password(
        "".join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=12))
    )
    user.profile_picture_url = "https://prspq1ztcixcgwhw.public.blob.vercel-storage.com/FoodFinder_logo_mini-BT2ai1W1oPpncg6z0yBBx2hTX8Bcbr.png"

    db.session.query(UserLikedRecipes).filter_by(user_id=user.id).delete()

    db.session.commit()
    logout_user()

    flash("Účet byl smazán", "success")

    return redirect(url_for("index"))
