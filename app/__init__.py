import os

import dotenv
from flask import Flask
from flask_login import LoginManager

from .models.models import User, db

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)


DEVELOPMENT = True

if DEVELOPMENT:
    dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
    out = dotenv.load_dotenv(dotenv_path, verbose=True)
    print(".env soubor načten" if out == True else "Nepodařilo se načíst .env")


app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["BLOB_READ_WRITE_TOKEN"] = os.environ.get("BLOB_READ_WRITE_TOKEN")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")
app.config["TESTING"] = os.environ.get("TESTING", "False")


db.init_app(app)

with app.app_context():
    db.create_all()

# nějaký důležitý kód

from app.views import recipe_routes, search_routes, user_routes
