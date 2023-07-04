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
    
    def get(self):
        user_id = get_jwt_identity()
        return {"user_id":user_id}, 200

    def post(self):

        # Validasi data
        username = request.json.get('username', None)
        password = request.json.get('password', None)

        if not username or not password:
            return jsonify( {
                "message": "Username dan password harus diisi",
                "status": 400
            })
        
        # Proses autentikasi
        user = Users.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            access_token = create_access_token(identity=user.user_id)
            return jsonify( {
                "token" : access_token,
                "data": {
                    "user_id": user.user_id,
                    "username": user.username,
                    "email": user.email
                },
                "status": 200
            } )

        else:
            # Jika autentikasi gagal
            return jsonify ( {
                "Pesan": "Username atau password salah",
                "status": 401
            } )


class Register(Resource):
    def post(self):
        # fetch data
        username = request.json.get('username', None)
        password = request.json.get('password', None)
        email = request.json.get('email', None)

        # data validation
        if not username or not password or not email:
            return jsonify( {"message": "Formulir tidak boleh kosong!"} )

        elif len(password) <= 6:
            return jsonify( {"message": "Password harus berisi minimal 6 digit!"} )

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
                message = 'Username sudah digunakan atau tidak tersedia'
                return jsonify(message=message)
            
            access_token = create_access_token(identity=values.user_id)

            # return json response
            return jsonify({
                "token" : access_token,
                "data": {
                    "user_id": values.user_id,
                    "username": values.username,
                    "email": values.email
                },
                "message": "Registrasi Berhasil",
                "status": 200
            })