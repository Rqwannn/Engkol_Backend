from flask import request, abort, jsonify, current_app
from flask_restful import Resource, reqparse, fields, marshal_with
from flask.config import Config

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user

from app.models.User import Users

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
        password = check_password_hash(args['password'])

        user = Users.query.filter_by(username=username).first()

        if user and user.check_password_hash(password):

            login_user(user)

            # Jika autentikasi berhasil
            return jsonify({
                "Data": {
                    "Username": user.username,
                },
                "Pesan": "Berhasil",
                "Status": 200
            })
        else:
            # Jika autentikasi gagal
            return jsonify({
                "Pesan": "Username atau password salah",
                "Status": 401
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
        user.save()  

        # Return JSON response
        return jsonify({
            "Data": {
                "Username": username
            },
            "Pesan": "Registrasi berhasil",
            "Status": 200
        })
