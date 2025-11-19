from flask import Blueprint, render_template
from flask_login import login_required, current_user
from src.models import CommunityPost, ToDo, UserCourse

dashboard_bp = Blueprint('dashboard_bp', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    user_posts = CommunityPost.query.filter_by(user_id=current_user.id).all()
    todos = ToDo.query.filter_by(user_id=current_user.id).all()
    courses = UserCourse.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', user=current_user, posts=user_posts, todos=todos, courses=courses)

#@dashboard_bp.route()
