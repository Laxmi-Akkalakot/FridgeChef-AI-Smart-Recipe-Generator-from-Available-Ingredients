from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from models.recipe import db, Recipe

saved_bp = Blueprint('saved', __name__)

@saved_bp.route('/save', methods=['POST'])
@login_required
def save_recipe():
    title = request.form.get('title', 'My Recipe')
    ingredients = request.form.get('ingredients')
    steps = request.form.get('steps')
    diet_type = request.form.get('diet_type', 'any')

    new_recipe = Recipe(
        title=title,
        ingredients=ingredients,
        steps=steps,
        diet_type=diet_type,
        user_id=current_user.id
    )
    db.session.add(new_recipe)
    db.session.commit()
    return redirect(url_for('saved.favourites'))

@saved_bp.route('/favourites')
@login_required
def favourites():
    recipes = Recipe.query.filter_by(
        user_id=current_user.id
    ).order_by(Recipe.saved_at.desc()).all()
    return render_template('favourites.html', recipes=recipes)

@saved_bp.route('/delete/<int:id>')
@login_required
def delete_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    if recipe.user_id != current_user.id:
        return redirect(url_for('saved.favourites'))
    db.session.delete(recipe)
    db.session.commit()
    return redirect(url_for('saved.favourites'))