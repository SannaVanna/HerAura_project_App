from flask import Blueprint, request, render_template, flash, redirect, url_for, jsonify
from src.models import User
from src.db import db
from flask_login import login_user, logout_user, login_required, current_user

auth_bp = Blueprint('auth_bp', __name__)


# ---------- Pages ----------
@auth_bp.route('/')
def index():
    if current_user.is_authenticated:  # Flask-Login's current_user
        return redirect(url_for('dashboard_bp.dashboard'))
    return render_template('index.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    print("SIGN-UP ROUTE TRIGGERED............")
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email').strip().lower()
        dob = request.form.get('dob')
        password = request.form.get('password')

        if User.query.filter(User.email == email).first():
            flash("Email already registered.", "warning")
            return redirect(url_for('auth_bp.register'))

        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            dob=dob,
            password=password
        )

        db.session.add(user)
        db.session.commit()

        login_user(user)  # ← Actually log them in
        flash("Registration successful.", "success")
        return redirect(url_for('dashboard_bp.dashboard'))

    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    print("LOGIN ROUTE TRIGGERED................")

    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and user.confirm_password(password):
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for("dashboard_bp.dashboard"))
        else:
            flash("Invalid email or password", "danger")
            return redirect(url_for('auth_bp.login'))
    return render_template('login.html')


# ---------- Utility endpoints ----------
@auth_bp.route('/api/profile')
def api_profile():
    if not current_user.is_authenticated:
        return jsonify({'error': 'not authenticated'}), 401
    data = {
        'id': current_user.id,
        'username': getattr(current_user, 'username', None),
        'email': current_user.email
    }
    return jsonify(data)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth_bp.index'))