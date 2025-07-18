from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from .config import Config;
import pkgutil
import importlib
from . import models
from .middlewares.secret_key import secret_key
from flask_cors import CORS
db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()

def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object(Config)
    app.config["DEBUG"] = True
    app.config.from_envvar("FLASK_ENV", silent=True)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    secret_key(app)
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)
    migrate.init_app(app, db)
    import_all_models()
    from .routes import bp as auth_bp
    app.register_blueprint(auth_bp)

    return app

def import_all_models():
    for loader, name, is_pkg in pkgutil.iter_modules(models.__path__):
        importlib.import_module(f"{models.__name__}.{name}")
