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

class Asets(Resource):
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