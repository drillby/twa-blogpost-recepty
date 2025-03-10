import datetime
import random
import re

from faker import Faker
from flask import jsonify, redirect, render_template, request, url_for
from fuzzywuzzy import fuzz
from sqlalchemy.sql.expression import desc, func

from app import app, db

from ..models.models import Recipe, RecipeImage, User, UserLikedRecipes


@app.route("/search")
def search():
    query = request.args.get("query").lower()

    # empty query returns index.html
    if not query:
        return redirect(url_for("index"))

    # searching using tags
    tag_synonyms = {
        "vecere": [
            "večeře",
            "večeře recepty",
            "recepty na večeři",
            "co k večeři",
            "večerní jídla",
            "jídla k večeři",
            "večeře pro rodinu",
            "rychlá večeře",
            "večerní menu",
            "večeře pro dvě",
            "večeře pro děti",
            "co připravit na večeři",
        ],
        "snidane": [
            "snídaně",
            "snídaně recepty",
            "co na snídani",
            "rychlá snídaně",
            "snídaně pro děti",
            "snídaně pro dva",
            "ideální snídaně",
            "sladká snídaně",
            "slaná snídaně",
            "snídaně do postele",
            "snídaně na víkend",
        ],
        "dezerty": [
            "dezert",
            "dezerty recepty",
            "sladkosti",
            "koláče",
            "dorty",
            "pečení",
            "cukroví",
            "sladké jídlo",
            "sladké recepty",
            "koláče a dezerty",
            "vánoční cukroví",
            "sladké dobroty",
            "dort na oslavu",
        ],
        "hlavni_jidla": [
            "hlavní jídla",
            "hlavní jídlo",
            "hlavní chod",
            "hlavní pokrm",
            "co na oběd",
            "oběd",
            "jídlo k obědu",
            "jednoduchá hlavní jídla",
            "hlavní jídlo pro rodinu",
            "jídlo pro dva",
            "ráno k obědu",
            "dobrá hlavní jídla",
            "oběd pro děti",
        ],
        "napoje": [
            "nápoje",
            "pití",
            "nápoje recepty",
            "co na pití",
            "lahodné nápoje",
            "zdravé nápoje",
            "nealkoholické nápoje",
            "smoothie",
            "cocktaily",
            "ovocné nápoje",
            "studené nápoje",
            "teplé nápoje",
            "nápoje pro děti",
        ],
        "polevky": [
            "polévky",
            "polévka",
            "polévka recepty",
            "zeleninová polévka",
            "masová polévka",
            "rychlá polévka",
            "domácí polévky",
            "krémové polévky",
            "česnečka",
            "vývary",
            "čočková polévka",
            "zeleninový vývar",
            "pohanková polévka",
        ],
        "predkrmy": [
            "předkrmy",
            "předkrm",
            "snídaňové předkrmy",
            "předkrmy recepty",
            "studené předkrmy",
            "teplé předkrmy",
            "ideální předkrm",
            "sýrové předkrmy",
            "předkrmy pro hosty",
            "lahodné předkrmy",
            "malé jídlo",
            "co na předkrm",
        ],
        "svaciny": [
            "svačiny",
            "svačina",
            "co na svačinu",
            "svačiny pro děti",
            "svačiny pro dospělé",
            "rychlé svačiny",
            "svačiny do školy",
            "svačiny pro školáky",
            "svačina pro sportovce",
            "malé jídlo",
            "sladká svačina",
            "slaná svačina",
            "svačiny do práce",
        ],
    }

    for tag, synonyms in tag_synonyms.items():
        if any(synonym in query for synonym in synonyms):
            recipes_tag = Recipe.query.filter(Recipe.tag == tag).all()
            return render_template("search-results.html", res=recipes_tag, query=query)

    # searching using title or ingredients
    recipes_all = Recipe.query.all()
    matches = []

    for recipe in recipes_all:

        query_words = re.split(r"[\s,;.\-!]+", query.lower())

        # title searching
        title_words = re.split(r"[\s,;.\-!]+", recipe.title.lower())

        match_ratios_title = [
            fuzz.ratio(title_word, query_word)
            for title_word in title_words
            if len(title_word) > 2
            for query_word in query_words
            if len(query_word) > 2
        ]

        match_ratio_title = max(match_ratios_title)

        # Testing matches title
        """
        for title_word in title_words:  
            for word in query_words:
                if fuzz.ratio(title_word, word) > 70:
                    print(title_word,fuzz.ratio(title_word, word), word)
        """

        # ingredients searching
        ingredients = re.split(r"[\s,;.\-!]+", recipe.ingredients.lower())

        match_ratios_ingredients = [
            fuzz.ratio(ingredient, query_word)
            for ingredient in ingredients
            if len(ingredient) > 2
            for query_word in query_words
            if len(query_word) > 2
        ]

        match_ratio_ingredients = max(match_ratios_ingredients)

        # Testing matches ingredients
        """
        print(match_ratio_title)
        for ingredient in ingredients:  
            for word in query_words:
                if fuzz.ratio(ingredient, word) > 79:
                    print(ingredient,fuzz.ratio(ingredient, word), word)
        """

        # results of matching
        if match_ratio_title > 79 or match_ratio_ingredients > 79:
            weighted_match_ratio = (
                0.55 * match_ratio_title + 0.45 * match_ratio_ingredients
            )
            matches.append((recipe, weighted_match_ratio))

    # sorting matches by weighted ratio
    matches.sort(key=lambda x: x[1], reverse=True)
    sorted_recipes = [match[0] for match in matches]

    return render_template("search-results.html", res=sorted_recipes, query=query)


