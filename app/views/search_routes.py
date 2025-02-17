import datetime

from flask import redirect, render_template, request, url_for

from app import app

image1 = "https://cdn.xsd.cz/resize/6d125047dfac3dac99242ac561319391_resize=1280,889_.jpg?hash=f2c0b06867af20405e1c9a0c01cedc0a"
image2 = "https://cdn.myshoptet.com/usr/www.peliskydog.cz/user/documents/upload/chodsky-pes.jpg"


class Recipe:
    def __init__(self, id, name, image):
        self.id = id
        self.name = name
        self.image = image

    def __repr__(self):
        return f"{self.name}"


@app.route("/search")
def search():
    query = request.args.get("query")
    if not query:
        return redirect(url_for("index"))
    res = [
        Recipe(1, "Recept 1", image1),
        Recipe(2, "Recept 2", image2),
        Recipe(3, "Recept 3", image1),
        Recipe(4, "Recept 4", image2),
    ]
    return render_template("search-results.html", res=res, query=query)


@app.route("/")
def index():
    year = datetime.datetime.now().year

    recipes = [
        Recipe(1, "Recept 1", image1),
        Recipe(2, "Recept 2", image2),
        Recipe(3, "Recept 3", image1),
        Recipe(4, "Recept 4", image2),
    ]

    return render_template("index.html", year=year, recipes=recipes)
