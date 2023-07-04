from flask import request, abort, jsonify, session
from flask_restful import Resource, reqparse, fields, marshal_with
from flask.config import Config
from app import db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager

from app.models.User import Users

# Bikin logika login di sini

class Login(Resource):
    
    # get sekalian contoh
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        return {"user_id":user_id}, 200

    def post(self):
        # Parsing data dari POST
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, help='Username is required')
        parser.add_argument('email', type=str, required=True, help='email is required')
        parser.add_argument('password', type=str, required=True, help='Password is required')
        args = parser.parse_args()

        # Validasi data
        username = args['username']
        password = args['password']

        if not username or not password:
            return {
                "message": "Username dan password harus diisi",
                "status": 400
            }

        # Proses autentikasi
        user = Users.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            access_token = create_access_token(identity=user.user_id)
            # print(get_jwt_identity())
            return access_token

        else:
            # Jika autentikasi gagal
            return {
                "Pesan": "Username atau password salah",
                "Status": 401
            }


class Register(Resource):
    def post(self):
        # fetch data
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')

        # data validation
        if not username or not password:
            return {"msg": "Username dan Password tidak boleh kosong!"}

        elif len(password) <= 6:
            return {"msg": "Password harus berisi minimal 6 digit!"}

        else:
            # save data to the database
            password_hash = generate_password_hash(password)
            values = Users(username=username, password=password_hash, email=email)

            # handler if username already use
            try:
                db.session.add(values) 
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                message = 'Username nya udah ada yang pake'
                return message

            # return json response
            return {
                "data": {
                    "username": values.username
                },
                "msg": "Registrasi Berhasil"
            }, 200