import uuid
from datetime import datetime
from flask import Flask, session, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from app import db

from app.models.User import *

class PemasukanResource(Resource):
    def get(self, bk_acc_id):
        bks = Money_bookkeeping.query.filter_by(deleted_at=None, bookkeeping_account_id=bk_acc_id)
        type = Transaction_type.query.filter_by(category_name="pemasukan").first()
        result = []
        for bk in bks:
            if bks.transaction_type_id == type.transaction_type_id:
                result.append({
                    "money_bookkeeping_id":bk.money_bookkeeping_id,
                    "bookkeeping_ticket_id":bk.bookkeeping_ticket_id,
                    "bookkeeping_account_id":bk.bookkeeping_account_id,
                    "nama_barang":bk.description,
                    "balances":bk.balances,
                    "amount":bk.amount,
                    "created_at":bk.created_at
                })
        return (result)
    
    @jwt_required()
    def post(self, bk_acc_id):
        user_id = get_jwt_identity()
        tipe_transaksi = Transaction_type.query.filter_by(category_name="pemasukan").first()
        tipe_pemasukan = tipe_transaksi.transaction_type_id
        ticket = Bookkeeping_ticket.query.filter_by(user_id=user_id, bookkeeping_account_id=bk_acc_id, deleted_at=None).first()
        
        ####################################################################
        pemasukan = request.json.get('pemasukan', None)
        balances = request.json.get('balances', None)
        amount = request.json.get('amount', None)
        ####################################################################

        value = Money_bookkeeping(
            bookkeeping_account_id=bk_acc_id,
            bookkeeping_ticket_id=ticket.bookkeeping_ticket_id,
            transaction_type_id=tipe_pemasukan,
            description=pemasukan,
            balances=balances,
            amount=amount,
            deleted_at=None
        )

        db.session.add(value)
        db.session.commit()

        return jsonify({
                "money_bookkeeping_id": value.money_bookkeeping_id,
                "bookkeeping_ticket_id": value.bookkeeping_ticket_id,
                "bookkeeping_account_id": value.bookkeeping_account_id,
                "transaction_type_id": value.transaction_type_id,
                "pemasukan": value.description,
                "balances": value.balances,
                "amount": value.amount,
                "created_at": value.created_at
        })


class TransactionTypeResource(Resource):

    def get(self):
        role = Transaction_type.query.all()

        result = []
        for a in role:
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
    def get(self):
        return 0