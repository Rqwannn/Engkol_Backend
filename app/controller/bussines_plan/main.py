from flask import request, jsonify, current_app
from flask_restful import Resource
from app import db
from datetime import datetime
import pytz
from flask_jwt_extended import get_jwt_identity, jwt_required
import openai

from app.models.User import *

class OpenAIApi(Resource):

    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()

        data = Bussiness_plan.query.filter_by(user_id=user_id, is_deleted=0).all()
        result = []
        for plan in data:
            result.append({
                "message":plan.ai_message,
                "bussiness_plan_id":plan.bussiness_plan_id,
                "user_id":plan.user_id,
                "bussiness_name":plan.bussiness_name,
                "bussiness_email":plan.bussiness_email,
                "bussiness_type":plan.bussiness_type,
                "postal_code":plan.postal_code,
                "bussiness_location":plan.bussiness_location,
                "budgets":plan.budgets,
                "target_market":plan.target_market,
                "status":plan.status,
                "is_deleted":plan.is_deleted,
                "created_at":plan.created_at
            })

        return jsonify({
             'data': result,
             'status': 200
        }) 


    @jwt_required()
    def post(self):
            user_id = get_jwt_identity()

            #######################################################################
            bussiness_name = request.json.get('bussiness_name', None)
            bussiness_email = request.json.get('bussiness_email', None)
            bussiness_type = request.json.get('bussiness_type', None)
            bussiness_location = request.json.get('bussiness_location', None)
            postal_code = request.json.get('postal_code', None)
            target_market = request.json.get('target_market', None)
            budgets = request.json.get('budgets', None)
            ########################################################################

            # connect to openAis
            app = current_app._get_current_object()
            openai.api_key = app.config['OPENAI_SECRET_KEY']
            if not target_market:
               completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": f"saya ingin membuka usaha bidang {bussiness_type} di {bussiness_location} dengan modal sebesar {budgets}. berikan dua saran usaha yang cocok untuk saya, lokasi spesifik yang strategis, dan cara pemasarannya"}])
            else:
               completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": f"saya ingin membuka usaha bidang {bussiness_type} di {bussiness_location} yang target marketnya adalah {target_market} dengan modal sebesar {budgets}. berikan dua saran usaha yang cocok untuk saya, lokasi spesifik yang strategis, dan cara pemasarannya"}])
            completed = completion.choices[0].message.content

            values = Bussiness_plan(
                user_id=user_id,
                bussiness_name=bussiness_name,
                bussiness_email=bussiness_email,
                bussiness_type=bussiness_type,
                bussiness_location=bussiness_location,
                postal_code=postal_code,
                budgets=budgets,
                target_market=target_market,
                is_deleted=0,
                status=0,
                ai_message=completed
            )

            db.session.add(values)
            db.session.commit()

            return jsonify(
                message=values.ai_message,
                bussiness_plan_id=values.bussiness_plan_id,
                user_id=values.user_id,
                bussiness_name=values.bussiness_name,
                bussiness_email=values.bussiness_email,
                bussiness_type=values.bussiness_type,
                postal_code=values.postal_code,
                bussiness_location=values.bussiness_location,
                budgets=values.budgets,
                target_market=values.target_market,
                status=values.status,
                is_deleted=values.is_deleted,
                created_at=values.created_at
            )

    def delete(self, planID):

        plan = Bussiness_plan.query.filter_by(bussiness_plan_id=planID).first()

        plan.is_deleted=1
        db.session.commit()

        return jsonify(message=f"Data {plan.bussiness_name} berhasil dihapus")
    
    @jwt_required()
    def put(self, planID):
        user_id=get_jwt_identity()

        role = Money_bookkeeping_role.query.filter_by(role_name='owner').first()
        role_id = role.role_id # akan diubah tergantung frontend
        plan = Bussiness_plan.query.filter_by(bussiness_plan_id=planID).first()

        bk_account = Bookkeeping_account(
            name_account=plan.bussiness_name,
            bussiness_email=plan.bussiness_email,
            bussiness_location=plan.bussiness_location,
            postal_code=plan.postal_code
        )

        db.session.add(bk_account)
        db.session.commit()

        bk_id = bk_account.bookkeeping_account_id

        bk_ticket = Bookkeeping_ticket(
            user_id=user_id,
            role_id=role_id,
            bookkeeping_account_id=bk_id,
            landing_status=1
        )

        plan.status = 1
        db.session.add(bk_ticket)
        db.session.commit()

        return jsonify({
            "data":{
                "ticket":{
                    "bookkeeping_ticket_id" : bk_ticket.bookkeeping_ticket_id,
                    "user_id" : bk_ticket.user_id,
                    "role_id" : bk_ticket.role_id,
                    "bookkeeping_account_id" : bk_ticket.bookkeeping_account_id,
                    "created_at" : bk_ticket.created_at
                },
                "account":{
                    "bookkeeping_account_id": bk_account.bookkeeping_account_id,
                    "name_account": bk_account.name_account,
                    "bussiness_email": bk_account.bussiness_email,
                    "bussiness_location": bk_account.bussiness_location,
                    "postal_code": bk_account.postal_code,
                    "created_at": bk_account.created_at
                }
            }
        })