from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api
from flask_talisman import Talisman

db = SQLAlchemy()
api = Api()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['OPENAI_SECRET_KEY'] = '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'

    db.init_app(app)

    Talisman(app, content_security_policy=None, force_https=True, strict_transport_security=True)

    # Register App

    # Register Path

    from app.path_url.bussines_plan import BUSSINES_PLAN_API_PATH

    BUSSINES_PLAN_API_PATH()

    api.init_app(app)

    Migrate(app, db)

    return app