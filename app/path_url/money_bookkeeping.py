from app import api
from app.controller.money_bookkeeping.money_bookkeeping import *


def money_bookkeeping_api_path():
    api.add_resource(BookkeepingAccountResource, "/api/v1/engkol/resource/BookkeepingAccount")
    api.add_resource(BookkeepingRoleResource, "/api/v1/engkol/resource/BookkeepingRole")
    api.add_resource(ActivityRoleResource, "/api/v1/engkol/resource/ActivityRole")
