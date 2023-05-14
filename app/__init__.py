from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api

db = SQLAlchemy()
api = Api()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)

    # Register App

    # Register Path

    from app.path_url.bussines_plan import BUSSINES_PLAN_API_PATH

    BUSSINES_PLAN_API_PATH()

    api.init_app(app)

    Migrate(app, db)

    return app