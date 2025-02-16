import datetime

from flask import redirect, render_template, request, url_for

from app import app


class Recipe:
    def __init__(self, id, name, image):
        self.id = id
        self.name = name
        self.image = image

    def __repr__(self):
        return f"{self.name}"


class RecipeDetail:

    def __init__(
        self,
        title,
        author_name,
        author_image,
        images,
        ingredients,
        instructions,
        related_recipes_id,
    ):
        self.title = title
        self.author_name = author_name
        self.author_image = author_image
        self.images = images
        self.ingredients = ingredients
        self.instructions = instructions
        self.related_recipes_id = related_recipes_id


image1 = "https://cdn.xsd.cz/resize/6d125047dfac3dac99242ac561319391_resize=1280,889_.jpg?hash=f2c0b06867af20405e1c9a0c01cedc0a"
image2 = "https://cdn.myshoptet.com/usr/www.peliskydog.cz/user/documents/upload/chodsky-pes.jpg"


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


@app.route("/about")
def about():
    return render_template("base.html")


@app.route("/recipe/<int:id>")
def recipe_detail(id):
    recipe = RecipeDetail(
        title=f"Recept {id}",
        author_name=f"Autor {id}",
        author_image="https://cdn.myshoptet.com/usr/www.peliskydog.cz/user/documents/upload/chodsky-pes.jpg",
        images=[
            "https://cdn.xsd.cz/resize/6d125047dfac3dac99242ac561319391_resize=1280,889_.jpg?hash=f2c0b06867af20405e1c9a0c01cedc0a",
            "https://cdn.myshoptet.com/usr/www.peliskydog.cz/user/documents/upload/chodsky-pes.jpg",
        ],
        ingredients=[
            f"{id} cup Ingredience 1",
            f"{id} tbsp Ingredience 2",
            f"{id} slices Ingredience 3",
        ],
        instructions=f"Postup přípravy receptu {id}.",
        related_recipes_id=[
            Recipe(1, "Recept 1", image1),
            Recipe(2, "Recept 2", image2),
            Recipe(3, "Recept 3", image1),
            Recipe(4, "Recept 4", image2),
        ],
    )

    return render_template("recipe-detail.html", recipe=recipe)


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
