import random

from flask import jsonify
from flask_login import login_required

from app import app, db

from ..models.models import Recipe, RecipeImage, User, UserLikedRecipes


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
        ],
        "predkrmy": [
            {
                "title": "Bruschetta",
                "ingredients": "Chléb, rajčata, česnek, bazalka",
                "instructions": "Opečte chléb, přidejte směs rajčat a česneku.",
            },
            {
                "title": "Caprese salát",
                "ingredients": "Rajčata, mozzarella, bazalka",
                "instructions": "Nakrájejte ingredience a servírujte s olivovým olejem.",
            },
        ],
        "snidane": [
            {
                "title": "Vaječná omeleta",
                "ingredients": "Vejce, mléko, sůl, pepř",
                "instructions": "Rozšlehejte vejce a osmažte na pánvi.",
            },
            {
                "title": "Ovesná kaše",
                "ingredients": "Ovesné vločky, mléko, med",
                "instructions": "Povařte vločky v mléce a oslaďte medem.",
            },
        ],
        "svaciny": [
            {
                "title": "Jablko s arašídovým máslem",
                "ingredients": "Jablko, arašídové máslo",
                "instructions": "Nakrájejte jablko a podávejte s máslem.",
            },
            {
                "title": "Tvaroh s ovocem",
                "ingredients": "Tvaroh, jahody, med",
                "instructions": "Smíchejte tvaroh s ovocem a oslaďte medem.",
            },
        ],
        "vecere": [
            {
                "title": "Grilovaný losos",
                "ingredients": "Losos, citron, bylinky",
                "instructions": "Opečte lososa a dochuťte citronem.",
            },
            {
                "title": "Zapečené brambory",
                "ingredients": "Brambory, sýr, šunka",
                "instructions": "Nakrájejte brambory a zapečte se sýrem a šunkou.",
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
                image_url=f"https://placehold.co/1000x200?text={recipe_data['title'].replace(' ', '+')}",
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


@login_required
@app.route("/delete-all-data")
def delete_all_data():
    try:
        # Smazání všech záznamů v databázi
        db.session.query(UserLikedRecipes).delete()
        db.session.query(RecipeImage).delete()
        db.session.query(Recipe).delete()
        db.session.query(User).delete()

        # Uložíme změny
        db.session.commit()

        return jsonify({"message": "Všechna data byla úspěšně smazána!"})

    except Exception as e:
        db.session.rollback()  # Vrácení zpět v případě chyby
        return jsonify({"error": str(e)}), 500
