from flask import jsonify, request
from flask_restful import Resource
from app import db
from datetime import datetime
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.models.User import Owner_profile
from app.controller.encryption import *

class ProfileResource(Resource):
    
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()

        profile = Owner_profile.query.filter_by(user_id=user_id).first()

        if not profile:
            return {"status":"0"}
        else:
            response = [{
                "profile_id": profile.profile_id,
                "user_id": profile.user_id,
                "postal_code": decrypt(profile.postal_code),
                "first_name": decrypt(profile.first_name),
                "last_name": decrypt(profile.last_name),
                "birth_date": profile.birth_date,
                "telephone_number": decrypt(profile.telephone_number),
                "address": decrypt(profile.address),
                "is_deleted": profile.is_deleted,
                "created_at": profile.created_at
            }]
            return jsonify(
                status=1,
                data=response
            )

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()

        ####################################################################
        first_name = request.json.get('first_name', None)
        last_name = request.json.get('last_name', None)
        birth_date = request.json.get('birth_date', None)
        telephone_number = request.json.get('telephone_number', None)
        postal_code = request.json.get('postal_code', None)
        address = request.json.get('address', None)
        ####################################################################
        
        date = datetime.strptime(birth_date, '%d-%m-%Y').date()

        profile = Owner_profile(
            user_id=user_id,
            first_name=encrypt(first_name),
            last_name=encrypt(last_name),
            birth_date=date,
            telephone_number=encrypt(telephone_number),
            postal_code=encrypt(postal_code),
            address=encrypt(address)
        )

        db.session.add(profile)
        db.session.commit()

        response = [{
                "profile_id": profile.profile_id,
                "user_id": profile.user_id,
                "postal_code": profile.postal_code,
                "first_name": profile.first_name,
                "last_name": profile.last_name,
                "birth_date": profile.birth_date,
                "telephone_number": profile.telephone_number,
                "address": profile.address,
                "is_deleted": profile.is_deleted,
                "created_at": profile.created_at
            }]
            
        msg = "Profile telah berhasil dibuat!"
        return jsonify(
            message=msg,
            data=response

        )

    @jwt_required()
    def put(self):
        user_id = get_jwt_identity()
        profile=Owner_profile.query.filter_by(user_id=user_id).first()

        user_id = get_jwt_identity()

        ####################################################################
        first_name = request.json.get('first_name', decrypt(profile.first_name))
        last_name = request.json.get('last_name', decrypt(profile.last_name))
        birth_date = request.json.get('birth_date', decrypt(profile.birth_date))
        telephone_number = request.json.get('telephone_number', decrypt(profile.telephone_number))
        postal_code = request.json.get('postal_code', decrypt(profile.postal_code))
        address = request.json.get('address', decrypt(profile.address))
        ####################################################################

        if not profile:
            msg_notProfile = 'Profile tidak ditemukan!'
            return jsonify(message=msg_notProfile)
        else:
            profile.first_name = encrypt(first_name)
            profile.last_name = encrypt(last_name)
            profile.birth_date = encrypt(birth_date)
            profile.telephone_number = encrypt(telephone_number)
            profile.postal_code = encrypt(postal_code)
            profile.address = encrypt(address)
            db.session.commit()

            msg = 'Profile telah berhasil diubah!'
            response = [{
                "profile_id": profile.profile_id,
                "user_id": profile.user_id,
                "postal_code": decrypt(profile.postal_code),
                "first_name": decrypt(profile.first_name),
                "last_name": decrypt(profile.last_name),
                "birth_date": profile.birth_date,
                "telephone_number": decrypt(profile.telephone_number),
                "address": decrypt(profile.address),
                "is_deleted": profile.is_deleted,
                "created_at": profile.created_at
            }]
            return jsonify(message=msg, data=response)