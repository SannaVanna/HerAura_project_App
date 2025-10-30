from flask import Blueprint, render_template
from flask_login import login_required, current_user
from src.models import CourseCategory, Course

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