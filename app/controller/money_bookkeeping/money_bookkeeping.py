import uuid
from datetime import datetime
import pytz
from flask import Flask, session, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from app import db
from app.controller.object.object import *

from app.models.User import *

class PemasukanResource(Resource): # MASUK # MASUK # MASUK # MASUK # MASUK # MASUK # MASUK # MASUK #
    def get(self, bk_acc_id):
        bks = Money_bookkeeping.query.filter_by(is_deleted=0, bookkeeping_account_id=bk_acc_id)
        result = []
        for bk in bks:
            if bk.transaction_type_id == Query.TransactionTypeId('pemasukan'):
                result.append({
                    "money_bookkeeping_id":bk.money_bookkeeping_id,
                    "bookkeeping_ticket_id":bk.bookkeeping_ticket_id,
                    "bookkeeping_account_id":bk.bookkeeping_account_id,
                    "nama_pemasukan":bk.description,
                    "balances":bk.balances,
                    "amount":bk.amount,
                    "created_at":bk.created_at
                })
        return jsonify(data=result)
    

    def post(self, bk_acc_id):
        
        ####################################################################
        pemasukan = request.json.get('pemasukan', None)
        balances = request.json.get('balances', None)
        amount = request.json.get('amount', None)
        ####################################################################

        value = Money_bookkeeping(
            bookkeeping_account_id=bk_acc_id,
            bookkeeping_ticket_id=Access.Ticket(bk_acc_id),
            transaction_type_id=Query.TransactionTypeId("pemasukan"),
            description=pemasukan,
            balances=balances,
            amount=amount,
            is_deleted=0
        )

        db.session.add(value)
        db.session.commit()

        value2 = Bookkeeping_activity(
            money_bookkeeping_id=value.money_bookkeeping_id,
            bookkeeping_account_id=value.bookkeeping_account_id,
            bookkeeping_ticket_id=value.bookkeeping_ticket_id,
            transaction_type_id=value.transaction_type_id,
            description=value.description,
            balances=value.balances,
            amount=value.amount,
            is_deleted=value.is_deleted
        )
        db.session.add(value2)
        db.session.commit()

        return jsonify({
                "money_bookkeeping_id": value.money_bookkeeping_id,
                "bookkeeping_ticket_id": value.bookkeeping_ticket_id,
                "bookkeeping_account_id": value.bookkeeping_account_id,
                "transaction_type_id": value.transaction_type_id,
                "nama_pemasukan": value.description,
                "balances": value.balances,
                "amount": value.amount,
                "created_at": value.created_at
        })
    
    def put(self, bk_acc_id): ########################### ini isinya bukan bookkeeping account, tapi money bookkeeping id
        value = Money_bookkeeping.query.filter_by(money_bookkeeping_id=bk_acc_id).first()

        pemasukan = request.json.get('pemasukan', value.description)
        balances = request.json.get('balances', value.balances)
        amount = request.json.get('amount', value.amount)

        value.description = pemasukan
        value.balances = balances
        value.amount = amount
        value.bookkeeping_ticket_id = Access.Ticket(value.bookkeeping_account_id)

        db.session.commit()

        value2 = Bookkeeping_activity(
            money_bookkeeping_id=value.money_bookkeeping_id,
            bookkeeping_account_id=value.bookkeeping_account_id,
            bookkeeping_ticket_id=Access.Ticket(value.bookkeeping_account_id),
            transaction_type_id=value.transaction_type_id,
            description=value.description,
            balances=value.balances,
            amount=value.amount,
            is_deleted=value.is_deleted
        )

        db.session.add(value2)
        db.session.commit()

        return jsonify({
                "money_bookkeeping_id": value.money_bookkeeping_id,
                "bookkeeping_ticket_id": value.bookkeeping_ticket_id,
                "bookkeeping_account_id": value.bookkeeping_account_id,
                "transaction_type_id": value.transaction_type_id,
                "nama_pemasukan": value.description,
                "balances": value.balances,
                "amount": value.amount,
                "created_at": value.created_at
        })
    
    def delete(self, bk_acc_id): ########################### ini isinya bukan bookkeeping account, tapi money bookkeeping id
        value = Money_bookkeeping.query.filter_by(money_bookkeeping_id=bk_acc_id).first()

        value.is_deleted =1
        db.session.commit()
        
        value2 = Bookkeeping_activity(
            money_bookkeeping_id=value.money_bookkeeping_id,
            bookkeeping_account_id=value.bookkeeping_account_id,
            bookkeeping_ticket_id=Access.Ticket(value.bookkeeping_account_id),
            transaction_type_id=value.transaction_type_id,
            description=value.description,
            balances=value.balances,
            amount=value.amount,
            is_deleted=value.is_deleted
        )

        db.session.add(value2)
        db.session.commit()

        return jsonify(message=f"{value.description} berhasil dihapus")


