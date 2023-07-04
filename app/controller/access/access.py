import uuid
from datetime import datetime
from flask_login import current_user, login_required
from flask import Flask, session
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from app import db
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager

from app.models.User import Bookkeeping_account, Money_bookkeeping_role


# cara pengguaan, di atasnyya dibuat dulu
# variabel akses yang isinya user yang diijinkan
@jwt_required()
# melihat role user
def WhoAreYou(akses):
    user_id = get_jwt_identity()

    if not akses:
        return {'msg': 'Anda harus membuat array akses yang berisi role yang diberikan akses'}

    else:
        account = Bookkeeping_account.query.filter_by(user_id=user_id).first()
        role = Money_bookkeeping_role.query.filter_by(role_id=account.role_id).first()

        if role in akses:
            return True

        else:
            return False