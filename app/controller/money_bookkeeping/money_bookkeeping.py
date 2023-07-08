import uuid
from datetime import datetime
from flask_login import current_user, login_required
from flask import Flask, session, jsonify, request
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from app import db

from app.models.User import *

class PemasukanResource(Resource):
    def get(self):
        bks = Money_bookkeeping.query.all()
        result = []
        for bk in bks:
            result.append({
                "money_bookkeeping_id" : bk.money_bookkeeping_id,
                "bookkeeping_ticket" : bk.bookkeeping_ticket,
                "transaction_type_id" : bk.bookkeeping_ticket,
                "transaction_date" : bk.transaction_date,
                "description" : bk.description,
                "balances" : bk.balances,
                "amount" : bk.amount,
                "is_deleted" : bk.is_deleted
            })
        return (result)
    
    def post(self):
        tipe_transaksi = Transaction_type.query.filter_by(category_name="pemasukan").first()

        ####################################################################
        pemasukan = request.json.get('pemasukan', None)
        balances = request.json.get('balances', None)
        amount = request.json.get('amount', None)
        ####################################################################

        value = Money_bookkeeping(
            transaction_type_id=tipe_transaksi.transaction_type.id,
            description=pemasukan,
            balances=balances,
            amount=amount
        )

        db.session.add(value)
        db.session.commit()

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
        category_name = request.json.get('category_name', None)

        db.session.add(Transaction_type(category_name=category_name))
        db.session.commit()

        return jsonify(message='success added')

class BookkeepingAsetsResource(Resource):
    def get(self):
        return 0