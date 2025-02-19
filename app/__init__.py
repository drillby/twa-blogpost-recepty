import os

import dotenv
from flask import Flask

from .models.models import Tag, db

app = Flask(__name__)

DEVELOPMENT = True

if DEVELOPMENT:
    dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
    out = dotenv.load_dotenv(dotenv_path, verbose=True)
    print(".env soubor načten" if out == True else "Nepodařilo se načíst .env")


app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["BLOB_READ_WRITE_TOKEN"] = os.environ.get("BLOB_READ_WRITE_TOKEN")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")


db.init_app(app)

with app.app_context():
    db.create_all()
    if not Tag.query.first():
        tags = [
            "dezerty",
            "hlavni_jidla",
            "napoje",
            "predkrmy",
            "snidane",
            "svaciny",
            "polevky",
        ]
        for tag in tags:
            tag = Tag(name=tag)
            db.session.add(tag)
            db.session.commit()


from app.views import recipe_routes, search_routes, user_routes
