from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    profile_picture_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    recipes = db.relationship("Recipe", back_populates="author", cascade="all, delete")
    liked_recipes = db.relationship(
        "Recipe", secondary="user_liked_recipes", back_populates="liked_by"
    )

    def __init__(self, username, email, password, profile_picture_url=None):
        self.username = username
        self.email = email
        self.set_password(password)
        self.profile_picture_url = profile_picture_url

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Recipe(db.Model):
    __tablename__ = "recipes"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author_id = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), nullable=True)

    author = db.relationship("User", back_populates="recipes")
    images = db.relationship(
        "RecipeImage", back_populates="recipe", cascade="all, delete-orphan"
    )
    liked_by = db.relationship(
        "User", secondary="user_liked_recipes", back_populates="liked_recipes"
    )
    tag = db.relationship("Tag", back_populates="recipes")


class Tag(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    recipes = db.relationship("Recipe", back_populates="tag")


class RecipeImage(db.Model):
    __tablename__ = "recipe_images"

    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(
        db.Integer, db.ForeignKey("recipes.id", ondelete="CASCADE"), nullable=False
    )
    image_url = db.Column(db.String(255), nullable=False)

    recipe = db.relationship("Recipe", back_populates="images")


class UserLikedRecipes(db.Model):
    __tablename__ = "user_liked_recipes"

    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    recipe_id = db.Column(
        db.Integer, db.ForeignKey("recipes.id", ondelete="CASCADE"), primary_key=True
    )
