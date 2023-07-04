import uuid
from datetime import datetime
from flask_login import current_user, login_required
from flask import request, Flask, session
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager, get_jwt
from sqlalchemy.exc import IntegrityError

from app.models.User import *

class RegisterBookkeeping(Resource):
    @jwt_required()
    def post(self):
        user_id=get_jwt_identity()
        name_account = request.json.get('name_account', None)
        username = request.json.get('username', None)
        password = request.json.get('password', None)

        if not name_account:
            msg = 'Nama bisnis harus diisi!'
            return jsonify(message=msg)
        elif not username or not password:
            msg = 'Username dan password harus diisi!'
            return jsonify(message=msg)
        elif len(password) <= 6:
            msg = 'Password harus memiliki setidaknya 6 karakter'
            return jsonify(message=msg)
        else:
            password_hash = generate_password_hash(password)
            values = Bookkeeping_account(
                username=username,
                password=password_hash,
                name_account=name_account,
                role_id='owner' # ini akan diganti
            )

            try:
                db.session.add(values) 
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                message = 'Username sudah digunakan atau tidak tersedia'
                return jsonify(message=message)

                values

                return jsonify({
                "data": {
                    "nama_bisnis": values.name_account,
                    "username": values.username,
                },
                "message": "Registrasi Berhasil",
                "status": 200
            })



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