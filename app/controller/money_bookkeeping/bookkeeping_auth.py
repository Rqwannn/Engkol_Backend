import uuid
from datetime import datetime
from flask_login import current_user, login_required
from flask import Flask, session
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager, get_jwt

from app.models.User import *

class Login_bookkeeping(Resource):

    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()

        jwt_data = get_jwt()
        nested_session = jwt_data['nested_session']
        data = nested_session.get('data')


        # print(user_id)
        return {
            "bookkeepint_id":data,
            "user_id":user_id
        }

    @jwt_required()
    def post(self):
        # Parsing data dari POST

        user_id = get_jwt_identity()

        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, help='Username is required')
        parser.add_argument('password', type=str, required=True, help='Password is required')
        args = parser.parse_args()

        # Validasi data
        username = args['username']
        password = args['password']

        if not username or not password:
            return {
                "Pesan": "Username dan password harus diisi",
                "Status": 400
            }

        # Proses autentikasi
        bk_account = Bookkeeping_account.query.filter_by(username=username).first()

        if bk_account and check_password_hash(bk_account.password, password):

            additional_claims = {'nested_session': {'data': bk_account.bookkeeping_account_id}}
            access_token = create_access_token(identity=user_id, additional_claims=additional_claims)
            return {"access_token":access_token}

        else:
            # Jika autentikasi gagal
            return {
                "Pesan": "Username atau password salah",
                "Status": 401
            }



class BookkeepingAccountResource(Resource):

    @jwt_required()
    def get(self):
        user_id=get_jwt_identity()

        data = Bookkeeping_account.query.filter_by(user_id=user_id).all()

        result = []
        for plan in data:
            result.append({
                "bookkeeping_account_id":plan.bookkeeping_account_id,
                "name_account":plan.name_account,
                "username":plan.username,
                "role_id":plan.role_id,
                "activity":plan.activity
            })

        return {'business_plans': result}, 200

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()

        parser = reqparse.RequestParser()
        # parser.add_argument('bookkeeping_ticket_id', type=str, required=True)
        parser.add_argument('role_id', type=str, required=True)
        parser.add_argument('activity', type=str, required=True)
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        parser.add_argument('name_account', type=str, required=True)
        args = parser.parse_args()

        bookkeeping = Bookkeeping_account(
            # bookkeeping_ticket_id=args['bookkeeping_ticket_id'],
            user_id=user_id,
            role_id=args['role_id'],
            activity=args['activity'],
            username=args['username'],
            password=generate_password_hash(args['password']),
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
        parser.add_argument('role_status', type=str, required=True) # 1 for active
        args = parser.parse_args()

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