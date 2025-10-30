from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import login_required, current_user
from src.models import User, CommunityPost, Comment, Like
from src.db import db

community_bp = Blueprint('community_bp', __name__)

# Community Feed
@community_bp.route('/community')
@login_required
def community_page():
    posts = CommunityPost.query.order_by(CommunityPost.created_at.desc()).all()
    users = User.query.all()
    return render_template('community.html', posts=posts, user=current_user, users=users)

# Create Post
@community_bp.route('/community/post', methods=['POST'])
@login_required
def create_post():
    content = request.form.get('content')
    if content:
        post = CommunityPost(content=content, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
    return redirect(url_for('community_bp.community_page'))

# Comment
@community_bp.route('/community/comment/<int:post_id>', methods=['POST'])
@login_required
def add_comment(post_id):
    content = request.form.get('content')
    if content:
        comment = Comment(content=content, user_id=current_user.id, post_id=post_id)
        db.session.add(comment)
        db.session.commit()
    return redirect(url_for('community_bp.community_page'))

# Like
@community_bp.route('/community/like/<int:post_id>', methods=['POST'])
@login_required
def like_post(post_id):
    existing_like = Like.query.filter_by(user_id=current_user.id, post_id=post_id).first()
    if existing_like:
        db.session.delete(existing_like)
    else:
        like = Like(user_id=current_user.id, post_id=post_id)
        db.session.add(like)
    db.session.commit()
    return jsonify({'success': True})