class PengeluaranResource(Resource): # KELUAR # KELUAR # KELUAR # KELUAR # KELUAR # KELUAR # KELUAR # KELUAR #
    def get(self, bk_acc_id):
        bks = Money_bookkeeping.query.filter_by(is_deleted=0, bookkeeping_account_id=bk_acc_id)
        result = []
        for bk in bks:
            if bk.transaction_type_id == Query.TransactionTypeId('pengeluaran'):
                result.append({
                    "money_bookkeeping_id":bk.money_bookkeeping_id,
                    "bookkeeping_ticket_id":bk.bookkeeping_ticket_id,
                    "bookkeeping_account_id":bk.bookkeeping_account_id,
                    "nama_pengeluaran":bk.description,
                    "balances":bk.balances,
                    "amount":bk.amount,
                    "created_at":bk.created_at
                })
        return jsonify(data=result)
    

    def post(self, bk_acc_id):
        
        ####################################################################
        pengeluaran = request.json.get('pengeluaran', None)
        balances = request.json.get('balances', None)
        amount = request.json.get('amount', None)
        ####################################################################

        value = Money_bookkeeping(
            bookkeeping_account_id=bk_acc_id,
            bookkeeping_ticket_id=Access.Ticket(bk_acc_id),
            transaction_type_id=Query.TransactionTypeId("pengeluaran"),
            description=pengeluaran,
            balances=balances,
            amount=amount,
            is_deleted=0
        )

        db.session.add(value)
        db.session.commit()

        value2 = Bookkeeping_activity(
            money_bookkeeping_id=value.money_bookkeeping_id,
            bookkeeping_account_id=value.bookkeeping_account_id,
            bookkeeping_ticket_id=value.bookkeeping_ticket_id,
            transaction_type_id=value.transaction_type_id,
            description=value.description,
            balances=value.balances,
            amount=value.amount,
            is_deleted=value.is_deleted
        )
        db.session.add(value2)
        db.session.commit()

        return jsonify({
                "money_bookkeeping_id": value.money_bookkeeping_id,
                "bookkeeping_ticket_id": value.bookkeeping_ticket_id,
                "bookkeeping_account_id": value.bookkeeping_account_id,
                "transaction_type_id": value.transaction_type_id,
                "nama_pengeluaran": value.description,
                "balances": value.balances,
                "amount": value.amount,
                "created_at": value.created_at
        })
    
    def put(self, bk_acc_id): ########################### ini isinya bukan bookkeeping account, tapi money bookkeeping id
        value = Money_bookkeeping.query.filter_by(money_bookkeeping_id=bk_acc_id).first()

        pengeluaran = request.json.get('pengeluaran', value.description)
        balances = request.json.get('balances', value.balances)
        amount = request.json.get('amount', value.amount)

        value.description = pengeluaran
        value.balances = balances
        value.amount = amount
        value.bookkeeping_ticket_id = Access.Ticket(value.bookkeeping_account_id)

        db.session.commit()

        value2 = Bookkeeping_activity(
            money_bookkeeping_id=value.money_bookkeeping_id,
            bookkeeping_account_id=value.bookkeeping_account_id,
            bookkeeping_ticket_id=Access.Ticket(value.bookkeeping_account_id),
            transaction_type_id=value.transaction_type_id,
            description=value.description,
            balances=value.balances,
            amount=value.amount,
            is_deleted=value.is_deleted
        )

        db.session.add(value2)
        db.session.commit()

        return jsonify({
                "money_bookkeeping_id": value.money_bookkeeping_id,
                "bookkeeping_ticket_id": value.bookkeeping_ticket_id,
                "bookkeeping_account_id": value.bookkeeping_account_id,
                "transaction_type_id": value.transaction_type_id,
                "nama_pengeluaran": value.description,
                "balances": value.balances,
                "amount": value.amount,
                "created_at": value.created_at
        })
    
    def delete(self, bk_acc_id): ########################### ini isinya bukan bookkeeping account, tapi money bookkeeping id
        value = Money_bookkeeping.query.filter_by(money_bookkeeping_id=bk_acc_id).first()

        value.is_deleted =1
        db.session.commit()
        
        value2 = Bookkeeping_activity(
            money_bookkeeping_id=value.money_bookkeeping_id,
            bookkeeping_account_id=value.bookkeeping_account_id,
            bookkeeping_ticket_id=Access.Ticket(value.bookkeeping_account_id),
            transaction_type_id=value.transaction_type_id,
            description=value.description,
            balances=value.balances,
            amount=value.amount,
            is_deleted=value.is_deleted
        )

        db.session.add(value2)
        db.session.commit()

        return jsonify(message=f"{value.description} berhasil dihapus")
    

