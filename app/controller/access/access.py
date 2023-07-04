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
    jwt_data = get_jwt()
    nested_session = jwt_data['nested_session']
    bookkeeping_id = nested_session.get('data')

    account = Bookkeeping_account.query.filter_by(user_id=user_id).first()
    role = Money_bookkeeping_role.query.filter_by(role_id=account.role_id).first()

    if account.bookkeeping_account_id == bookkeeping_id:
        if role.role_name in akses:
            return True
        else:
            return False
    else:
        return False