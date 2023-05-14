from app import api
from app.controller.bussines_plan.main import *

def BUSSINES_PLAN_API_PATH():
    api.add_resource(OpenAIApi, "/openAI")