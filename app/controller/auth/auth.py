from flask import request, abort, jsonify, session
from flask_restful import Resource, reqparse, fields, marshal_with
from flask.config import Config
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager

from app.models.User import Users

# Bikin logika login di sini

class Login(Resource):


    # get sekalian contoh
    @jwt_required()
    def get(self):
        username = get_jwt_identity()
        user = Users.query.filter_by(username=username).first()

        if not user:
            return {"message":"user not found"}, 404

        return {"user_id":user.user_id}, 200

    def post(self):
        # Parsing data dari POST
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
        user = Users.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            access_token = create_access_token(identity=username)
            # print(get_jwt_identity())
            return jsonify(access_token=access_token)

        else:
            # Jika autentikasi gagal
            return {
                "Pesan": "Username atau password salah",
                "Status": 401
            }


class Register(Resource):
    def post(self):
        # Ambil data dari permintaan POST
        username = request.form.get('username')
        password = generate_password_hash(request.form.get('password'))  # hashing password nya dihapus dulu

        # validasi data
        if not username or not password:
            return jsonify({
                "Pesan": "Username dan password harus diisi",
                "Status": 400
            })

        if len(password) < 6:
            return jsonify({
                "Pesan": "Password harus memiliki setidaknya 6 digit karakter",
                "Status": 400
            })

        # Simpan data ke database
        user = Users(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        
        # Return JSON response
        return jsonify({
            "data":{
                "user_id":user.user_id,
            },
            "Pesan": "Registrasi berhasil",
            "Status": 200
        })