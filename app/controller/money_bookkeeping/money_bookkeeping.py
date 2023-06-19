import uuid
from datetime import datetime
from flask_login import current_user, login_required
from flask import Flask, session
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from app import db

from app.models.User import *


class MoneyBookkkeepingResource(Resource):
    def get(self, money_bookkeeping_id):
        values = Money_bookkeeping.query.get(money_bookkeeping_id)
        if values:
            return {
                'data': values,
            }
        else:
            return {'message': 'bookkeeping not found'}, 404

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('bookkeeping_ticket', type=str, required=True)
        parser.add_argument('transaction_type_id', type=str, required=True)
        parser.add_argument('description', type=str, required=True)
        parser.add_argument('balances', type=str, required=True)
        parser.add_argument('amount', type=str, required=True)
        args = parser.parse_args()

        values = Money_bookkeeping(
            bookkeeping_ticket=args['bookkeeping_ticket'],
            transaction_type_id=args['transaction_type_id'],
            description=args['description'],
            balances=args['balances'],
            amount=args['amount'],
        )

        db.session.add(values)
        db.session.commit()

        return {'message': 'bookkeeping created successfully'}, 201

    def put(self, bookkeeping_id):
        parser = reqparse.RequestParser()
        parser.add_argument('bookkeeping_ticket', type=str, required=True)
        parser.add_argument('transaction_type_id', type=str, required=True)
        parser.add_argument('description', type=str, required=True)
        parser.add_argument('balances', type=str, required=True)
        parser.add_argument('amount', type=str, required=True)
        args = parser.parse_args()

        bookkeeping = Bookkeeping_account.query.get(money_bookkeeping_id)
        if bookkeeping:
            bookkeeping.bookkeeping_ticket = args['bookkeeping_ticket']
            bookkeeping.transaction_type_id = args['transaction_type_id']
            bookkeeping.description = args['description']
            bookkeeping.balances = args['balances']
            bookkeeping.amount = args['amount']
            db.session.commit()
            return {'message': 'bookkeeping updated successfully'}
        else:
            return {'message': 'bookkeeping not found'}, 404

    def delete(self, money_bookkeeping_id):
        values = Bookkeeping_account.query.get(Money_bookkeeping_id)
        if values:
            db.session.delete(values)
            db.session.commit()
            return {'message': 'data deleted successfully'}
        else:
            return {'message': 'data not found'}, 404

class BookkeepingAccountResource(Resource):
    def get(self, bookkeeping_account_id):
        bookkeeping = Bookkeeping_account.query.get(bookkeeping_account_id)
        if bookkeeping:
            return {
                'data': bookkeeping,
            }
        else:
            return {'message': 'bookkeeping not found'}, 404

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('bookkeeping_ticket_id', type=str, required=True)
        parser.add_argument('role_id', type=str, required=True)
        parser.add_argument('activity', type=str, required=True)
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        parser.add_argument('name_account', type=str, required=True)
        args = parser.parse_args()

        bookkeeping = Bookkeeping_account(
            bookkeeping_ticket_id=args['bookkeeping_ticket_id'],
            role_id=args['role_id'],
            activity=args['activity'],
            username=args['username'],
            password=args['password'],
            name_account=args['name_account']
        )

        db.session.add(bookkeeping)
        db.session.commit()

        return {'message': 'bookkeeping created successfully'}, 201

    def put(self, bookkeeping_id):
        parser = reqparse.RequestParser()
        parser.add_argument('bookkeeping_ticket_id', type=str, required=True)
        parser.add_argument('role_id', type=str, required=True)
        parser.add_argument('activity', type=str, required=True)
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        parser.add_argument('name_account', type=str, required=True)
        args = parser.parse_args()

        bookkeeping = Bookkeeping_account.query.get(bookkeeping_id)
        if bookkeeping:
            bookkeeping.bookkeeping_ticket_id = args['bookkeeping_ticket_id']
            bookkeeping.role_id = args['role_id']
            bookkeeping.activity = args['activity']
            bookkeeping.username = args['username']
            bookkeeping.password = args['password']
            bookkeeping.name_account = args['name_account']
            db.session.commit()
            return {'message': 'bookkeeping updated successfully'}
        else:
            return {'message': 'bookkeeping not found'}, 404

    def delete(self, bookkeeping_id):
        bookkeeping = Bookkeeping_account.query.get(bookkeeping_id)
        if bookkeeping:
            db.session.delete(bookkeeping)
            db.session.commit()
            return {'message': 'bookkeeping deleted successfully'}
        else:
            return {'message': 'bookkeeping not found'}, 404


