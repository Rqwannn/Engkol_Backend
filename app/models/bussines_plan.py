from datetime import datetime
from app import db
import uuid

from app.models.money_bookkeeping import Money_bookeeping

class Bussiness_plan(db.Model):
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
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    bookeeping_ticket = db.relationship("bookeeping_ticket", backref="bookeeping_ticket", lazy=True, uselist=True)


class Pivot_bussines_bookkeeping(db.Model):
    postel_code_location = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    bussines_plan_id = db.Column(db.String(36), db.ForeignKey('bussiness_plan.bussines_plan_id'), nullable=False)
    money_bookeeping_id = db.Column(db.String(36), db.ForeignKey('money_bookeeping.money_bookeeping_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())

class Bookeeping_ticket(db.Model):
    bookeeping_ticket_id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    bussines_plan_id = db.Column(db.String(36), db.ForeignKey('bussines_plan.bussines_plan_id'), nullable=False)
    money_bookeeping_id = db.Column(db.String(36), db.ForeignKey('money_bookeeping.money_bookeeping_id'), nullable=False)
    created_at = datetime.now()
