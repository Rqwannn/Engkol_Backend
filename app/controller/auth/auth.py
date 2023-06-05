from flask import request, jsonify
from flask_restful import Resource, reqparse
from flask.config import Config

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user

from app.models.User import Users
from app import db

# Bikin logika login di sini


class Login(Resource):
    def post(self):
        # Parsing data dari POST
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, help='Username is required')
        parser.add_argument('password', type=str, required=True, help='Password is required')
        args = parser.parse_args()

        # Proses autentikasi
        username = args['username']
        password = args['password']

        user = Users.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):

            login_user(user)

            # Jika autentikasi berhasil

            return jsonify({
                "UserData": user,
                "status": 200,
                "pesan": "Berhasil",
            })
        else:
            # Jika autentikasi gagal
            return jsonify({
                "status": 401,
                "pesan": "Gagal",
            })



    
# Bikin logika register di sini

class Register(Resource):
    def post(self):
        # Ambil data dari permintaan POST
        username = request.form.get('username')
        password = generate_password_hash(request.form.get('password'))

        # validasi data
        if not username or not password:
            return jsonify({
                "Pesan": "Username dan password harus diisi",
                "Status": 400
            })

        # Simpan data ke database
        user = Users(username=username, password=password)

        db.session.add(user)
        db.session.commit()

        # Return JSON response
        return jsonify({
            "Data": {
                "Username": username
            },
            "Pesan": "Registrasi berhasil",
            "Status": 200
        })
