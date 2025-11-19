from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .db import db

# -------------------------------
# USER MODEL
# -------------------------------
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    dob = db.Column(db.String, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    profile_image = db.Column(db.String(300), default='default_profile.png')
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    posts = db.relationship('CommunityPost', backref='user', lazy=True)
    comments = db.relationship('Comment', backref='user', lazy=True)
    likes = db.relationship('Like', backref='user', lazy=True)
    todos = db.relationship('ToDo', backref='user', lazy=True)
    ai_chats = db.relationship('AIChat', backref='user', lazy=True)
    health_logs = db.relationship('HealthTracker', backref='user', lazy=True)
    course_progress = db.relationship('UserCourse', backref='user', lazy=True)

    is_authenticated = True
    is_active = True
    is_anonymous = False

    def __init__(self, first_name, last_name, email, dob,  password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.dob = dob
        self.password = generate_password_hash(password)

    def confirm_password(self, password):
        return check_password_hash(self.password, password)

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return f"<Users {self.email}>"


# -------------------------------
# COMMUNITY MODELS
# -------------------------------
class CommunityPost(db.Model):
    __tablename__ = 'community_posts'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Relationships
    comments = db.relationship('Comment', backref='post', cascade="all, delete-orphan", lazy=True)
    likes = db.relationship('Like', backref='post', cascade="all, delete-orphan", lazy=True)


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('community_posts.id'), nullable=False)


class Like(db.Model):
    __tablename__ = 'likes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('community_posts.id'), nullable=False)


# -------------------------------
# MENTOR MODEL
# -------------------------------
class Mentor(db.Model):
    __tablename__ = 'mentors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    title = db.Column(db.String(150))
    field = db.Column(db.String(100))
    bio = db.Column(db.Text)
    contact_email = db.Column(db.String(150))
    contact_url = db.Column(db.String(250))
    on_app = db.Column(db.Boolean, default=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)


# -------------------------------
# COURSES / LEARN A SKILL
# -------------------------------
class CourseCategory(db.Model):
    __tablename__ = 'course_categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # e.g. "Tech" or "Craft"
    description = db.Column(db.Text)
    courses = db.relationship('Course', backref='category', lazy=True)


class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    video_url = db.Column(db.String(500))  # e.g., YouTube link
    category_id = db.Column(db.Integer, db.ForeignKey('course_categories.id'))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    user_progress = db.relationship('UserCourse', backref='course', lazy=True)

    def __repr__(self):
        return f"<Course {self.title}>"



class UserCourse(db.Model):
    __tablename__ = 'user_courses'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    completed = db.Column(db.Boolean, default=False)
    date_started = db.Column(db.DateTime, default=datetime.utcnow)
    date_completed = db.Column(db.DateTime)


# -------------------------------
# TO-DO LIST
# -------------------------------
class ToDo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(250), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


# -------------------------------
# HEALTH TRACKER (MENSTRUAL CYCLE)
# -------------------------------
class HealthTracker(db.Model):
    _tablename__ = 'health_tracker'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # ✅ must be here
    age = db.Column(db.Integer, nullable=False)
    cycle_start_date = db.Column(db.String(50), nullable=False)
    cycle_length = db.Column(db.Integer, nullable=False)
    flow_days = db.Column(db.Integer, nullable=False)
    mood = db.Column(db.String(50))
    notes = db.Column(db.Text)
    next_period_date = db.Column(db.String(50))
    health_message = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f"<HealthTracker UserID:{self.user_id} next_period:{self.next_period_date}>"


# -------------------------------
# AI CHATBOT LOGS
# -------------------------------
class AIChat(db.Model):
    __tablename__ = 'ai_chats'
    id = db.Column(db.Integer, primary_key=True)
    user_message = db.Column(db.Text, nullable=False)
    bot_response = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)