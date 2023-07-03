import uuid
from datetime import datetime
from flask_login import current_user, login_required
from flask import Flask, session
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from app import db
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager

from app.models.User import Users, Owner_profile

class ProfileResource(Resource):
    
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()

        profile = Owner_profile.query.filter_by(user_id=user_id).first()

        if not profile:
             return {"status":"0"}
        else:
             return {"status":"1"}        

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()

        parser = reqparse.RequestParser()
        parser.add_argument('first_name', type=str, required=True)
        parser.add_argument('last_name', type=str, required=True)
        parser.add_argument('birth_date', type=str, required=True)
        parser.add_argument('telephone_number', type=str, required=True)
        # parser.add_argument('postal_code', type=str, required=True)
        parser.add_argument('address', type=str, required=True)
        args = parser.parse_args()

        profile = Owner_profile(
            user_id=user_id,
            first_name=args['first_name'],
            last_name=args['last_name'],
            birth_date=datetime.strptime(args['birth_date'], '%d-%m-%Y').date(),
            telephone_number=args['telephone_number'],
            # postal_code=args['postal_code'],
            address=args['address']
        )

        db.session.add(profile)
        db.session.commit()

        return {'message': 'Profile created successfully'}, 201

    @jwt_required()
    def put(self):
        user_id = get_jwt_identity()
        
        parser = reqparse.RequestParser()
        parser.add_argument('first_name', type=str, required=True)
        parser.add_argument('last_name', type=str, required=True)
        parser.add_argument('birth_date', type=str, required=True)
        parser.add_argument('telephone_number', type=str, required=True)
        # parser.add_argument('postal_code', type=str, required=True)
        parser.add_argument('address', type=str, required=True)
        args = parser.parse_args()

        profile=Owner_profile.query.filter_by(user_id=user_id).first()

        if not profile:
            return {'message': 'Profile not found'}, 404
        else:
            profile.first_name = args['first_name']
            profile.last_name = args['last_name']
            profile.birth_date = datetime.strptime(args['birth_date'], '%d-%m-%Y').date()
            profile.telephone_number = args['telephone_number']
            # profile.postal_code = args['postal_code']
            profile.address = args['address']
            db.session.commit()

            return {'message': 'Profile updated successfully'}