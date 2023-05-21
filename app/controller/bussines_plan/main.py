from flask import request, abort, jsonify, current_app
from flask_restful import Resource, reqparse, fields, marshal_with
from flask.config import Config
import openai


class OpenAIApi(Resource):
    def get(self):
        app = current_app._get_current_object()
        openai.api_key = app.config['OPENAI_SECRET_KEY']

        # completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": message}])
        # print(completion.choices[0].message.content)
        return jsonify({
            "Testi": "Berhasil"
        })
    
    # class openai get post
