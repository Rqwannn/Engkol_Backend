from flask_login import UserMixin
from datetime import datetime
from app import db
import uuid


class Users(db.Model, UserMixin):
    user_id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    username = db.Column(db.String(30), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(30))
    profile = db.relationship("profile", backref='profile', lazy=True, uselist=True)
    is_deleted = db.Column(db.Boolean)


class UsersHistory(db.Model):
    user_history = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.user_id'), nullable=False)
    description = db.Column(db.Text)
    history_date = db.Column(db.DateTime, default=datetime.utcnow())


class Profile(db.Model):
    profile_id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.user_id'), nullable=False)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    birth_date = db.Column(db.Date)
    telephone_number = db.Column(db.String(15))
    postal_code = db.Column(db.String(36), db.ForeignKey('postal_code_address.postal_code'), nullable=False)
    address = db.Column(db.Text)


class bookeeping_account(db.Model):
    bookeeping_account_id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    name_account = db.Column(db.String(50))
    role_id = db.Column(db.String(50), db.ForeignKey('money_bookeeping_role.role_id'))
    created_at = db.DateTimeField(auto_now_add=True)
    deleted_at =db.DateTimeField(auto_now_add=True)


class money_bookeeping_role(db.Model):
    role_id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    role_name = db.Column(db.String(25))
    role_status = db.Column(db.String(2))


class activity_role(db.Model):
    activity_id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    money_bookeeping_account = db.Column(db.String(36), db.ForeignKey('bookeeping_account.bookeeping_account_id'))
    activity = db.Column(db.String(255))
    perubahan = db.Column(db.String(255))
    time = db.DateTimeField(auto_now_add=True)