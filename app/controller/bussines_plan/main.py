from flask import request, abort, jsonify, current_app
from flask_restful import Resource, reqparse, fields, marshal_with
from flask.config import Config
import openai
openai.api_key = current_app.config['OPENAI_SECRET_KEY']

class OpenAIApi(Resource):
    def get(self):
        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": message}])
        print(completion.choices[0].message.content)
        return jsonify({
            "Testi": "Berhasil"
        })
    
    #class openai get post