class UtangResource(Resource): # UTANG # UTANG # UTANG # UTANG # UTANG # UTANG # UTANG # UTANG # UTANG #
    def get(self, bk_acc_id):
        bks = Money_bookkeeping.query.filter_by(is_deleted=0, bookkeeping_account_id=bk_acc_id)
        result = []
        for bk in bks:
            if bk.transaction_type_id == Query.TransactionTypeId('utang'):
                result.append({
                    "money_bookkeeping_id":bk.money_bookkeeping_id,
                    "bookkeeping_ticket_id":bk.bookkeeping_ticket_id,
                    "bookkeeping_account_id":bk.bookkeeping_account_id,
                    "nama_pemberi_utang":bk.description,
                    "balances":bk.balances,
                    "periode_utang":bk.amount,
                    "created_at":bk.created_at
                })
        return jsonify(data=result)
    

    def post(self, bk_acc_id):
        
        ####################################################################
        utang = request.json.get('utang', None)
        balances = request.json.get('balances', None)
        periode_utang = request.json.get('periode_utang', None)
        ####################################################################

        value = Money_bookkeeping(
            bookkeeping_account_id=bk_acc_id,
            bookkeeping_ticket_id=Access.Ticket(bk_acc_id),
            transaction_type_id=Query.TransactionTypeId("utang"),
            description=utang,
            balances=balances,
            amount=periode_utang,
            is_deleted=0
        )

        db.session.add(value)
        db.session.commit()

        value2 = Bookkeeping_activity(
            money_bookkeeping_id=value.money_bookkeeping_id,
            bookkeeping_account_id=value.bookkeeping_account_id,
            bookkeeping_ticket_id=value.bookkeeping_ticket_id,
            transaction_type_id=value.transaction_type_id,
            description=value.description,
            balances=value.balances,
            amount=value.amount,
            is_deleted=value.is_deleted
        )
        db.session.add(value2)
        db.session.commit()

        return jsonify({
                "money_bookkeeping_id": value.money_bookkeeping_id,
                "bookkeeping_ticket_id": value.bookkeeping_ticket_id,
                "bookkeeping_account_id": value.bookkeeping_account_id,
                "transaction_type_id": value.transaction_type_id,
                "nama_pemberi_utang": value.description,
                "balances": value.balances,
                "periode_utang": value.amount,
                "created_at": value.created_at
        })
    
    def put(self, bk_acc_id): ########################### ini isinya bukan bookkeeping account, tapi money bookkeeping id
        value = Money_bookkeeping.query.filter_by(money_bookkeeping_id=bk_acc_id).first()

        utang = request.json.get('utang', value.description)
        balances = request.json.get('balances', value.balances)
        amount = request.json.get('amount', value.amount)

        value.description = utang
        value.balances = balances
        value.amount = amount
        value.bookkeeping_ticket_id = Access.Ticket(value.bookkeeping_account_id)

        db.session.commit()

        value2 = Bookkeeping_activity(
            money_bookkeeping_id=value.money_bookkeeping_id,
            bookkeeping_account_id=value.bookkeeping_account_id,
            bookkeeping_ticket_id=Access.Ticket(value.bookkeeping_account_id),
            transaction_type_id=value.transaction_type_id,
            description=value.description,
            balances=value.balances,
            amount=value.amount,
            is_deleted=value.is_deleted
        )

        db.session.add(value2)
        db.session.commit()

        return jsonify({
                "money_bookkeeping_id": value.money_bookkeeping_id,
                "bookkeeping_ticket_id": value.bookkeeping_ticket_id,
                "bookkeeping_account_id": value.bookkeeping_account_id,
                "transaction_type_id": value.transaction_type_id,
                "nama_pemberi_utang": value.description,
                "balances": value.balances,
                "periode_utang": value.amount,
                "created_at": value.created_at
        })
    
    def delete(self, bk_acc_id): ########################### ini isinya bukan bookkeeping account, tapi money bookkeeping id
        value = Money_bookkeeping.query.filter_by(money_bookkeeping_id=bk_acc_id).first()

        value.is_deleted =1
        db.session.commit()
        
        value2 = Bookkeeping_activity(
            money_bookkeeping_id=value.money_bookkeeping_id,
            bookkeeping_account_id=value.bookkeeping_account_id,
            bookkeeping_ticket_id=Access.Ticket(value.bookkeeping_account_id),
            transaction_type_id=value.transaction_type_id,
            description=value.description,
            balances=value.balances,
            amount=value.amount,
            is_deleted=value.is_deleted
        )

        db.session.add(value2)
        db.session.commit()

        return jsonify(message=f"Utang kepada {value.description} berhasil dihapus")
    

