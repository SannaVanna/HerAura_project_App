from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .flasklogin import login_manager
from flask_login import current_user
from datetime import datetime
from .db import db
#from routes.mentor_routes import routes
from .routes.dashboard_routes import dashboard_bp
from .routes.community_routes import community_bp
from .routes.mentor_routes import mentor_bp
from .routes.learn_routes import learn_bp
from .routes.todo_routes import todo_bp
from .routes.health_routes import health_bp
from .routes.ai_routes import ai_bp
from .routes.auth_routes import auth_bp
from .routes.profile_routes import profile_bp
from src.utils import time_ago
from src.utils import is_user_online
import os


# app = Flask(__name__, static_folder="static")
app = Flask(__name__, static_folder="static")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///girlUser.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'profile_images')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db.init_app(app)
migrate = Migrate(app, db)

login_manager.init_app(app)
login_manager.login_view = 'auth_bp.login'


@app.before_request
def update_last_seen():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


def create_app():
    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = 'HerAuraSecretKey54936'
    #app.register_blueprint(routes, url_prefix="/")
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(community_bp)
    app.register_blueprint(mentor_bp)
    app.register_blueprint(learn_bp)
    app.register_blueprint(todo_bp)
    app.register_blueprint(health_bp)
    app.register_blueprint(ai_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(profile_bp)

    app.jinja_env.globals.update(time_ago=time_ago)
    app.jinja_env.globals['is_user_online'] = is_user_online


    with app.app_context():
        db.create_all()

    return app
