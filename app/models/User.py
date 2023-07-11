from flask_login import UserMixin
from datetime import datetime
from app import db
import uuid
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import pytz

Base = declarative_base()


class Users(db.Model, UserMixin, Base):
    __tablename__ = 'users'

    user_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(36), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(36))
    is_deleted = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.now(pytz.timezone('Asia/Jakarta')))

    # bookkeeping_account = relationship("Bookkeeping_account", backref='users', lazy=True)
    owner_profile = relationship("Owner_profile", backref='users', lazy=True)
    bussiness_plan = relationship("Bussiness_plan", backref="users", lazy=True)
    Bookkeeping_ticket = relationship("Bookkeeping_ticket", backref="users", lazy=True)

    def get_id(self):
        return str(self.user_id)


class Owner_profile(db.Model):
    __tablename__ = 'owner_profile'

    profile_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.user_id'), nullable=False)
    postal_code = db.Column(db.String(36))
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    birth_date = db.Column(db.Date)
    telephone_number = db.Column(db.String(16))
    address = db.Column(db.Text)
    is_deleted = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.now(pytz.timezone('Asia/Jakarta')))

    def get_id(self):
        return str(self.profile_id)


##### MONEY BOOKKEEPING #####

class Bookkeeping_account(db.Model, Base):
    __tablename__ = 'bookkeeping_account'

    bookkeeping_account_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name_account = db.Column(db.String(72))
    bussiness_email = db.Column(db.String(120))
    bussiness_location = db.Column(db.String(120))
    postal_code = db.Column(db.String(12))
    created_at = db.Column(db.DateTime, default=datetime.now(pytz.timezone('Asia/Jakarta')))
    is_deleted = db.Column(db.Integer)

    bookkeeping_activity = relationship("Bookkeeping_activity", backref='bookkeeping_account', lazy=True)
    bookkeeping_asets = relationship("Asets_activity", backref='Bookkeeping_account', lazy=True)
    money_bookkeeping = relationship("Money_bookkeeping", backref='Bookkeeping_account', lazy=True)

    def get_id(self):
        return str(self.bookkeeping_account_id)


class Money_bookkeeping_role(db.Model, Base):
    __tablename__ = 'money_bookkeeping_role'

    role_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    role_name = db.Column(db.String(36))

    bookkeeping_ticket = relationship("Bookkeeping_ticket", backref="Money_bookkeeping_role", lazy=True)

    def get_id(self):
        return str(self.role_id)


class Money_bookkeeping(db.Model, Base):
    __tablename__ = 'money_bookkeeping'

    money_bookkeeping_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    bookkeeping_ticket_id = db.Column(db.String(36), db.ForeignKey('bookkeeping_ticket.bookkeeping_ticket_id'))
    bookkeeping_account_id = db.Column(db.String(36), db.ForeignKey('bookkeeping_account.bookkeeping_account_id'))
    transaction_type_id = db.Column(db.String(36), db.ForeignKey('transaction_type.transaction_type_id'))
    description = db.Column(db.String(255))
    balances = db.Column(db.Integer) ##################################################################################### harga satuan
    amount = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.now(pytz.timezone('Asia/Jakarta')))
    is_deleted = db.Column(db.Integer)

    bookkeeping_activity = relationship("Bookkeeping_activity", backref='money_bookkeeping', lazy=True)

    def get_id(self):
        return str(self.money_bookkeeping_id)


class Transaction_type(db.Model, Base):
    __tablename__ = 'transaction_type'

    transaction_type_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    category_name = db.Column(db.String(36))

    bookkeeping_activity = relationship("Bookkeeping_activity", backref='transaction_type', lazy=True)
    money_bookkeeping = relationship("Money_bookkeeping", backref='transaction_type', lazy=True)

    def get_id(self):
        return str(self.transaction_type_id)


