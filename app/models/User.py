from flask_login import UserMixin
from datetime import datetime
from app import db
import uuid
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Users(db.Model, UserMixin, Base):
    __tablename__ = 'users'

    user_id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    username = db.Column(db.String(30), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(30))
    is_deleted = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())

    owner_profile = relationship("Owner_profile", backref='users', lazy=True)
    user_history = relationship("Users_history", backref='users', lazy=True)

    def get_id(self):
        return str(self.user_id)


class Owner_profile(db.Model, Base):
    __tablename__ = 'owner_profile'

    profile_id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.user_id'), nullable=False)
    postal_code = db.Column(db.String(36), db.ForeignKey('postal_code_address.postal_code'), nullable=False)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    birth_date = db.Column(db.Date)
    telephone_number = db.Column(db.String(15))
    address = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())

    def get_id(self):
        return str(self.profile_id)


class Users_history(db.Model, Base):
    __tablename__ = 'users_history'

    user_history_id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.user_id'), nullable=False)
    description = db.Column(db.Text)
    history_date = db.Column(db.DateTime, default=datetime.utcnow())
    created_at = db.Column(db.DateTime, default=datetime.utcnow())

    def get_id(self):
        return str(self.user_history_id)


##### MONEY BOOKKEEPING #####

class Bookkeeping_account(db.Model, Base):
    __tablename__ = 'bookkeeping_account'

    bookkeeping_account_id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    bookkeeping_ticket_id = db.Column(db.String(36), db.ForeignKey('bookkeeping_ticket.bookkeeping_ticket_id'))
    role_id = db.Column(db.String(50), db.ForeignKey('money_bookkeeping_role.role_id'))
    activity = db.Column(db.String(255))
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    name_account = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    deleted_at = db.Column(db.DateTime)

    activity_role = relationship("Activity_role", backref="bookkeeping_account", lazy=True)

    def get_id(self):
        return str(self.bookkeeping_account_id)


class Money_bookkeeping_role(db.Model, Base):
    __tablename__ = 'money_bookkeeping_role'

    role_id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    role_name = db.Column(db.String(25))
    role_status = db.Column(db.String(2))
    created_at = db.Column(db.DateTime, default=datetime.utcnow())

    bookkeeping_account = relationship("Bookkeeping_account", backref="money_bookkeeping_role", lazy=True)

    def get_id(self):
        return str(self.role_id)


class Activity_role(db.Model, Base):
    __tablename__ = 'activity_role'

    activity_id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    money_bookkeeping_account = db.Column(db.String(36), db.ForeignKey('bookkeeping_account.bookkeeping_account_id'))
    activity = db.Column(db.String(255))
    perubahan = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow())

    def get_id(self):
        return str(self.activity_id)


class Money_bookkeeping(db.Model, Base):
    __tablename__ = 'money_bookkeeping'

    money_bookkeeping_id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    bookkeeping_ticket = db.Column(db.String(36), db.ForeignKey('bookkeeping_ticket.bookkeeping_ticket_id'))
    transaction_type_id = db.Column(db.String(36), db.ForeignKey('transaction_type.transaction_type_id'))
    transaction_date = db.Column(db.DateTime, default=datetime.utcnow())
    description = db.Column(db.String(255))
    balances = db.Column(db.Integer)
    amount = db.Column(db.Integer)
    is_deleted = db.Column(db.Integer)

    bookkeeping_asets = relationship("Bookkeeping_asets", backref='money_bookkeeping', lazy=True)

    def get_id(self):
        return str(self.money_bookkeeping_id)


class Transaction_type(db.Model, Base):
    __tablename__ = 'transaction_type'

    transaction_type_id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    category_name = db.Column(db.String(36))
    created_at = db.Column(db.DateTime, default=datetime.utcnow())

    money_bookkeeping = relationship("Money_bookkeeping", backref='transaction_type', lazy=True)

    def get_id(self):
        return str(self.transaction_category_id)


class Bookkeeping_ticket(db.Model, Base):
    __tablename__ = 'bookkeeping_ticket'

    bookkeeping_ticket_id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow())

    bookkeeping_account = relationship("Bookkeeping_account", backref='tickets', lazy=True)
    money_bookkeeping = relationship("Money_bookkeeping", backref='ticket', lazy=True)

    def get_id(self):
        return str(self.bookkeeping_ticket_id)


class Bookkeeping_asets(db.Model, Base):
    __tablename__ = 'bookkeeping_asets'

    aset_id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    money_bookkeeping_id = db.Column(db.String(36), db.ForeignKey('money_bookkeeping.money_bookkeeping_id'),
                                     nullable=False)
    nama_barang = db.Column(db.String(36))
    harga = db.Column(db.Integer)
    tanggal_beli = db.Column(db.Date)
    kondisi_barang = db.Column(db.String(36))
    created_at = db.Column(db.DateTime, default=datetime.utcnow())

    def get_id(self):
        return str(self.aset_id)


