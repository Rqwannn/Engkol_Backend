from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
from flask import jsonify
from app.models.User import Bookkeeping_ticket, Money_bookkeeping_role


@jwt_required()
# akses bookkeeping
def WhoAreYou(id, akses):
    user_id = get_jwt_identity()

    ticket = Bookkeeping_ticket.query.filter_by(user_id=user_id).first()
    if not ticket:
        return jsonify(message="Anda tidak tertaut ke akun pembukuan uang")
    
    tickets = Bookkeeping_ticket.query.filter_by(bookkeeping_account_id=id, user_id=user_id)
    for ticket in tickets:
        roles = Money_bookkeeping_role.query.filter_by(role_id=ticket.role_id).first()
        if roles.role_name in akses:
            return True
    return False 


@jwt_required()
def ticket(bk_id):
    user_id = get_jwt_identity()
    ticket = Bookkeeping_ticket.query.filter_by(user_id=user_id).first()
    if not ticket:
        return jsonify(message="Anda tidak tertaut ke akun pembukuan uang")
    tickets = Bookkeeping_ticket.query.filter_by(bookkeeping_account_id=bk_id, user_id=user_id)
    return tickets.bookkeeping_ticket_id