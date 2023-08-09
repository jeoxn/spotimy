from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
DB_NAME = "database.db"

def create_website():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "secret-key"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    from .models import Playlist, Song

    with app.app_context():
        db.init_app(app)
        db.create_all()

    from .urls import urls
    app.register_blueprint(urls, url_prefix="/")

    return app