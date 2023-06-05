from datetime import datetime
from flask import jsonify
from flask_login import current_user
from flask_restful import Resource, reqparse
from app import db

from app.models.User import Profile

class ProfileResource(Resource):
    def get(self):
        
        # Bisa menggunakan cara ini current_user.profile karena menggunakan relationship

        profile = current_user.profile

        if profile:
            return jsonify({
                'data': profile,
                'pesan': "Data profile berhasil di ambil",
                'status': 200
            })
        else:
            return jsonify(
                {
                    'pesan': 'Data profile tidak di temukan, mohon untuk menambah data profile',
                    'status': 204
                }
            )
        
    def post(self):
        parser = reqparse.RequestParser()
        
        parser.add_argument('first_name', type=str, required=True)
        parser.add_argument('last_name', type=str, required=True)
        parser.add_argument('birth_date', type=str, required=True)
        parser.add_argument('telephone_number', type=str, required=True)
        parser.add_argument('postal_code', type=str, required=True)
        parser.add_argument('address', type=str, required=True)

        args = parser.parse_args()

        profile = Profile(
            user_id=current_user,
            first_name=args['first_name'],
            last_name=args['last_name'],
            birth_date=datetime.strptime(args['birth_date'], '%d-%m-%Y').date(),
            telephone_number=args['telephone_number'],
            postal_code=args['postal_code'],
            address=args['address']
        )

        db.session.add(profile)
        db.session.commit()

        return jsonify({
            "pesan": "Profile berhasil di tambahkan"
        })

    def put(self, profile_id):
        parser = reqparse.RequestParser()

        parser.add_argument('first_name', type=str, required=True)
        parser.add_argument('last_name', type=str, required=True)
        parser.add_argument('birth_date', type=str, required=True)
        parser.add_argument('telephone_number', type=str, required=True)
        parser.add_argument('postal_code', type=str, required=True)
        parser.add_argument('address', type=str, required=True)
        
        args = parser.parse_args()

        profile = Profile.query.filter_by(profile_id=profile_id)

        if profile:

            data = {
                "first_name": args['first_name'],
                "last_name": args['last_name'],
                "birth_date": datetime.strptime(args['birth_date'], '%d-%m-%Y').date(),
                "telephone_number": args['telephone_number'],
                "postal_code": args['postal_code'],
                "address": args['address'],
            }

            profile.update(data)
            db.session.commit()

            return jsonify({
                "data": profile,
                "pesan": "Profile berhasil di perbarui",
                "status": 200
            })
        else:
            return jsonify({
                "pesan": "Profile tidak di temukan, gagal di perbarui",
                "status": 404
            })
