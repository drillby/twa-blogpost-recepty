from flask import redirect, render_template, request, url_for

from app import app


class Recipe:
    def __init__(self, id, name, image):
        self.id = id
        self.name = name
        self.image = image

    def __repr__(self):
        return f"{self.name}"


class User:
    def __init__(
        self, id, username, email, recipes, liked_recipes, profile_picture_url
    ):
        self.id = id
        self.username = username
        self.profile_picture_url = profile_picture_url
        self.email = email
        self.recipes = recipes
        self.liked_recipes = liked_recipes

    def __repr__(self):
        return f"{self.username}"


image1 = "https://cdn.xsd.cz/resize/6d125047dfac3dac99242ac561319391_resize=1280,889_.jpg?hash=f2c0b06867af20405e1c9a0c01cedc0a"
image2 = "https://cdn.myshoptet.com/usr/www.peliskydog.cz/user/documents/upload/chodsky-pes.jpg"


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
    user = User(
        id=1,
        username="User 1",
        profile_picture_url=image1,
        email="a@a.a",
        recipes=(
            [
                Recipe(1, "Recept 1", image1),
                Recipe(2, "Recept 2", image2),
                Recipe(3, "Recept 3", image1),
                Recipe(4, "Recept 4", image2),
            ]
        ),
        liked_recipes=(
            [
                Recipe(1, "Recept 1", image1),
                Recipe(2, "Recept 2", image2),
            ]
            if my_profile
            else []
        ),
    )
    return render_template("profile.html", user=user)
