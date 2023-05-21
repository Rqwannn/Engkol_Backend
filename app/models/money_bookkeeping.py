from app import db
import uuid


class MoneyBookeeping(db.Model):
    money_bookeeping_id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    transaction_date = db.Column(db.DateTime)
    transaction_type = db.Column(db.Integer)  # ubah
    category_id = db.Column(db.Integer)  # ubah
    description = db.Column(db.Text)
    balances = db.Column(db.Integer)
    id_deleted = db.Column(db.Boolean)
