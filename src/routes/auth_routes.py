from flask import Blueprint, request, render_template, flash, session, redirect, url_for, g, jsonify, Request
from src.models import db, User
from src.flasklogin import login_manager
from src.db import db
from flask_login import current_user, login_user, logout_user, login_required
import os

auth_bp = Blueprint('auth_bp', __name__)


# ---------- Simple auth helpers (demo-only) ----------
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def current_user():
    if 'user_id' in session:
        return User.query.get(session['user_id'])
    return None

# ---------- Pages ----------
@auth_bp.route('/')
def index():
    u = current_user()
    if u:
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

        print(request.form)
        db.session.add(user)
        db.session.commit()
        # print(user)
        # print(User)

        load_user(user.id)
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


# ---------- Small utility endpoints ----------
@auth_bp.route('/api/profile')
def api_profile():
    u = current_user()
    if not u:
        return jsonify({'error': 'not authenticated'}), 401
    data = {'id': u.id, 'username': u.username, 'email': u.email}
    return jsonify(data)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('you have been looged out.', 'info')
    return redirect(url_for('auth_bp.index'))