# ##### POSTAL CODE #####

class Postal_code_address(db.Model, Base):
    __tablename__ = 'postal_code_address'

    postal_code = db.Column(db.String(36), primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())

    owner_profile = relationship("Owner_profile", backref="postal_code_address", lazy=True)

    def get_id(self):
        return str(self.postal_code)


class Provinces_list(db.Model, Base):
    __tablename__ = 'provinces_list'

    province_id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    province_name = db.Column(db.String(30))
    created_at = db.Column(db.DateTime, default=datetime.utcnow())

    regencys_list = relationship("Regencys_list", backref="provinces_list", lazy=True)
    pivot_postal_code_location = relationship("Pivot_postal_code_location", backref="provinces_list", lazy=True)

    def get_id(self):
        return str(self.province_id)


class Regencys_list(db.Model, Base):
    __tablename__ = 'regencys_list'

    regency_id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    regencys_name = db.Column(db.String(30))
    provincy_id = db.Column(db.String(36), db.ForeignKey('provinces_list.province_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())

    subdistricts_list = relationship("Subdistricts_list", backref="regencys_list", lazy=True)
    pivot_postal_code_location = relationship("Pivot_postal_code_location", backref="regencys_list", lazy=True)

    def get_id(self):
        return str(self.regency_id)


class Subdistricts_list(db.Model, Base):
    __tablename__ = 'subdistricts_list'

    subdistrict_id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    regency_id = db.Column(db.String(36), db.ForeignKey('regencys_list.regency_id'), nullable=False)
    subdistrict_name = db.Column(db.String(30))
    created_at = db.Column(db.DateTime, default=datetime.utcnow())

    pivot_postal_code_location = relationship("Pivot_postal_code_location", backref="subdistricts_list", lazy=True)

    def get_id(self):
        return str(self.subdistrict_id)


class Pivot_postal_code_location(db.Model, Base):
    __tablename__ = 'pivot_postal_code_location'

    pivot_postal_code_location = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    postal_code = db.Column(db.String(36), db.ForeignKey('postal_code_address.postal_code'))
    provinces_id = db.Column(db.String(36), db.ForeignKey('provinces_list.province_id'), nullable=False)
    regency_id = db.Column(db.String(36), db.ForeignKey('regencys_list.regency_id'), nullable=False)
    subdistricts_id = db.Column(db.String(36), db.ForeignKey('subdistricts_list.subdistrict_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())

    def get_id(self):
        return str(self.postel_code_location)


##### BUSSINESS PLAN #####

class Bussiness_plan(db.Model, Base):
    __tablename__ = 'bussiness_plan'

    bussiness_plan_id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    # bussiness_email = db.Column(db.String(100), unique=True)
    bussiness_type = db.Column(db.String(50))
    # postal_code = db.Column(db.String(36))
    bussiness_location = db.Column(db.String(100))
    # geolocation = db.Column(db.String(40))
    budgets = db.Column(db.String(100))
    ai_message = db.Column(db.Text)
    # target_market = db.Column(db.String(100))
    # status = db.Column(db.String(50))
    is_deleted = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())

    pivot_bussiness_bookkeeping = relationship("Pivot_bussiness_bookkeeping", backref='bussiness_plan', lazy=True)

    def get_id(self):
        return str(self.bussiness_plan_id)


class Pivot_bussiness_bookkeeping(db.Model, Base):
    __tablename__ = 'pivot_bussiness_bookkeeping'

    pivot_bussiness_bookkeeping = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    bussiness_plan_id = db.Column(db.String(36), db.ForeignKey('bussiness_plan.bussiness_plan_id'))
    bookkeeping_account_id = db.Column(db.String(36), db.ForeignKey('bookkeeping_account.bookkeeping_account_id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow())

    def get_id(self):
        return str(self.pivot_bussiness_bookkeeping)


class Pivot_bussiness_plan_location(db.Model, Base):
    __tablename__ = 'pivot_bussiness_plan_location'

    pivot_bussiness_plan_location_id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    bussiness_plan_id = db.Column(db.String(36), db.ForeignKey('bussiness_plan.bussiness_plan_id'))
    pivot_postal_code_location_id = db.Column(db.String(36),
                                              db.ForeignKey('pivot_postal_code_location.pivot_postal_code_location'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow())

    def get_id(self):
        return str(self.pivot_bussiness_plan_location_id)


class Pivot_bussiness_plan_account(db.Model, Base):
    __tablename__ = 'pivot_bussiness_plan_account'

    pivot_bussiness_plan_account_id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    bussiness_plan_id = db.Column(db.String(36), db.ForeignKey('bussiness_plan.bussiness_plan_id'))
    user_id = db.Column(db.String(36), db.ForeignKey('users.user_id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow())

    def get_id(self):
        return str(self.pivot_bussiness_plan_account_id)
