from flask import Blueprint, render_template
from flask_login import login_required, current_user
from src.models import CourseCategory, Course
from src.db import db

learn_bp = Blueprint('learn_bp', __name__)

@learn_bp.route('/learn')
@login_required
def learn_skill():
    categories = CourseCategory.query.all()
    return render_template('learn_skill.html', categories=categories)

@learn_bp.route('/learn/category/<int:cat_id>')
@login_required
def category_courses(cat_id):
    category = CourseCategory.query.get_or_404(cat_id)
    courses = Course.query.filter_by(category_id=cat_id).all()
    return render_template('course_detail.html', category=category, courses=courses)

from flask import request, jsonify

# ---------- API ENDPOINTS ----------

# Get all categories
@learn_bp.route('/api/categories', methods=['GET'])
def api_get_categories():
    categories = CourseCategory.query.all()
    data = []
    for cat in categories:
        data.append({
            'id': cat.id,
            'name': cat.name,
            'description': cat.description
        })
    return jsonify(data), 200


# Add a new category
@learn_bp.route('/api/categories', methods=['POST'])
def api_add_category():
    payload = request.get_json()
    cat = CourseCategory(
        name=payload.get('name'),
        description=payload.get('description')
    )
    db.session.add(cat)
    db.session.commit()
    return jsonify({'ok': True, 'id': cat.id}), 201


# Get all courses
@learn_bp.route('/api/courses', methods=['GET'])
def api_get_courses():
    courses = Course.query.all()
    data = []
    for c in courses:
        data.append({
            'id': c.id,
            'title': c.title,
            'description': c.description,
            'video_url': c.video_link,
            'category_id': c.category_id
        })
    return jsonify(data), 200


# Add new course
@learn_bp.route('/api/courses', methods=['POST'])
def api_add_course():
    payload = request.get_json()
    c = Course(
        title=payload.get('title'),
        description=payload.get('description'),
        video_url=payload.get('video_link'),
        category_id=payload.get('category_id')
    )
    db.session.add(c)
    db.session.commit()
    print(c)
    return jsonify({'ok': True, 'id': c.id}), 201