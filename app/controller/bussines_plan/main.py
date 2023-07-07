from flask import request, jsonify, current_app
from flask_restful import Resource
from app import db
from flask_jwt_extended import get_jwt_identity, jwt_required
import openai

from app.models.User import Bussiness_plan

class OpenAIApi(Resource):

    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        print(user_id)

        data = Bussiness_plan.query.filter_by(user_id=user_id, is_deleted=0).all()
        result = []
        for plan in data:
            result.append({
                'bussiness_plan_id': plan.bussiness_plan_id,
                'bussiness_type': plan.bussiness_type,
                'bussiness_email': plan.bussiness_email,
                'target_market':plan.target_market,
                'location': plan.bussiness_location,
                'budget': plan.budgets,
                'created_at': plan.created_at
            })

        return jsonify({
             'data': result,
             'status': 200
        }) 


    @jwt_required()
    def post(self):
            user_id = get_jwt_identity()

            bussiness_type = request.json.get('bussiness_type', None)
            bussiness_location = request.json.get('bussiness_location', None)
            budgets = request.json.get('budgets', None)
            email = request.json.get('email', None)
            target_market = request.json.get('target_market', None)


            # connect to openAis
            app = current_app._get_current_object()
            openai.api_key = app.config['OPENAI_SECRET_KEY']

            completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": f"saya ingin membuka usaha bidang {bussiness_type} di {bussiness_location} dengan modal sebesar {budgets}. berikan dua saran usaha yang cocok untuk saya, lokasi spesifik yang strategis, dan cara pemasarannya"}])
            completed = completion.choices[0].message.content

            values = Bussiness_plan(
                user_id=user_id,
                bussiness_type=bussiness_type,
                bussiness_location=bussiness_location,
                budgets=budgets,
                bussiness_email=email,
                target_market=target_market,
                is_deleted=0,
                status=0,
                ai_message=completed
            )

            db.session.add(values)
            db.session.commit()

            return jsonify(
                message=completed + "/n Agar perusahaan anda bisa bertahan lama, sangat perlu melakukan pencatatan keuangan. Mencatat keuangan perusahaan bukanlah hal yang rumit, mencatat pengeluaran dan pemasukan harian sudah cukup untuk memulai mencatat keuangan. /n Anda dapat menggunakan fitur Pencatatan Keuangan yang tersedia di App Engkol yang sedang kamu gunakan ini.",
                bussiness_type=bussiness_type,
                bussiness_location=bussiness_location,
                target_market=target_market,
                budgets=budgets,
                bussiness_email=email,
            )

    def delete(self, planID):

        plan = Bussiness_plan.query.filter_by(bussiness_plan_id=planID).first()

        plan.is_deleted=1
        db.session.commit()

        return jsonify(message="Data berhasil dihapus")