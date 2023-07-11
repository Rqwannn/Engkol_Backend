from flask import jsonify, request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.models.User import *
from app.controller.object.object import *


class RoleResource(Resource):
    def get (self):
        result = []
        for a in Query.All(Money_bookkeeping_role):
            result.append({
                "role_id":a.role_id,
                "role_name":a.role_name
            })
        
        return jsonify(result)

    def post(self):

        ###################################################
        role_name = request.json.get('role_name', None)
        ###################################################

        db.session.add(Money_bookkeeping_role(role_name=role_name))
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
        bussiness_email = request.json.get('bussiness_email', None)
        bussiness_location = request.json.get('bussiness_location', None)
        postal_code = request.json.get('postal_code', None)
        ####################################################################

        bk_account = Bookkeeping_account(
            name_account=name_account,
            bussiness_email=bussiness_email,
            bussiness_location=bussiness_location,
            postal_code=postal_code

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
                    "bussiness_email": bk_account.bussiness_email,
                    "bussiness_location": bk_account.bussiness_location,
                    "postal_code": bk_account.postal_code,
                    "created_at": bk_account.created_at
                }
            }
        })
    
    # sementara
    def get(self):
        result = []
        for a in Query.All(Bookkeeping_account):
            if not a.is_deleted:
                result.append({
                    "bookkeeping_account_id":a.bookkeeping_account_id,
                    "name_account":a.name_account,
                    "created_at":a.created_at
                })
        return jsonify(ticket=result)

    def delete(self):
        for a in Query.All(Bookkeeping_account):
            db.session.delete(a)
        db.session.commit()


        return jsonify(msg="all data deleted")
    
    
class EmployeeResource(Resource):
    def get(self, bookkeeping_account_id):
        #############################################################
        username = request.json.get('username', None)
        #############################################################
        
        user = Users.query.filter_by(username=username).first()
        acc = Bookkeeping_account.query.filter_by(username=username, bookkeeping_account_id=bookkeeping_account_id, is_deleted=0)

        if not user:
            return jsonify(message=f"{username} tidak ditemukan")
        if not acc:
            return jsonify(data=user)
        


    def post(self, bookkeeping_account_id):
        akses = ['owner', 'manager']
        if Access.WhoAreYou(bookkeeping_account_id, akses) == True:

            ###################################################################################
            username = request.json.get('username', self.get()) # username adalah username pegawai
            posisi = request.json.get('posisi', None) # ini masih harus didiskusikan apakah posisi langsung di post atau role id nya
            ###################################################################################
            
            role = Money_bookkeeping_role.query.filter_by(role_name=posisi).first()
            role_id = role.role_id # akan diubah tergantung frontend
            user = Users.query.filter_by(username=username).first()
            ticket = Bookkeeping_ticket.query.filter_by(user_id=user.user_id).first()
            
            if not ticket:
                ticket = Bookkeeping_ticket(
                    user_id=user.user_id,
                    role_id=role_id,
                    bookkeeping_account_id=bookkeeping_account_id,
                    landing_status=1
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
                return jsonify(message=f"{username} sudah terdaftar")
        else:
            return jsonify(message="Anda tidak diijinkan menambahkan data karyawan")