from flask import Flask
from dotenv import load_dotenv
from .config import Config
from .extensions import db, migrate, login_manager, csrf

load_dotenv()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    # register blueprints
    from .routes.auth import auth_bp
    from .routes.main import main_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    # user loader (Flask-Login)
    from .models.user import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
