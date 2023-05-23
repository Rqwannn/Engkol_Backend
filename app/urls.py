def __URLPATH__():

    # Register Path

    from app.path_url.bussines_plan import business_plan_api_path
    from app.path_url.auth import auth_api_path

    business_plan_api_path()
    auth_api_path()
    
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user
from app.models import User

app = Flask(__name__)
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    return user

# Register Path
from app.path_url.bussines_plan import business_plan_api_path
from app.path_url.auth import auth_api_path

business_plan_api_path()
auth_api_path()

# Login Path
def login_api_path():
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':

            username = request.form['username']
            password = request.form['password']

            if user and user.password == password:
                user = User.query.filter_by(username=username).first()

                login_user(user)

                return redirect(url_for('home'))

        return True

    login()

__URLPATH__()
app.run()
