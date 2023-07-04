from app import api
from app.controller.money_bookkeeping.money_bookkeeping import *
from app.controller.money_bookkeeping.bookkeeping_auth import *


def bookkeeping_api_path():
    api.add_resource(BookkeepingAccountResource, "/api/v1/engkol/resource/bk_account")
    api.add_resource(BookkeepingRoleResource, "/api/v1/engkol/resource/bk_role")
    api.add_resource(ActivityRoleResource, "/api/v1/engkol/resource/bk_activity")
    api.add_resource(MoneyBookkkeepingResource, "/api/v1/engkol/resource/money_bookkeeping")
    api.add_resource(TransactionTypeResource, "/api/v1/engkol/resource/transaction_type")
    api.add_resource(BookkeepingAsetsResource, "/api/v1/engkol/resource/bk_asets")
    api.add_resource(PivotBussinessBookkeepingResource, "/api/v1/engkol/resource/pivot_bussiness_bookkeeping")
    api.add_resource(Login_bookkeeping, "/api/v1/engkol/resource/bk_login")