class Bookkeeping_ticket(db.Model):
    __tablename__ = 'bookkeeping_ticket'

    bookkeeping_ticket_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.user_id'))
    role_id = db.Column(db.String(36), db.ForeignKey('money_bookkeeping_role.role_id'))
    bookkeeping_account_id = db.Column(db.String(36), db.ForeignKey('bookkeeping_account.bookkeeping_account_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(pytz.timezone('Asia/Jakarta')))
    is_deleted = db.Column(db.Integer)

    landing_status = db.Column(db.Integer)

    bookkeeping_activity = relationship("Bookkeeping_activity", backref='bookkeeping_ticket', lazy=True)
    bookkeeping_account = relationship("Bookkeeping_account", backref='Bookkeeping_ticket', lazy=True)
    money_bookkeeping = relationship("Money_bookkeeping", backref='bookkeeping_ticket', lazy=True)

    def get_id(self):
        return str(self.bookkeeping_ticket_id)
    

class Bookkeeping_asets(db.Model, Base):
    __tablename__ = 'bookkeeping_asets'

    aset_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    bookkeeping_account_id = db.Column(db.String(36), db.ForeignKey('bookkeeping_account.bookkeeping_account_id'), nullable=False)
    nama_barang = db.Column(db.String(36))
    harga_barang = db.Column(db.Integer)
    tanggal_beli = db.Column(db.Date)
    barang_baik = db.Column(db.Integer)
    barang_buruk = db.Column(db.Integer)
    is_deleted = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.now(pytz.timezone('Asia/Jakarta')))

    asets_activity = relationship("Asets_activity", backref='bookkeeping_asets', lazy=True)

    def get_id(self):
        return str(self.aset_id)
    
class Asets_activity(db.Model):
    __tablename__ = "aset_activity"

    asets_activity_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    aset_id = db.Column(db.String(36), db.ForeignKey('bookkeeping_asets.aset_id'), nullable=False)
    bookkeeping_account_id = db.Column(db.String(36), db.ForeignKey('bookkeeping_account.bookkeeping_account_id'), nullable=False)
    nama_barang = db.Column(db.String(36))
    harga_barang = db.Column(db.Integer)
    tanggal_beli = db.Column(db.Date)
    barang_baik = db.Column(db.Integer)
    barang_buruk = db.Column(db.Integer)
    is_deleted = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.now(pytz.timezone('Asia/Jakarta')))

    def get_id(self):
        return str(self.asets_activity_id)

class Bussiness_plan(db.Model):
    __tablename__ = 'bussiness_plan'

    bussiness_plan_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.user_id'))
    bussiness_name = db.Column(db.String(72))
    bussiness_email = db.Column(db.String(100))
    bussiness_type = db.Column(db.String(72))
    postal_code = db.Column(db.String(36))
    bussiness_location = db.Column(db.String(120))
    budgets = db.Column(db.String(120))
    ai_message = db.Column(db.Text)
    target_market = db.Column(db.String(120))
    status = db.Column(db.Integer)
    is_deleted = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.now(pytz.timezone('Asia/Jakarta')))

    # pivot_bussiness_bookkeeping = relationship("pivot_bussiness_bookkeeping", backref='bussiness_plan', lazy=True)

    def get_id(self):
        return str(self.bussiness_plan_id)
    
class Bookkeeping_activity(db.Model):
    __tabblename__ = "bookkeeping_activity"

    bookkeeping_activity_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    money_bookkeeping_id = db.Column(db.String(36), db.ForeignKey('money_bookkeeping.money_bookkeeping_id'))
    bookkeeping_ticket_id = db.Column(db.String(36), db.ForeignKey('bookkeeping_ticket.bookkeeping_ticket_id'))
    bookkeeping_account_id = db.Column(db.String(36), db.ForeignKey('bookkeeping_account.bookkeeping_account_id'))
    transaction_type_id = db.Column(db.String(36), db.ForeignKey('transaction_type.transaction_type_id'))
    description = db.Column(db.String(255))
    balances = db.Column(db.Integer) #####################################################################################satuan
    amount = db.Column(db.Integer)
    is_deleted = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.now(pytz.timezone('Asia/Jakarta')))

    def get_id(self):
        return str(self.bookkeeping_activity_id)
    


# ##### POSTAL CODE #####

# class Postal_code_address(db.Model, Base):
#     __tablename__ = 'postal_code_address'

#     postal_code = db.Column(db.String(36), primary_key=True)
#     created_at = db.Column(db.DateTime, default=datetime.now(pytz.timezone('Asia/Jakarta')))

#     # owner_profile = relationship("Owner_profile", backref="postal_code_address", lazy=True)

#     def get_id(self):
#         return str(self.postal_code)


# class Provinces_list(db.Model, Base):
#     __tablename__ = 'provinces_list'

#     province_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
#     province_name = db.Column(db.String(30))
#     created_at = db.Column(db.DateTime, default=datetime.now(pytz.timezone('Asia/Jakarta')))

