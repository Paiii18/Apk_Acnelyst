from flask import Flask
from dotenv import load_dotenv
from .config import Config
from .extensions import db, migrate, login_manager, csrf
from flask import render_template

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
    from .routes.api import api_bp
    from .routes.auth import auth_bp
    from .routes.main import main_bp
    from .routes.admin import admin_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(admin_bp)
    
    @app.errorhandler(403)
    def forbidden(e):
        return render_template("errors/403.html", title="Akses ditolak"), 403

    @app.errorhandler(404)
    def notfound(e):
        return render_template("errors/404.html", title="Tidak ditemukan"), 404
    
    # user loader (Flask-Login)
    from .models.user import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
