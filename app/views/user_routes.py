import vercel_blob
from flask import flash, redirect, render_template, request, url_for
from flask_login import UserMixin, current_user, login_required, login_user, logout_user

from app import app, db, login_manager

from ..models.models import Recipe, RecipeImage, User, UserLikedRecipes


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = (
            db.session.query(User).filter_by(username=request.form["username"]).first()
        )
        print(user)
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
    if request.method == "POST":
        # logika pro registraci
        pass
    else:
        return render_template("register.html")


@app.route("/account-settings", methods=["GET", "POST"])
@login_required
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