@app.route("/", methods=["GET"])
def index():
    # Featured selection by client time
    time_param = request.args.get("time")
    if time_param == "NaN" or time_param is None:
        print("Nepodařilo se získat čas od klienta, používám čas serveru.")
        client_time = datetime.datetime.now().hour
    else:
        try:
            client_time = int(time_param)
            print(client_time)
        except ValueError:
            print("Neplatná hodnota času, používám serverový čas.")
            client_time = datetime.datetime.now().hour

    searching_tag = ""
    if 0 < client_time < 9:
        searching_tag = "snidane"
    elif client_time < 11:
        searching_tag = "svaciny"
    elif client_time < 13:
        searching_tag = "hlavni_jidla"
    elif client_time < 15:
        searching_tag = "dezerty"
    elif client_time < 17:
        searching_tag = "svacina"
    else:
        searching_tag = "vecere"

    recipes_featured = (
        Recipe.query.filter(Recipe.tag == searching_tag)
        .order_by(func.random())
        .limit(4)
        .all()
    )
    # Newest recepies
    page = request.args.get("page", 1, type=int)
    per_page = 10

    recipes_paginated = Recipe.query.order_by(desc(Recipe.created_at)).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return render_template(
        "index.html",
        recipes=recipes_paginated.items,
        recipes_featured=recipes_featured,
        next_page=recipes_paginated.next_num if recipes_paginated.has_next else None,
    )


