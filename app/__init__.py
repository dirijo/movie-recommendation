from flask import Flask
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from .models import configure as config_db
from .serializer import configure as config_ma


def create_app():
    app = Flask(__name__)
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = "sqlite:////tmp/movies.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    app.config["DEBUG"] = True

    config_db(app)
    config_ma(app)
    Migrate(app, app.db)

    from .movies import bp_movies

    app.register_blueprint(bp_movies)
    return app
