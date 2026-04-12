from flask import Flask
from flask_login import LoginManager
from config import Config
from models.recipe import db, User
from routes.recipe_routes import recipe_bp
from routes.saved_routes import saved_bp
from routes.auth_routes import auth_bp

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

# Setup Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please login to access this page!'
login_manager.login_message_category = 'error'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.register_blueprint(recipe_bp)
app.register_blueprint(saved_bp)
app.register_blueprint(auth_bp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("✅ Database created!")
    app.run(debug=True)