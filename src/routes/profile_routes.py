import os
from flask import Blueprint, request, redirect, url_for, render_template
from flask_login import login_required, current_user
from src.db import db

profile_bp = Blueprint('profile_bp', __name__)

os.makedirs("static/profile_images", exist_ok=True)

@profile_bp.route('/profile')
@login_required
def profile_page():
    return render_template('profile.html', user=current_user)

@profile_bp.route('/profile/update', methods=['POST'])
@login_required
def update_profile():
    #update text fields
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    dob = request.form.get('dob')
    #current_user.about = request.form.get('about')

    if first_name:
        current_user.first_name = first_name

    if last_name:
        current_user.last_name = last_name

    if email:
        current_user.email = email

    if dob:
        current_user.dob = dob                


    #Handle upload image
    
    image = request.files.get('image')
    if image:
        filename = f"user_{current_user.id}.jpg"
        filepath = os.path.join('static/profile_images', filename)
        image.save(filepath)
        current_user.profile_image = filename
    else:
        print("No image uploaded.")    

    db.session.commit()

    return redirect(url_for('profile_bp.profile_page'))