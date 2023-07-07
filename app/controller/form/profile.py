from flask import jsonify, request
from flask_restful import Resource
from app import db
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.models.User import Owner_profile

class ProfileResource(Resource):
    
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()

        profile = Owner_profile.query.filter_by(user_id=user_id).first()

        if not profile:
            return {"status":"0"}
        else:
            response = [{
                "first_name": profile.first_name,
                "last_name": profile.last_name,
                "birth_date": profile.birth_date.strftime("%d-%m-%Y"),
                "telephone_number": profile.telephone_number,
                "address": profile.address
            }]
            return jsonify(
                status=1,
                data=response
            )

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        first_name = request.json.get('first_name', None)
        last_name = request.json.get('last_name', None)
        birth_date = request.json.get('birth_date', None)
        telephone_number = request.json.get('telephone_number', None)
        postal_code = request.json.get('postal_code', None)
        address = request.json.get('address', None)

        profile = Owner_profile(
            user_id=user_id,
            first_name=first_name,
            last_name=last_name,
            birth_date=birth_date,
            telephone_number=telephone_number,
            postal_code=postal_code,
            address=address
        )

        db.session.add(profile)
        db.session.commit()

        msg = "Profile telah berhasil dibuat!"
        return jsonify(message=msg)

    @jwt_required()
    def put(self):
        user_id = get_jwt_identity()
        profile=Owner_profile.query.filter_by(user_id=user_id).first()

        user_id = get_jwt_identity()
        first_name = request.json.get('first_name', profile.first_name)
        last_name = request.json.get('last_name', profile.last_name)
        birth_date = request.json.get('birth_date', profile.birth_date)
        telephone_number = request.json.get('telephone_number', profile.telephone_number)
        postal_code = request.json.get('postal_code', profile.postal_code)
        address = request.json.get('address', profile.address)

        if not profile:
            msg_notProfile = 'Profile tidak ditemukan!'
            return jsonify(message=msg_notProfile)
        else:
            profile.first_name = first_name
            profile.last_name = last_name
            profile.birth_date = birth_date
            profile.telephone_number = telephone_number
            profile.postal_code = postal_code
            profile.address = address
            db.session.commit()

            msg = 'Profile telah berhasil diubah!'
            
            return jsonify(message=msg, data = {
                "first_name":first_name,
                "last_name":last_name,
                "birth_date":birth_date,
                "telephone_number":telephone_number,
                "postal_code":postal_code,
                "address":address
            })