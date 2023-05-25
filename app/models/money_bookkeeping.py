from app import db
import uuid
from datetime import datetime

class Money_bookeeping(db.Model):
    money_bookeeping_id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    transaction_date = db.Column(db.DateTime)
    transaction_type = db.Column(db.Integer)  # ubah
    category_id = db.Column(db.Integer)  # ubah
    description = db.Column(db.Text)
    balances = db.Column(db.Integer)
    id_deleted = db.Column(db.Boolean)

class Bookeeping_account(db.Model):
    bookeeping_account_id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    name_account = db.Column(db.String(50))
    role_id = db.Column(db.String(50), db.ForeignKey('money_bookeeping_role.role_id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    # created_at = db.Column(db.DateTime, server_default=db.func.now())
    deleted_at = db.Column(db.DateTime, default=datetime.utcnow())

class Money_bookeeping_role(db.Model):
    role_id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    role_name = db.Column(db.String(25))
    role_status = db.Column(db.String(2))

class Activity_role(db.Model):
    activity_id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    money_bookeeping_account = db.Column(db.String(36), db.ForeignKey('bookeeping_account.bookeeping_account_id'))
    activity = db.Column(db.String(255))
    perubahan = db.Column(db.String(255))
    time = db.Column(db.DateTime, default=datetime.utcnow())
