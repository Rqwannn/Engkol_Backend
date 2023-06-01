# from app import db
# import uuid
# from datetime import datetime

# class Postal_code_address(db.Model):
#     postal_code = db.Column(db.String(36), primary_key=True)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow())

# class Provinces_list(db.Model):
#     province_id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
#     province_name = db.Column(db.String(30))
#     regencys_list = db.relationship("regencys_list", backref="regencys_list", lazy=True, uselist=False)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow())

# class Regencys_list(db.Model):
#     regency_id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
#     regencys_name = db.Column(db.String(30))
#     provincy_id = db.Column(db.String(36), db.ForeignKey('provinces_list.province_id'), nullable=False)
#     subdistricts_list = db.relationship("subdistricts_list", backref="subdistricts_list", lazy=True, uselist=False)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow())

# class Subdistricts_list(db.Model):
#     subdistrict_id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
#     subdistrict_name = db.Column(db.String(30))
#     regencys_id = db.Column(db.String(36), db.ForeignKey('regencys_list.regency_id'), nullable=False)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow())

# class Pivot_postal_code_location(db.Model):
#     postel_code_location = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
#     postal_code = db.column(db.String(36), db.ForeignKey('postal_code_address.postal_code'))
#     provinces_id = db.Column(db.String(36), db.ForeignKey('provinces_list.province_id'), nullable=False)
#     districts_id = db.Column(db.String(36), db.ForeignKey('regencys_list.regency_id'), nullable=False)
#     subdistricts_id = db.Column(db.String(36), db.ForeignKey('subdistricts_list.subdistrict_id'), nullable=False)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow())