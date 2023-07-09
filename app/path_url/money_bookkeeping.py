from app import api
from app.controller.money_bookkeeping.money_bookkeeping import *
from app.controller.money_bookkeeping.bookkeeping_auth import *


def bookkeeping_api_path():
    api.add_resource(RegisterBookkeeping, "/api/v1/engkol/resource/bk_register")
    api.add_resource(EmployeeResource, "/api/v1/engkol/resource/bk_employee/<string:bookkeeping_account_id>")
    api.add_resource(PemasukanResource, "/api/v1/engkol/resource/bk_pemasukan/<string:bk_acc_id>")
    api.add_resource(TransactionTypeResource, "/api/v1/engkol/resource/transaction_type")
    api.add_resource(BookkeepingAsetsResource, "/api/v1/engkol/resource/bk_asets")
    api.add_resource(RoleResource, "/api/v1/engkol/resource/role")