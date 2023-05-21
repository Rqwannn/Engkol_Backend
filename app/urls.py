def __URLPATH__():

    # Register Path

    from app.path_url.bussines_plan import business_plan_api_path
    from app.path_url.auth import auth_api_path

    business_plan_api_path()
    auth_api_path()