from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
from flask import jsonify
from app.models.User import *

class Access():
    @jwt_required()
    # akses bookkeeping
    def WhoAreYou(bk_id, akses):
        user_id = get_jwt_identity()

        ticket = Bookkeeping_ticket.query.filter_by(user_id=user_id).first()
        if not ticket:
            return jsonify(message="Anda tidak tertaut ke akun pembukuan uang")
        
        tickets = Bookkeeping_ticket.query.filter_by(bookkeeping_account_id=bk_id, user_id=user_id)
        for ticket in tickets:
            roles = Money_bookkeeping_role.query.filter_by(role_id=ticket.role_id).first()
            if roles.role_name in akses:
                return True
        return False 

    @jwt_required()
    def Ticket(bk_id):
        user_id = get_jwt_identity()
        ticket = Bookkeeping_ticket.query.filter_by(user_id=user_id, bookkeeping_account_id=bk_id, is_deleted=0).first()
        return ticket.bookkeeping_ticket_id
        
        
class Query():
    def All(table):
        result = table.query.all()
        return result

    def TransactionTypeId(role):
        tipe_transaksi = Transaction_type.query.filter_by(category_name=role).first()
        tipe_id = tipe_transaksi.transaction_type_id
        return tipe_id