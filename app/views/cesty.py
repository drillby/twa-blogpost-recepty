import datetime

from flask import redirect, render_template, request, url_for

from app import app


class Recipe:
    def __init__(self, name, image):
        self.name = name
        self.image = image

    def __repr__(self):
        return f"{self.name}"


@app.route("/")
def index():
    year = datetime.datetime.now().year

    image1 = "https://cdn.xsd.cz/resize/6d125047dfac3dac99242ac561319391_resize=1280,889_.jpg?hash=f2c0b06867af20405e1c9a0c01cedc0a"
    image2 = "https://cdn.myshoptet.com/usr/www.peliskydog.cz/user/documents/upload/chodsky-pes.jpg"

    recipes = [
        Recipe("Recept 1", image1),
        Recipe("Recept 2", image2),
        Recipe("Recept 3", image1),
        Recipe("Recept 4", image2),
    ]

    return render_template("index.html", year=year, recipes=recipes)


@app.route("/login")
def login():
    if request.method == "POST":
        # logika pro prihlaseni
        pass
    else:
        return render_template("login.html")


@app.route("/about")
def about():
    return render_template("base.html")
