import os


class Config:
    DEBUG = True
    TESTING = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default_secret_key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
