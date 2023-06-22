from flask import request, abort, jsonify, current_app
from flask_restful import Resource, reqparse, fields, marshal_with
from flask.config import Config
from app import db
import openai

from app.models.User import Bussiness_plan

class OpenAIApi(Resource):

    def get(self, bussiness_plan_id):
        plan = Bussiness_plan.query.get(bussiness_plan_id)
        if plan:
            return {
                'data': plan,
            }
        else:
            return {'message': 'bookkeeping not found'}, 404

    def post(self):
            parser = reqparse.RequestParser()
            parser.add_argument('user_id', type=str, required=True)
            parser.add_argument('bussiness_type', type=str, required=True)
            parser.add_argument('bussiness_location', type=str, required=True)
            parser.add_argument('budgets', type=str, required=True)
            args = parser.parse_args()

            # connect to openAi

            app = current_app._get_current_object()
            openai.api_key = app.config['OPENAI_SECRET_KEY']

            completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": f"saya ingin membuka usaha bidang {args['bussiness_type']} di {args['bussiness_location']} dengan modal sebesar {args['budgets']}. berikan dua saran usaha yang cocok untuk saya, lokasi spesifik yang strategis, dan cara pemasarannya"}])
            completed = completion.choices[0].message.content

            values = Bussiness_plan(
                user_id=args['user_id'],
                bussiness_type=args['bussiness_type'],
                bussiness_location=args['bussiness_location'],
                budgets=args['budgets'],
                ai_message=completed
            )

            db.session.add(values)
            db.session.commit()

            return jsonify(completed + "/n Agar perusahaan anda bisa berlangsung lama, sangat perlu melakukan pencatatan keuangan. Mencatat keuangan perusahaan bukanlah hal yang rumit, mencatat pengeluaran dan pemasukan harian sudah cukup untuk memulai mencatat keuangan. /n Anda dapat menggunakan fitur Pencatatan Keuangan yang tersedia di App Engkol yang sedang kamu gunakan ini.")