class BookkeepingRoleResource(Resource):
    def get(self, bookkeeping_role_id):
        bookkeeping_role = Money_bookkeeping_role.query.get(bookkeeping_role_id)
        if bookkeeping_role:
            return {
                'data': bookkeeping_role,
            }
        else:
            return {'message': 'bookkeeping role not found'}, 404

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('role_name', type=str, required=True)
        parser.add_argument('role_status', type=str, required=True)
        args = parser.parse_args()

        print(current_user)

        bookkeeping_role = Money_bookkeeping_role(
            role_name=args['role_name'],
            role_status=args['role_status']
        )

        db.session.add(bookkeeping_role)
        db.session.commit()

        return {'message': 'bookkeeping role created successfully'}, 201

    def put(self, bookkeeping_role_id):
        parser = reqparse.RequestParser()
        parser.add_argument('role_name', type=str, required=True)
        parser.add_argument('role_status', type=str, required=True)
        args = parser.parse_args()

        bookkeeping_role = Money_bookkeeping_role.query.get(bookkeeping_role_id)
        if bookkeeping_role:
            bookkeeping_role.role_name = args['role_name']
            bookkeeping_role.role_status = args['role_status']
            db.session.commit()
            return {'message': 'bookkeeping role updated successfully'}
        else:
            return {'message': 'bookkeeping role not found'}, 404

    def delete(self, bookkeeping_role_id):
        bookkeeping_role = Money_bookkeeping_role.query.get(bookkeeping_role_id)
        if bookkeeping_role:
            db.session.delete(bookkeeping_role)
            db.session.commit()
            return {'message': 'bookkeeping role deleted successfully'}
        else:
            return {'message': 'bookkeeping role not found'}, 404


class TransactionTypeResource(Resource):
    def get(self, transaction_type_id):
        values = Transaction_type.query.get(transaction_type_id)
        if values:
            return {
                'data': values,
            }
        else:
            return {'message': 'data not found'}, 404

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('category_name', type=str, required=True)
        args = parser.parse_args()

        print(current_user)

        values = Transaction_type(
            category_name=args['category_name']
        )

        db.session.add(values)
        db.session.commit()

        return {'message': 'activity role created successfully'}, 201

    def put(self, transaction_type_id):
        parser = reqparse.RequestParser()
        parser.add_argument('category_name', type=str, required=True)
        args = parser.parse_args()

        values = Transaction_type.query.get(activity_role_id)
        if values:
            values.category_name = args['category_name']
            db.session.commit()
            return {'message': 'data updated successfully'}
        else:
            return {'message': 'data not found'}, 404

    def delete(self, transaction_type_id):
        values = Transaction_type.query.get(transaction_type_id)
        if values:
            db.session.delete(values)
            db.session.commit()
            return {'message': 'data deleted successfully'}
        else:
            return {'message': 'data not found'}, 404

class ActivityRoleResource(Resource):
    def get(self, activity_role_id):
        activity_role = Activity_role.query.get(activity_role_id)
        if activity_role:
            return {
                'data': activity_role,
            }
        else:
            return {'message': 'activity role not found'}, 404

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('money_bookkeeping_account', type=str, required=True)
        parser.add_argument('activity', type=str, required=True)
        parser.add_argument('perubahan', type=str, required=True)
        parser.add_argument('postal_code', type=str, required=True)
        parser.add_argument('address', type=str, required=True)
        args = parser.parse_args()

        print(current_user)

        activity_role = Activity_role(
            money_bookkeeping_account=args['money_bookkeeping_account'],
            activity=args['activity'],
            perubahan=args['perubahan'],
        )

        db.session.add(activity_role)
        db.session.commit()

        return {'message': 'activity role created successfully'}, 201

    def put(self, activity_role_id):
        parser = reqparse.RequestParser()
        parser.add_argument('money_bookkeeping_account', type=str, required=True)
        parser.add_argument('activity', type=str, required=True)
        parser.add_argument('perubahan', type=str, required=True)
        args = parser.parse_args()

        activity_role = Activity_role.query.get(activity_role_id)
        if activity_role:
            activity_role.money_bookkeeping_account = args['money_bookkeeping_account']
            activity_role.activity = args['activity']
            activity_role.perubahan = args['perubahan']
            db.session.commit()
            return {'message': 'activity role updated successfully'}
        else:
            return {'message': 'activity role not found'}, 404

    def delete(self, activity_role_id):
        activity_role = Activity_role.query.get(activity_role_id)
        if activity_role:
            db.session.delete(activity_role)
            db.session.commit()
            return {'message': 'activity role deleted successfully'}
        else:
            return {'message': 'activity role not found'}, 404


