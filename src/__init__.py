from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .flasklogin import login_manager
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


# app = Flask(__name__, static_folder="static")
app = Flask(__name__, static_folder="static")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///girlUser.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)
migrate = Migrate(app, db)

login_manager.init_app(app)
login_manager.login_view = 'auth_bp.login'


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


    with app.app_context():
        db.create_all()

    return app
