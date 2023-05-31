import uuid
from datetime import datetime
from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from app import db

from app.models.User import Profile

class ProfileResource(Resource):
    def get(self, profile_id):
        profile = Profile.query.get(profile_id)
        if profile:
            return {
                'profile_id': profile.profile_id,
                'user_id': profile.user_id,
                'first_name': profile.first_name,
                'last_name': profile.last_name,
                'birth_date': profile.birth_date.isoformat(),
                'telephone_number': profile.telephone_number,
                'postal_code': profile.postal_code,
                'address': profile.address,
                'created_at': profile.created_at.isoformat()
            }
        else:
            return {'message': 'Profile not found'}, 404

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=str, required=True)
        parser.add_argument('first_name', type=str, required=True)
        parser.add_argument('last_name', type=str, required=True)
        parser.add_argument('birth_date', type=str, required=True)
        parser.add_argument('telephone_number', type=str, required=True)
        parser.add_argument('postal_code', type=str, required=True)
        parser.add_argument('address', type=str, required=True)
        args = parser.parse_args()

        profile = Profile(
            user_id=args['user_id'],
            first_name=args['first_name'],
            last_name=args['last_name'],
            birth_date=datetime.strptime(args['birth_date'], '%d-%m-%Y').date(),
            telephone_number=args['telephone_number'],
            postal_code=args['postal_code'],
            address=args['address']
        )

        db.session.add(profile)
        db.session.commit()

        return {'message': 'Profile created successfully'}, 201

    def put(self, profile_id):
        parser = reqparse.RequestParser()
        parser.add_argument('first_name', type=str, required=True)
        parser.add_argument('last_name', type=str, required=True)
        parser.add_argument('birth_date', type=str, required=True)
        parser.add_argument('telephone_number', type=str, required=True)
        parser.add_argument('postal_code', type=str, required=True)
        parser.add_argument('address', type=str, required=True)
        args = parser.parse_args()

        profile = Profile.query.get(profile_id)
        if profile:
            profile.first_name = args['first_name']
            profile.last_name = args['last_name']
            profile.birth_date = datetime.strptime(args['birth_date'], '%d-%m-%Y').date()
            profile.telephone_number = args['telephone_number']
            profile.postal_code = args['postal_code']
            profile.address = args['address']
            db.session.commit()
            return {'message': 'Profile updated successfully'}
        else:
            return {'message': 'Profile not found'}, 404

    def delete(self, profile_id):
        profile = Profile.query.get(profile_id)
        if profile:
            db.session.delete(profile)
            db.session.commit()
            return {'message': 'Profile deleted successfully'}
        else:
            return {'message': 'Profile not found'}, 404
