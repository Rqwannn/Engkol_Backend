from app import api
from app.controller.form.profile import ProfileResource


def forms_api_path():
    api.add_resource(ProfileResource, "/api/v1/engkol/resource/profile")
    # api.add_resource(ProfileResource, "/api/v1/engkol/resource/profile/<string:profile_id>")
