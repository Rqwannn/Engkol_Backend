from flask import jsonify, request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.models.User import *
from app.controller.access.access import WhoAreYou


class RoleResource(Resource):
    def get (self):
        role = Money_bookkeeping_role.query.all()

        result = []
        for a in role:
            result.append({
                "role_id":a.role_id,
                "role_name":a.role_name
            })
        
        return jsonify(result)

    def post(self):

        ###################################################
        role = request.json.get('role_name', None)
        ###################################################

        db.session.add(Money_bookkeeping_role(role_name=role))
        db.session.commit()

        return jsonify(message="sucsess added")
    
    def delete(self):
        role = Money_bookkeeping_role.query.all()
        for a in role:
            db.session.delete(a)
        db.session.commit()

        return jsonify(msg="all data deleted")

class RegisterBookkeeping(Resource):
    @jwt_required()
    def post(self):
        user_id=get_jwt_identity()

        role = Money_bookkeeping_role.query.filter_by(role_name='owner').first()
        role_id = role.role_id # akan diubah tergantung frontend

        ####################################################################
        name_account = request.json.get('name_account')
        ####################################################################

        bk_account = Bookkeeping_account(
            name_account=name_account
        )

        db.session.add(bk_account)
        db.session.commit()

        bk_id = bk_account.bookkeeping_account_id

        bk_ticket = Bookkeeping_ticket(
            user_id=user_id,
            role_id=role_id,
            bookkeeping_account_id=bk_id
        )

        db.session.add(bk_ticket)
        db.session.commit()

        return jsonify({
            "data":{
                "ticket":{
                    "bookkeeping_ticket_id" : bk_ticket.bookkeeping_ticket_id,
                    "user_id" : bk_ticket.user_id,
                    "role_id" : bk_ticket.role_id,
                    "bookkeeping_account_id" : bk_ticket.bookkeeping_account_id,
                    "created_at" : bk_ticket.created_at
                },
                "account":{
                    "bookkeeping_account_id": bk_account.bookkeeping_account_id,
                    "name_account": bk_account.name_account,
                    "created_at": bk_account.created_at,
                    "deleted_at": bk_account.deleted_at
                }
            }
        })
    
    # sementara
    def get(self):
        ticket = Bookkeeping_account.query.all()
        result = []
        for a in ticket:
            if not a.deleted_at:
                result.append({
                    "bookkeeping_account_id":a.bookkeeping_account_id,
                    "name_account":a.name_account,
                    "created_at":a.created_at
                })
        return jsonify(ticket=result)

    def delete(self):
        role = Bookkeeping_account.query.all()
        for a in role:
            db.session.delete(a)
        db.session.commit()

        ticket = Bookkeeping_ticket.query.all()
        for a in ticket:
            db.session.delete(a)
        db.session.commit()

        return jsonify(msg="all data deleted")
    
    
class EmployeeResource(Resource):
    def post(self, bookkeeping_account_id):
        akses = ['owner']
        if WhoAreYou(bookkeeping_account_id, akses) == True:

            ###################################################################################
            username = request.json.get('username', None) # username adalah username pegawai
            posisi = request.json.get('posisi', None)
            ###################################################################################
            
            role = Money_bookkeeping_role.query.filter_by(role_name=posisi).first()
            role_id = role.role_id # akan diubah tergantung frontend
            user = Users.query.filter_by(username=username).first()

            if not user:
                return jsonify(message="Username tidak ditemukan")
            
            ticket = Bookkeeping_ticket(
                user_id=user.user_id,
                role_id=role_id,
                bookkeeping_account_id=bookkeeping_account_id
            )

            db.session.add(ticket)
            db.session.commit()

            return jsonify({
                "ticket":{
                        "bookkeeping_ticket_id" : ticket.bookkeeping_ticket_id,
                        "user_id" : ticket.user_id,
                        "role_id" : ticket.role_id,
                        "bookkeeping_account_id" : ticket.bookkeeping_account_id,
                        "created_at" : ticket.created_at
                    }
            })
        else:
            return jsonify(message="Anda tidak diijinkan menambahkan data karyawan")