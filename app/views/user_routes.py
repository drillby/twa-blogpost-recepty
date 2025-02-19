import vercel_blob
from flask import redirect, render_template, request, url_for

from app import app, db

from ..models.models import Recipe, RecipeImage, User, UserLikedRecipes


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # logika pro prihlaseni
        pass
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # logika pro registraci
        pass
    else:
        return render_template("register.html")


@app.route("/account-settings", methods=["GET", "POST"])
def account_settings():
    if request.method == "POST":
        # logika pro zmenu nastaveni uctu
        pass
    else:
        return render_template("account-settings.html")


@app.route("/profile/<int:id>")
def my_profile(id):
    my_profile = bool(request.args.get("my_profile", False))
    user = {}
    return render_template("profile.html", user=user)
