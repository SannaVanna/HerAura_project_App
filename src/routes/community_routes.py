from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from flask_login import login_required, current_user
from src.models import User, CommunityPost, Comment, Like, CommentReaction
from src.db import db

community_bp = Blueprint('community_bp', __name__)

# Community Feed
@community_bp.route('/community')
@login_required
def community_page():
    posts = CommunityPost.query.order_by(CommunityPost.created_at.desc()).all()
    users = User.query.all()
    print(posts)
    print(users)
    return render_template('community.html', posts=posts, user=current_user, users=users)

# Create Post
@community_bp.route('/community/post', methods=['POST'])
@login_required
def create_post():
    content = request.form.get('content')
    if content:
        post = CommunityPost(content=content, user_id=current_user.id)
        print(post)
        db.session.add(post)
        db.session.commit()
    return redirect(url_for('community_bp.community_page'))

# Edit Post (GET + POST)
@community_bp.route('/community/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = CommunityPost.query.get_or_404(post_id)

    # Security: Only the owner can edit
    if post.user_id != current_user.id:
        return "Unauthorized", 403

    if request.method == 'POST':
        new_content = request.form.get('content')
        
        if new_content:
            post.content = new_content
            db.session.commit()
            print(new_content)
            return redirect(url_for('community_bp.community_page'))

    return render_template('edit_post.html', post=post, user=current_user)
    

# Delete Post
@community_bp.route('/community/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = CommunityPost.query.get_or_404(post_id)

    # Security: Only the owner can delete
    if post.user_id != current_user.id:
        return jsonify({"error": f"Post with ID {post_id} Not Found"}), 404

    db.session.delete(post)
    db.session.commit()
    print(f"Deleting post {post} by {post.user_id}")
    flash("Post deleted successfully!", "success")
    return redirect(url_for('community_bp.community_page'))

# Comment
@community_bp.route('/community/comment/<int:post_id>', methods=['POST'])
@login_required
def add_comment(post_id):
    content = request.form.get('content')
    if content:
        comment = Comment(content=content, user_id=current_user.id, post_id=post_id)
        db.session.add(comment)
        print(User.comments)        
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
    #return jsonify({'success': True})
    return redirect(url_for('community_bp.community_page'))

@community_bp.route('/community/comment/react/<int:comment_id>', methods=['POST'])
@login_required
def comment_react(comment_id):
    comment = Comment.query.get_or_404(comment_id)

    #check if user already reacted
    existing_rection = CommentReaction.query.filter_by(user_id=current_user.id, comment_id=comment.id).first()

    if existing_rection:
        db.session.delete(existing_rection) # remove reaction if exists
        db.session.commit()
        #return jsonify({'successs': True, 'reacted': False})
        return redirect(url_for('community_bp.community_page'))
    
    reaction = CommentReaction(user_id=current_user.id, comment_id=comment.id)
    db.session.add(reaction)
    db.session.commit()
    #return jsonify({'successs': True, 'reacted': False})
    return redirect(url_for('community_bp.community_page'))
