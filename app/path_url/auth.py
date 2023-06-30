from app import api
from app.controller.auth.auth import *


def auth_api_path():
    api.add_resource(Login, "/api/v1/engkol/resource/login")
    api.add_resource(Register, "/api/v1/engkol/resource/register")