class BookkeepingAsetsResource(Resource):
    def get(self, aset_id):
        values = Bookkeeping_asets.query.get(aset_id)
        if values:
            return {
                'data': values,
            }
        else:
            return {'message': 'data not found'}, 404

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('money_bookkeeping_id', type=str, required=True)
        parser.add_argument('nama_barang', type=str, required=True)
        parser.add_argument('harga', type=str, required=True)
        parser.add_argument('tanggal_beli', type=str, required=True)
        parser.add_argument('kondisi_barang', type=str, required=True)
        args = parser.parse_args()

        print(current_user)

        values = Bookkeeping_asets(
            money_bookkeeping_id=args['money_bookkeeping_id'],
            nama_barang=args['nama_barang'],
            harga=args['harga'],
            tanggal_beli=datetime.strptime(args['tanggal_beli'], '%d-%m-%Y').date(),
            kondisi_barang=args['kondisi_barang']
        )

        db.session.add(values)
        db.session.commit()

        return {'message': 'data created successfully'}, 201

    def put(self, aset_id):
        parser = reqparse.RequestParser()
        parser.add_argument('money_bookkeeping_id', type=str, required=True)
        parser.add_argument('nama_barang', type=str, required=True)
        parser.add_argument('harga', type=str, required=True)
        parser.add_argument('tanggal_beli', type=str, required=True)
        parser.add_argument('kondisi_barang', type=str, required=True)
        args = parser.parse_args()

        values = Bookkeeping_asets.query.get(aset_id)
        if values:
            values.money_bookkeeping_id = args['money_bookkeeping_id']
            values.nama_barang = args['nama_barang']
            values.harga = args['harga']
            values.tanggal_beli = datetime.strptime(args['tanggal_beli'], '%d-%m-%Y').date(),
            values.kondisi_barang = args['kondisi_barang']
            db.session.commit()
            return {'message': 'data updated successfully'}
        else:
            return {'message': 'data not found'}, 404

    def delete(self, aset_id):
        values = Bookkeeping_asets.query.get(aset_id)
        if values:
            db.session.delete(values)
            db.session.commit()
            return {'message': 'data deleted successfully'}
        else:
            return {'message': 'data not found'}, 404


class PivotBussinessBookkeepingResource(Resource):
    def get(self, pivot_bussiness_bookkeeping_id):
        values = Pivot_bussiness_bookkeeping.query.get(pivot_bussiness_bookkeeping_id)
        if values:
            return {
                'data': values,
            }
        else:
            return {'message': 'data not found'}, 404

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('bussiness_plan_id', type=str, required=True)
        parser.add_argument('bookkeeping_account_id', type=str, required=True)
        args = parser.parse_args()

        print(current_user)

        values = Pivot_bussiness_bookkeeping(
            bussiness_plan_id=args['bussiness_plan_id'],
            bookkeeping_account_id=args['bookkeeping_account_id'],
        )

        db.session.add(values)
        db.session.commit()

        return {'message': 'data created successfully'}, 201

    def put(self, pivot_bussiness_bookkeeping_id):
        parser = reqparse.RequestParser()
        parser.add_argument('bussiness_plan_id', type=str, required=True)
        parser.add_argument('bookkeeping_account_id', type=str, required=True)
        args = parser.parse_args()

        values = Pivot_bussiness_bookkeeping.query.get(pivot_bussiness_bookkeeping_id)
        if values:
            values.bussiness_plan_id = args['bussiness_plan_id']
            values.bookkeeping_account_id = args['bookkeeping_account_id']
            db.session.commit()
            return {'message': 'data updated successfully'}
        else:
            return {'message': 'data not found'}, 404

    def delete(self, pivot_bussiness_bookkeeping_id):
        values = Pivot_bussiness_bookkeeping.query.get(pivot_bussiness_bookkeeping_id)
        if values:
            db.session.delete(values)
            db.session.commit()
            return {'message': 'data deleted successfully'}
        else:
            return {'message': 'data not found'}, 404