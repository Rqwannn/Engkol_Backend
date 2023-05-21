from flask import request, abort, jsonify, current_app
from flask_restful import Resource, reqparse, fields, marshal_with
from flask.config import Config

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user

# Bikin logika login di sini

class Login(Resource):
    def post(self):
        

        # Return Json Seperti ini

        return jsonify({
            "Data": {
                # "Username":
                # "Password"
                # Dll kecuali Id user jangan di return
            },
            "Pesan": "Berhasil", # Bisa di ubah se enaknya aja
            "Status": 200
        })
    
# Bikin logika register di sini

class Register(Resource):
    def post(self):

        # Return Json Seperti ini

        return jsonify({
            "Data": {
                # "Username":
                # "Password"
                # Dll kecuali Id user jangan di return
            },
            "Pesan": "Berhasil", # Bisa di ubah se enaknya aja
            "Status": 200
        })