from flask import Blueprint, request, render_template, flash, session, redirect, url_for, g, jsonify, Request
from src.models import db, User, Mentor
from src.flasklogin import login_manager
from src.db import db
from flask_login import current_user, login_user, logout_user, login_required
import os

mentor_bp = Blueprint('mentor_bp', __name__)

# ---------- Mentor connect ----------

@mentor_bp.route('/mentors_page')
def mentors_page():
    u = current_user
    mentors = Mentor.query.order_by(Mentor.field, Mentor.name).all()
    return render_template('mentors_connect.html', mentors=mentors, user=u)

# REST: get mentors (JSON)
@mentor_bp.route('/api/mentors', methods=['GET'])
def api_get_mentors():
    mentors = Mentor.query.order_by(Mentor.field, Mentor.name).all()
    data = []
    for m in mentors:
        data.append({
            'id': m.id,
            'name': m.name,
            'title': m.title,
            'field': m.field,
            'bio': m.bio,
            'contact_email': m.contact_email,
            'contact_url': m.contact_url,
            'on_app': m.on_app
        })
    return jsonify(data)


# REST: add mentor (admin or seeding)
@mentor_bp.route('/api/mentors', methods=['POST'])
def api_add_mentor():
    payload = request.get_json()
    # minimal validation
    m = Mentor(
        name = payload.get('name'),
        title = payload.get('title'),
        field = payload.get('field'),
        bio = payload.get('bio'),
        contact_email = payload.get('contact_email'),
        contact_url = payload.get('contact_url'),
        on_app = payload.get('on_app', False)
    )
    db.session.add(m)
    db.session.commit()
    return jsonify({'ok': True, 'id': m.id}), 201


# Mentor detail page
@mentor_bp.route('/mentor/<int:mentor_id>')
def mentor_detail(mentor_id):
    m = Mentor.query.get_or_404(mentor_id)
    return render_template('mentor_detail.html', mentor=m)


