import datetime
import random

from faker import Faker
from flask import redirect, render_template, request, url_for, jsonify

from app import app, db

from ..models.models import Recipe, RecipeImage, User, UserLikedRecipes

from fuzzywuzzy import fuzz

from sqlalchemy.sql.expression import func, desc

import re



@app.route("/search")
def search():
    query = request.args.get("query").lower()
    
    #empty query returns index.html
    if not query:
        return redirect(url_for("index"))
    

    # searching using tags
    tag_synonyms = {
        "vecere": ["večeře", "večeře recepty", "recepty na večeři", "co k večeři", "večerní jídla", "jídla k večeři", "večeře pro rodinu", "rychlá večeře", "večerní menu", "večeře pro dvě", "večeře pro děti", "co připravit na večeři"],
        "snidane": ["snídaně", "snídaně recepty", "co na snídani", "rychlá snídaně", "snídaně pro děti", "snídaně pro dva", "ideální snídaně", "sladká snídaně", "slaná snídaně", "snídaně do postele", "snídaně na víkend"],
        "dezerty": ["dezert", "dezerty recepty", "sladkosti", "koláče", "dorty", "pečení", "cukroví", "sladké jídlo", "sladké recepty", "koláče a dezerty", "vánoční cukroví", "sladké dobroty", "dort na oslavu"],
        "hlavni_jidla": ["hlavní jídla", "hlavní jídlo", "hlavní chod", "hlavní pokrm", "co na oběd", "oběd", "jídlo k obědu", "jednoduchá hlavní jídla", "hlavní jídlo pro rodinu", "jídlo pro dva", "ráno k obědu", "dobrá hlavní jídla", "oběd pro děti"],
        "napoje": ["nápoje", "pití", "nápoje recepty", "co na pití", "lahodné nápoje", "zdravé nápoje", "nealkoholické nápoje", "smoothie", "cocktaily", "ovocné nápoje", "studené nápoje", "teplé nápoje", "nápoje pro děti"],
        "polevky": ["polévky", "polévka", "polévka recepty", "zeleninová polévka", "masová polévka", "rychlá polévka", "domácí polévky", "krémové polévky", "česnečka", "vývary", "čočková polévka", "zeleninový vývar", "pohanková polévka"],
        "predkrmy": ["předkrmy", "předkrm", "snídaňové předkrmy", "předkrmy recepty", "studené předkrmy", "teplé předkrmy", "ideální předkrm", "sýrové předkrmy", "předkrmy pro hosty", "lahodné předkrmy", "malé jídlo", "co na předkrm"],
        "svaciny": ["svačiny", "svačina", "co na svačinu", "svačiny pro děti", "svačiny pro dospělé", "rychlé svačiny", "svačiny do školy", "svačiny pro školáky", "svačina pro sportovce", "malé jídlo", "sladká svačina", "slaná svačina", "svačiny do práce"]
    }
        
    for tag, synonyms in tag_synonyms.items():
        if any(synonym in query for synonym in synonyms):
            recipes_tag = Recipe.query.filter(Recipe.tag == tag).all()
            return render_template("search-results.html", res=recipes_tag, query=query)


    #searching using title or ingredients
    recipes_all = Recipe.query.all()
    matches = []

    for recipe in recipes_all:

        query_words = re.split(r'[\s,;.\-!]+', query.lower())  


           #title searching 
        title_words = re.split(r'[\s,;.\-!]+', recipe.title.lower())  
        
        match_ratios_title = [
            fuzz.ratio(title_word, query_word)  
            for title_word in title_words if len(title_word) > 2 
            for query_word in query_words if len(query_word) > 2  
         ]

        match_ratio_title  = max(match_ratios_title)
        
        #Testing matches title
        """
        for title_word in title_words:  
            for word in query_words:
                if fuzz.ratio(title_word, word) > 70:
                    print(title_word,fuzz.ratio(title_word, word), word)
        """


            #ingredients searching 
        ingredients = re.split(r'[\s,;.\-!]+', recipe.ingredients.lower())  
     
        match_ratios_ingredients = [
            fuzz.ratio(ingredient, query_word)  
            for ingredient in ingredients if len(ingredient) > 2 
            for query_word in query_words if len(query_word) > 2  
         ]

        match_ratio_ingredients = max(match_ratios_ingredients)
    
        #Testing matches ingredients
        """
        print(match_ratio_title)
        for ingredient in ingredients:  
            for word in query_words:
                if fuzz.ratio(ingredient, word) > 79:
                    print(ingredient,fuzz.ratio(ingredient, word), word)
        """          


        #results of matching 
        if match_ratio_title > 79 or match_ratio_ingredients > 79: 
            weighted_match_ratio = 0.55 * match_ratio_title + 0.45 * match_ratio_ingredients 
            matches.append((recipe, weighted_match_ratio))



    #sorting matches by weighted ratio              
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
        searching_tag = "svacina"
    elif client_time < 13:
        searching_tag = "hlavni_jidla"
    elif client_time < 15:
        searching_tag = "dezerty"
    elif client_time < 17:
        searching_tag = "svacina"
    else:
        searching_tag = "vecere"

    recipes_featured = Recipe.query.filter(Recipe.tag == searching_tag).order_by(func.random()).limit(4).all()

      # Newest recepies 
    page = request.args.get("page", 1, type=int)
    per_page = 10

    recipes_paginated = Recipe.query.order_by(desc(Recipe.created_at)).paginate(page=page, per_page=per_page, error_out=False)



    return render_template("index.html", recipes=recipes_paginated.items, recipes_featured=recipes_featured, next_page=recipes_paginated.next_num if recipes_paginated.has_next else None)



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
