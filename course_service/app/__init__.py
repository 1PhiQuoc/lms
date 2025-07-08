from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()

def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config.from_envvar("FLASK_ENV", silent=True)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    from .routes import bp as course_bp
    app.register_blueprint(course_bp)

    return app
