from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from services.ai_service import get_recipe, get_nutrition
from models.recipe import db, RecipeHistory

recipe_bp = Blueprint('recipe', __name__)

@recipe_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    recipe_text = None
    ingredients = ''
    diet_type = 'any'
    error = None
    nutrition = None

    if request.method == 'POST':
        ingredients = request.form.get('ingredients', '').strip()
        diet_type = request.form.get('diet_type', 'any')

        if not ingredients:
            error = "Please enter at least one ingredient!"
        else:
            ingredient_list = [i.strip() for i in ingredients.split(',')]
            try:
                recipe_text = get_recipe(ingredient_list, diet_type)
                nutrition = get_nutrition(ingredients, recipe_text)

                # Save to history
                history = RecipeHistory(
                    ingredients=ingredients,
                    recipe_text=recipe_text,
                    diet_type=diet_type,
                    user_id=current_user.id
                )
                db.session.add(history)

                # Keep only last 10 per user
                all_history = RecipeHistory.query.filter_by(
                    user_id=current_user.id
                ).order_by(RecipeHistory.generated_at.desc()).all()

                if len(all_history) > 10:
                    for old in all_history[10:]:
                        db.session.delete(old)

                db.session.commit()

            except Exception as e:
                error = f"Something went wrong: {str(e)}"

    history_list = RecipeHistory.query.filter_by(
        user_id=current_user.id
    ).order_by(RecipeHistory.generated_at.desc()).limit(10).all()

    return render_template('index.html',
                           recipe=recipe_text,
                           nutrition=nutrition,
                           ingredients=ingredients,
                           diet_type=diet_type,
                           error=error,
                           history_list=history_list)