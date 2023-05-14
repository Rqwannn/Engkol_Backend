from flask import request, abort, jsonify
from flask_restful import Resource, reqparse, fields, marshal_with

class OpenAIApi(Resource):
    def get(self):
        return jsonify({
            "Testi": "Berhasil"
        })