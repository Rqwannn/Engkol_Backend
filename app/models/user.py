from flask_login import UserMixin
from datetime import datetime
from app import db
import uuid

class users(db.Model, UserMixin):
    user_id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    username = db.Coloumn(db.String(30), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(30))
    profile_id = db.relationship("Profile", backref='users', lazy=True, uselist=False)
    is_deleted = db.Coloumn(db.Boolean)

class users_history(db.Model, UserMixin):
    user_history = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    user_id = db.relationship("users", backref='users_story', lazy=True, uselist=False)
    description = db.Column(db.Text)
    history_date = db.Column(db.DateTime)

class profile(db.Model, UserMixin):
    profile_id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    birth_date = db.Column(db.Date)
    telephone_number = db.Column(db.String(15))
    postal_code = db.relationship("pivot_postal_code_location", backref='profile', lazy=True, uselist=False)
    address = db.Column(db.Text)

class bussiness_plan(db.Model, UserMixin):
    bussines_plan_id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    bussines_name = db.Column(db.String(255))
    bussines_email = db.Column(db.String(100))
    bussines_type = db.Column(db.String(50))
    postal_code = db.Column(db.String(10))
    adress = db.Column(db.Text)
    geolocation = db.Column(db.String(100))
    budgets = db.Column(db.Integer)
    customer_age = db.Column(db.Integer)
    target_market = db.Column(db.String(50))
    status = db.Column(db.Boolean)
    is_deleted = db.Column(db.Booolean)

class money_bookeeping(db.Model, UserMixin):
    money_bookeeping_id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    transaction_date = db.Column(db.DateTime)
    transaction_type = db.Column(db.Integer) #ubah
    category_id =  db.Column(db.Integer) #ubah
    description = db.Column(db.Text)
    balances = db.Column(db.Integer)
    id_deleted = db.Column(db.Boolean)

class postal_code_address(db.Model, UserMixin):
    postal_code = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))

class pivot_postel_code_location(db.Model, UserMixin):
    postal_code = db.relationship('postal_code_address', backref="pivot_postal_code_location_backref", lazy='joined')
    provinces_id = db.relationship('provinces', backref= 'pivot_postal_code_location', lazy='joined')
    districts_id = db.relationship('districts', backref = 'pivot_postal_code_location', lazy='joined')
    subdistricts_id = db.relationship('subdistricts', backref = 'pivot_postal_code_location', lazy='joined')

class provinces_list(db.Model, UserMixin):
    province_id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    province_name = db.Column(db.String(30))

class regencys_list(db.Model, UserMixin):
    regency_id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    regencys_name = db.Column(db.String(30))
    provincy_id = db.relationship('provinces_list', backref = 'regencys_list', lazy='joined')

class subdistricts_list(db.Model, UserMix):
    subdistrict_id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    subdistrict_name = db.Column(db.String(30))
    regencys_id = db.relationship('regencys_list', backref = 'subdistricts_list', lazy='joined')