class PiutangResource(Resource): # PIUTANG # PIUTANG # PIUTANG # PIUTANG # PIUTANG # PIUTANG # PIUTANG #
    def get(self, bk_acc_id):
        bks = Money_bookkeeping.query.filter_by(is_deleted=0, bookkeeping_account_id=bk_acc_id)
        result = []
        for bk in bks:
            if bk.transaction_type_id == Query.TransactionTypeId('piutang'):
                result.append({
                    "money_bookkeeping_id":bk.money_bookkeeping_id,
                    "bookkeeping_ticket_id":bk.bookkeeping_ticket_id,
                    "bookkeeping_account_id":bk.bookkeeping_account_id,
                    "nama_pengutang":bk.description,
                    "balances":bk.balances,
                    "periode_piutang":bk.amount,
                    "created_at":bk.created_at
                })
        return jsonify(data=result)
    

    def post(self, bk_acc_id):
        
        ####################################################################
        piutang = request.json.get('piutang', None)
        balances = request.json.get('balances', None)
        periode_piutang = request.json.get('periode_piutang', None)
        ####################################################################

        value = Money_bookkeeping(
            bookkeeping_account_id=bk_acc_id,
            bookkeeping_ticket_id=Access.Ticket(bk_acc_id),
            transaction_type_id=Query.TransactionTypeId("piutang"),
            description=piutang,
            balances=balances,
            amount=periode_piutang,
            is_deleted=0
        )

        db.session.add(value)
        db.session.commit()

        value2 = Bookkeeping_activity(
            money_bookkeeping_id=value.money_bookkeeping_id,
            bookkeeping_account_id=value.bookkeeping_account_id,
            bookkeeping_ticket_id=value.bookkeeping_ticket_id,
            transaction_type_id=value.transaction_type_id,
            description=value.description,
            balances=value.balances,
            amount=value.amount,
            is_deleted=value.is_deleted
        )
        db.session.add(value2)
        db.session.commit()

        return jsonify({
                "money_bookkeeping_id": value.money_bookkeeping_id,
                "bookkeeping_ticket_id": value.bookkeeping_ticket_id,
                "bookkeeping_account_id": value.bookkeeping_account_id,
                "transaction_type_id": value.transaction_type_id,
                "nama_pengutang": value.description,
                "balances": value.balances,
                "periode_piutang": value.amount,
                "created_at": value.created_at
        })
    
    def put(self, bk_acc_id): ########################### ini isinya bukan bookkeeping account, tapi money bookkeeping id
        value = Money_bookkeeping.query.filter_by(money_bookkeeping_id=bk_acc_id).first()

        piutang = request.json.get('piutang', value.description)
        balances = request.json.get('balances', value.balances)
        amount = request.json.get('amount', value.amount)

        value.description = piutang
        value.balances = balances
        value.amount = amount
        value.bookkeeping_ticket_id = Access.Ticket(value.bookkeeping_account_id)

        db.session.commit()

        value2 = Bookkeeping_activity(
            money_bookkeeping_id=value.money_bookkeeping_id,
            bookkeeping_account_id=value.bookkeeping_account_id,
            bookkeeping_ticket_id=Access.Ticket(value.bookkeeping_account_id),
            transaction_type_id=value.transaction_type_id,
            description=value.description,
            balances=value.balances,
            amount=value.amount,
            is_deleted=value.is_deleted
        )

        db.session.add(value2)
        db.session.commit()

        return jsonify({
                "money_bookkeeping_id": value.money_bookkeeping_id,
                "bookkeeping_ticket_id": value.bookkeeping_ticket_id,
                "bookkeeping_account_id": value.bookkeeping_account_id,
                "transaction_type_id": value.transaction_type_id,
                "nama_piutang": value.description,
                "balances": value.balances,
                "periode_piutang": value.amount,
                "created_at": value.created_at
        })
    
    def delete(self, bk_acc_id): ########################### ini isinya bukan bookkeeping account, tapi money bookkeeping id
        value = Money_bookkeeping.query.filter_by(money_bookkeeping_id=bk_acc_id).first()

        value.is_deleted =1
        db.session.commit()
        
        value2 = Bookkeeping_activity(
            money_bookkeeping_id=value.money_bookkeeping_id,
            bookkeeping_account_id=value.bookkeeping_account_id,
            bookkeeping_ticket_id=Access.Ticket(value.bookkeeping_account_id),
            transaction_type_id=value.transaction_type_id,
            description=value.description,
            balances=value.balances,
            amount=value.amount,
            is_deleted=value.is_deleted
        )

        db.session.add(value2)
        db.session.commit()

        return jsonify(message=f"{value.description} berhasil dihapus")


class TransactionTypeResource(Resource):

    def get(self):
        result = []
        for a in Query.All(Transaction_type):
            result.append({
                "tipe":a.category_name
            })

        return (result)

    def post(self):
        ################################################################
        category_name = request.json.get('category_name', None)
        ################################################################

        db.session.add(Transaction_type(category_name=category_name))
        db.session.commit()

        return jsonify(message='success added')

class BookkeepingAsetsResource(Resource):
    def get(self, bk_acc_id):
        asets = Bookkeeping_asets.query.filter_by(bookkeeping_account_id=bk_acc_id).all()
        result = []
        for aset in asets:
            result.append({
                "aset_id": aset.aset_id,
                "bookkeeping_account_id": aset.bookkeeping_account_id,
                "nama_barang": aset.nama_barang,
                "harga_barang": aset.harga_barang,
                "tanggal_beli": aset.tanggal_beli,
                "barang_baik": aset.barang_baik,
                "barang_buruk": aset.barang_buruk,
                "is_deleted": aset.is_deleted,
                "created_at": aset.created_at
            })
 
        return jsonify(data=result)