#     regencys_list = relationship("Regencys_list", backref="provinces_list", lazy=True)
#     pivot_postal_code_location = relationship("Pivot_postal_code_location", backref="provinces_list", lazy=True)

#     def get_id(self):
#         return str(self.province_id)


# class Regencys_list(db.Model, Base):
#     __tablename__ = 'regencys_list'

#     regency_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
#     regencys_name = db.Column(db.String(30))
#     provincy_id = db.Column(db.String(36), db.ForeignKey('provinces_list.province_id'), nullable=False)
#     created_at = db.Column(db.DateTime, default=datetime.now(pytz.timezone('Asia/Jakarta')))

#     subdistricts_list = relationship("Subdistricts_list", backref="regencys_list", lazy=True)
#     pivot_postal_code_location = relationship("Pivot_postal_code_location", backref="regencys_list", lazy=True)

#     def get_id(self):
#         return str(self.regency_id)


# class Subdistricts_list(db.Model, Base):
#     __tablename__ = 'subdistricts_list'

#     subdistrict_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
#     regency_id = db.Column(db.String(36), db.ForeignKey('regencys_list.regency_id'), nullable=False)
#     subdistrict_name = db.Column(db.String(30))
#     created_at = db.Column(db.DateTime, default=datetime.now(pytz.timezone('Asia/Jakarta')))

#     pivot_postal_code_location = relationship("Pivot_postal_code_location", backref="subdistricts_list", lazy=True)

#     def get_id(self):
#         return str(self.subdistrict_id)


# class Pivot_postal_code_location(db.Model, Base):
#     __tablename__ = 'pivot_postal_code_location'

#     pivot_postal_code_location = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
#     postal_code = db.Column(db.String(36), db.ForeignKey('postal_code_address.postal_code'))
#     provinces_id = db.Column(db.String(36), db.ForeignKey('provinces_list.province_id'), nullable=False)
#     regency_id = db.Column(db.String(36), db.ForeignKey('regencys_list.regency_id'), nullable=False)
#     subdistricts_id = db.Column(db.String(36), db.ForeignKey('subdistricts_list.subdistrict_id'), nullable=False)
#     created_at = db.Column(db.DateTime, default=datetime.now(pytz.timezone('Asia/Jakarta')))

#     def get_id(self):
#         return str(self.postel_code_location)


##### BUSSINESS PLAN #####



# class Pivot_bussiness_bookkeeping(db.Model, Base):
#     __tablename__ = 'pivot_bussiness_bookkeeping'

#     pivot_bussiness_bookkeeping_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
#     bussiness_plan_id = db.Column(db.String(36), db.ForeignKey('bussiness_plan.bussiness_plan_id'))
#     bookkeeping_account_id = db.Column(db.String(36), db.ForeignKey('bookkeeping_account.bookkeeping_account_id'))
#     created_at = db.Column(db.DateTime, default=datetime.now(pytz.timezone('Asia/Jakarta')))

#     def get_id(self):
#         return str(self.pivot_bussiness_bookkeeping)


# class Pivot_bussiness_plan_location(db.Model, Base):
#     __tablename__ = 'pivot_bussiness_plan_location'

#     pivot_bussiness_plan_location_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
#     bussiness_plan_id = db.Column(db.String(36), db.ForeignKey('bussiness_plan.bussiness_plan_id'))
#     pivot_postal_code_location_id = db.Column(db.String(36),db.ForeignKey('pivot_postal_code_location.pivot_postal_code_location'))
#     created_at = db.Column(db.DateTime, default=datetime.now(pytz.timezone('Asia/Jakarta')))

#     def get_id(self):
#         return str(self.pivot_bussiness_plan_location_id)


# class Pivot_bussiness_plan_account(db.Model, Base):
#     __tablename__ = 'pivot_bussiness_plan_account'

#     pivot_bussiness_plan_account_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
#     bussiness_plan_id = db.Column(db.String(36), db.ForeignKey('bussiness_plan.bussiness_plan_id'))
#     user_id = db.Column(db.String(36), db.ForeignKey('users.user_id'))
#     created_at = db.Column(db.DateTime, default=datetime.now(pytz.timezone('Asia/Jakarta')))

#     def get_id(self):
#         return str(self.pivot_bussiness_plan_account_id)
