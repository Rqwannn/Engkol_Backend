from app import api
from app.controller.bussines_plan.main import *


def business_plan_api_path():
    api.add_resource(OpenAIApi, "/openAI")
