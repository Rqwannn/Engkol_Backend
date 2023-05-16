from datetime import datetime
from app import db
import uuid

class bussiness_plan(db.Model):
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
    is_deleted = db.Column(db.Boolean)

class postal_code_address(db.Model):
    postal_code = db.Column(db.String(36), primary_key=True)

class pivot_postel_code_location(db.Model):
    postel_code_location = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    postal_code = db.column(db.String(36), db.ForeignKey('postal_code_address.postal_code'))
    provinces_id = db.Column(db.String(36), db.ForeignKey('provinces_list.province_id'), nullable=False)
    districts_id = db.Column(db.String(36), db.ForeignKey('regencys_list.regency_id'), nullable=False)
    subdistricts_id = db.Column(db.String(36), db.ForeignKey('subdistricts_list.subdistrict_id'), nullable=False)

class provinces_list(db.Model):
    province_id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    province_name = db.Column(db.String(30))

class regencys_list(db.Model):
    regency_id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    regencys_name = db.Column(db.String(30))
    provincy_id = db.Column(db.String(36), db.ForeignKey('provinces_list.province_id'), nullable=False)

class subdistricts_list(db.Model):
    subdistrict_id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    subdistrict_name = db.Column(db.String(30))
    regencys_id = db.Column(db.String(36), db.ForeignKey('regencys_list.regency_id'), nullable=False)