"""At this time, we're not using flask-login.  TODO: implement auth system."""

import flask_login

from app.models import User

login_manager = flask_login.LoginManager()


def init_flask_login(app):
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "You must be authorized to access this tool."
    login_manager.login_message_category = "info"

    @login_manager.user_loader
    def load_user(user_id):
        return User.get_by_id(user_id)