@app.route("/generate-test-data")
def generate_test_data():
    test_data = {
        "dezerty": [
            {
                "title": "Čokoládový dort",
                "ingredients": "Čokoláda, mouka, cukr, vejce, máslo",
                "instructions": "Smíchejte ingredience a upečte na 180°C.",
            },
            {
                "title": "Jablečný štrůdl",
                "ingredients": "Jablka, listové těsto, cukr, skořice",
                "instructions": "Zabalte jablka do těsta a upečte.",
            },
            {
                "title": "Tiramisu",
                "ingredients": "Mascarpone, vejce, piškoty, káva, kakao",
                "instructions": "Poskládejte vrstvy a nechte ztuhnout.",
            },
            {
                "title": "Palačinky",
                "ingredients": "Mléko, mouka, vejce, cukr",
                "instructions": "Usmažte tenké palačinky na pánvi.",
            },
        ],
        "hlavni_jidla": [
            {
                "title": "Svíčková na smetaně",
                "ingredients": "Hovězí maso, smetana, kořenová zelenina",
                "instructions": "Uvařte maso a připravte omáčku.",
            },
            {
                "title": "Kuře na paprice",
                "ingredients": "Kuřecí maso, paprika, smetana",
                "instructions": "Orestujte maso a přidejte smetanovou omáčku.",
            },
            {
                "title": "Guláš",
                "ingredients": "Hovězí maso, cibule, paprika, brambory",
                "instructions": "Vařte dlouho na mírném ohni.",
            },
            {
                "title": "Rizoto",
                "ingredients": "Rýže, kuřecí maso, zelenina",
                "instructions": "Orestujte suroviny a vařte s vývarem.",
            },
        ],
        "napoje": [
            {
                "title": "Domácí limonáda",
                "ingredients": "Citrony, voda, cukr, led",
                "instructions": "Smíchejte a podávejte chlazené.",
            },
            {
                "title": "Horká čokoláda",
                "ingredients": "Mléko, čokoláda, cukr",
                "instructions": "Ohřejte mléko a rozmíchejte čokoládu.",
            },
            {
                "title": "Smoothie s banánem",
                "ingredients": "Banán, mléko, med",
                "instructions": "Rozmixujte do hladka.",
            },
            {
                "title": "Mojito (nealko)",
                "ingredients": "Máta, limetka, cukr, soda",
                "instructions": "Rozmačkejte limetku a mátu, dolijte sodou.",
            },
        ],
        "polevky": [
            {
                "title": "Rajská polévka",
                "ingredients": "Rajčata, cibule, koření",
                "instructions": "Povařte rajčata a rozmixujte.",
            },
            {
                "title": "Česnečka",
                "ingredients": "Česnek, brambory, vývar",
                "instructions": "Vařte vývar a přidejte česnek.",
            },
            {
                "title": "Hrachová polévka",
                "ingredients": "Sušený hrách, mrkev, brambory",
                "instructions": "Vařte hrách a rozmixujte.",
            },
            {
                "title": "Dýňová polévka",
                "ingredients": "Dýně, smetana, koření",
                "instructions": "Opečte dýni a rozmixujte.",
            },
        ],
    }
    created_recipes = []
    user_map = {}
    all_recipes = []

    # Vytvoříme uživatele pro každou kategorii
    for category in test_data.keys():
        user = User(
            username=f"{category}_chef",
            email=f"{category}@test.com",
            password="testpassword",
            profile_picture_url=f"https://placehold.co/100x100?text={category}+Chef",
        )
        db.session.add(user)
        db.session.commit()
        user_map[category] = user.id  # Uložíme ID uživatele pro danou kategorii

    # Vytvoříme recepty a přiřadíme je k uživatelům
    for category, recipes in test_data.items():
        author_id = user_map[category]
        for recipe_data in recipes:
            new_recipe = Recipe(
                title=recipe_data["title"],
                ingredients=recipe_data["ingredients"],
                instructions=recipe_data["instructions"],
                tag=category,
                author_id=author_id,
            )
            db.session.add(new_recipe)
            db.session.commit()
            all_recipes.append(new_recipe)

            # Přidáme placeholder obrázek
            image = RecipeImage(
                recipe_id=new_recipe.id,
                image_url=f"https://placehold.co/300x200?text={recipe_data['title'].replace(' ', '+')}",
            )
            db.session.add(image)

            created_recipes.append(new_recipe.title)

    db.session.commit()

    # Každý uživatel si náhodně oblíbí několik receptů
    all_recipe_ids = [r.id for r in all_recipes]
    for user_id in user_map.values():
        liked_recipes = random.sample(
            all_recipe_ids, k=random.randint(2, 5)
        )  # Každý si oblíbí 2 až 5 receptů
        for recipe_id in liked_recipes:
            like_entry = UserLikedRecipes(user_id=user_id, recipe_id=recipe_id)
            db.session.add(like_entry)

    db.session.commit()

    return jsonify(
        {
            "message": "Testovací recepty a uživatelé byli vytvořeni!",
            "recipes": created_recipes,
        }
    )
