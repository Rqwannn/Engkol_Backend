from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api
from flask_talisman import Talisman
from flask_login import LoginManager

db = SQLAlchemy()
api = Api()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['OPENAI_SECRET_KEY'] = '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'

    db.init_app(app)

    Talisman(app, content_security_policy=None, force_https=True, strict_transport_security=True)

    from app.urls import __URLPATH__

    __URLPATH__()

    api.init_app(app)
    login_manager.init_app(app)

    from app.models.User import Users

    @login_manager.user_loader
    def load_user(user_id):
        
        # since the user_id is just the primary key of our user table, use it in the query for the user

        return Users.query.get(int(user_id))

    Migrate(app, db)

    return app
