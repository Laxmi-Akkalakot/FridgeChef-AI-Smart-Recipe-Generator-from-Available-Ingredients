from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from models.recipe import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        confirm = request.form.get('confirm_password', '').strip()

        # Validations
        if not username or not email or not password:
            flash('All fields are required!', 'error')
            return render_template('register.html')

        if password != confirm:
            flash('Passwords do not match!', 'error')
            return render_template('register.html')

        if len(password) < 6:
            flash('Password must be at least 6 characters!', 'error')
            return render_template('register.html')

        # Check if user exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered! Please login.', 'error')
            return render_template('register.html')

        existing_username = User.query.filter_by(username=username).first()
        if existing_username:
            flash('Username already taken!', 'error')
            return render_template('register.html')

        # Create new user
        hashed_password = generate_password_hash(password)
        new_user = User(
            username=username,
            email=email,
            password=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully! Please login.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        if not email or not password:
            flash('Please fill in all fields!', 'error')
            return render_template('login.html')

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash('Invalid email or password!', 'error')
            return render_template('login.html')

        login_user(user)
        flash(f'Welcome back, {user.username}!', 'success')
        return redirect(url_for('recipe.index'))

    return render_template('login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('auth.login'))