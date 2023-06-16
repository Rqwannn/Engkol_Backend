import uuid
from datetime import datetime
from flask_login import current_user, login_required
from flask import Flask, session
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from app import db

from app.models.User import *

class bookkeepingResource(Resource):
    def get(self, bookkeeping_account_id):
        bookkeeping = bookkeeping_account.query.get(bookkeeping_account_id)
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

        bookkeeping = bookkeeping_account(
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

        bookkeeping = bookkeeping_account.query.get(bookkeeping_id)
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
        bookkeeping = bookkeeping_account.query.get(bookkeeping_id)
        if bookkeeping:
            db.session.delete(bookkeeping)
            db.session.commit()
            return {'message': 'bookkeeping deleted successfully'}
        else:
            return {'message': 'bookkeeping not found'}, 404


class BookkeepingRoleResource(Resource):
    def get(self, BookkeepingRole_id):
        BookkeepingRole = Money_bookkeeping_role.query.get(BookkeepingRole_id)
        if BookkeepingRole:
            return {
                'data': BookkeepingRole,
            }
        else:
            return {'message': 'BookkeepingRole not found'}, 404

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('role_name', type=str, required=True)
        parser.add_argument('role_status', type=str, required=True)
        args = parser.parse_args()

        print(current_user)

        BookkeepingRole = Money_bookkeeping_role(
            role_name=args['role_name'],
            role_status=args['role_status']
        )

        db.session.add(BookkeepingRole)
        db.session.commit()

        return {'message': 'BookkeepingRole created successfully'}, 201

    def put(self, BookkeepingRole_id):
        parser = reqparse.RequestParser()
        parser.add_argument('role_name', type=str, required=True)
        parser.add_argument('role_status', type=str, required=True)
        args = parser.parse_args()

        BookkeepingRole = Money_bookkeeping_role.query.get(BookkeepingRole_id)
        if BookkeepingRole:
            BookkeepingRole.role_name = args['role_name']
            BookkeepingRole.role_status = args['role_status']
            db.session.commit()
            return {'message': 'BookkeepingRole updated successfully'}
        else:
            return {'message': 'BookkeepingRole not found'}, 404

    def delete(self, BookkeepingRole_id):
        BookkeepingRole = Money_bookkeeping_role.query.get(BookkeepingRole_id)
        if BookkeepingRole:
            db.session.delete(BookkeepingRole)
            db.session.commit()
            return {'message': 'BookkeepingRole deleted successfully'}
        else:
            return {'message': 'BookkeepingRole not found'}, 404


class ActivityRoleResource(Resource):
    def get(self, activity_id):
        ActivityRole = Activity_role.query.get(activity_id)
        if ActivityRole:
            return {
                'data': ActivityRole,
            }
        else:
            return {'message': 'ActivityRole not found'}, 404

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('money_bookkeeping_account', type=str, required=True)
        parser.add_argument('activity', type=str, required=True)
        parser.add_argument('perubahan', type=str, required=True)
        parser.add_argument('postal_code', type=str, required=True)
        parser.add_argument('address', type=str, required=True)
        args = parser.parse_args()

        print(current_user)

        ActivityRole = Activity_role(
            money_bookkeeping_account=args['money_bookkeeping_account'],
            activity=args['activity'],
            perubahan=args['perubahan'],
        )

        db.session.add(ActivityRole)
        db.session.commit()

        return {'message': 'ActivityRole created successfully'}, 201

    def put(self, activity_id):
        parser = reqparse.RequestParser()
        parser.add_argument('money_bookkeeping_account', type=str, required=True)
        parser.add_argument('activity', type=str, required=True)
        parser.add_argument('perubahan', type=str, required=True)
        args = parser.parse_args()

        ActivityRole = Activity_role.query.get(activity_id)
        if ActivityRole:
            ActivityRole.money_bookkeeping_account = args['money_bookkeeping_account']
            ActivityRole.activity = args['activity']
            ActivityRole.perubahan = args['perubahan']
            db.session.commit()
            return {'message': 'ActivityRole updated successfully'}
        else:
            return {'message': 'ActivityRole not found'}, 404

    def delete(self, activity_id):
        ActivityRole = Activity_role.query.get(activity_id)
        if ActivityRole:
            db.session.delete(ActivityRole)
            db.session.commit()
            return {'message': 'ActivityRole deleted successfully'}
        else:
            return {'message': 'ActivityRole not found'}, 404
