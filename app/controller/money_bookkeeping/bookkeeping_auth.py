from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.models.User import *

class RegisterBookkeeping(Resource):
    # @jwt_required()
    def post(self):
        # user_id=get_jwt_identity()

        db.session.add(Bookkeeping_ticket())
        db.session.commit