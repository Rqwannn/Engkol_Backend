import uuid
from datetime import datetime
from flask_login import current_user, login_required
from flask import Flask, session, jsonify, request
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from app import db

from app.models.User import *

class PemasukanResource(Resource):
    def get(self, bk_acc_id):
        bks = Money_bookkeeping.query.filter_by(is_deleted=0, bookkeeping_account_id=bk_acc_id)
        type = Transaction_type.query.filter_by(category_name="pemasukan").first()
        result = []
        if bks.transaction_type_id == type.transaction_type_id:
            for bk in bks:
                result.append({
                    "money_bookkeeping_id" : bk.money_bookkeeping_id,
                    "bookkeeping_ticket" : bk.bookkeeping_ticket,
                    "transaction_date" : bk.transaction_date,
                    "description" : bk.description,
                    "balances" : bk.balances,
                    "amount" : bk.amount,
                })
            return (result)
    
    def post(self, bk_acc_id):
        tipe_transaksi = Transaction_type.query.filter_by(category_name="pemasukan").first()
        tipe_pemasukan = tipe_transaksi.trasactio_type_id

        ####################################################################
        pemasukan = request.json.get('pemasukan', None)
        balances = request.json.get('balances', None)
        amount = request.json.get('amount', None)
        ####################################################################

        value = Money_bookkeeping(
            bookkeeping_account_id=bk_acc_id,
            bookkeeping_ticket_id="",
            transaction_type_id=tipe_pemasukan,
            description=pemasukan,
            balances=balances,
            amount=amount,
            is_deleted=0
        )

        db.session.add(value)
        db.session.commit()

        return jsonify({
            "money_bookkeeping_id": value.money_bookkeeping_id,
            "bookkeeping_ticket": value.bookkeeping_ticket,
            "transaction_type_id": value.transaction_type_id,
            "transaction_date": value.transaction_date,
            "description": value.description,
            "balances": value.balances,
            "amount": value.amount,
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