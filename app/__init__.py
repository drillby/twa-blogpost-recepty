import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)


app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["DATABASE_URL"] = os.environ.get("DATABASE_URL")
app.config["BLOB_READ_WRITE_TOKEN"] = os.environ.get("BLOB_READ_WRITE_TOKEN")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


from app.views import recipe_routes, search_routes, user_routes
