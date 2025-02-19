import os

import dotenv
from flask import Flask

from .models.models import db

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


from app.views import recipe_routes, search_routes, user_routes
