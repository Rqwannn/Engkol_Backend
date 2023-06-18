import uuid
from datetime import datetime
from flask_login import current_user, login_required
from flask import Flask, session
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from app import db

from app.models.User import *

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
