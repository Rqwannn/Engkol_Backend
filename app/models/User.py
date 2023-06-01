from flask_login import UserMixin
from datetime import datetime
from app import db
import uuid

# from app.models.postal_code import Postal_code_address

class Users(db.Model, UserMixin):
    user_id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    username = db.Column(db.String(30), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(30))
#     profile = db.relationship("profile", backref='profile', lazy=True, uselist=True)
#     user_history = db.relationship("user_history", backref='user_history', lazy=True, uselist=True)
#     is_deleted = db.Column(db.Boolean)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow())

# class Users_history(db.Model):
#     user_history = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
#     user_id = db.Column(db.String(36), db.ForeignKey('users.user_id'), nullable=False)
#     description = db.Column(db.Text)
#     history_date = db.Column(db.DateTime, default=datetime.utcnow())
#     created_at = db.Column(db.DateTime, default=datetime.utcnow())

class Profile(db.Model):
    profile_id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    # user_id = db.Column(db.String(36), db.ForeignKey('users.user_id'), nullable=False)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    birth_date = db.Column(db.Date)
    telephone_number = db.Column(db.String(15))
    # postal_code = db.Column(db.String(36), db.ForeignKey('postal_code_address.postal_code'), nullable=False)
    address = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
