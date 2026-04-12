from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    recipes = db.relationship('Recipe', backref='user', lazy=True)
    history = db.relationship('RecipeHistory', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    steps = db.Column(db.Text, nullable=False)
    diet_type = db.Column(db.String(50), default='any')
    saved_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Recipe {self.title}>'


class RecipeHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ingredients = db.Column(db.Text, nullable=False)
    recipe_text = db.Column(db.Text, nullable=False)
    diet_type = db.Column(db.String(50), default='any')
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<RecipeHistory {self.id}>'