import os
import pathlib
import uuid

from dotenv import load_dotenv
from flask import Flask

from app.blueprints import auth, yt_dler
from app.extensions.celery import celery_init_app
from app.extensions.flask_login import init_flask_login
from app.extensions.react import serve_react
from app.extensions.shell import add_shell_contexts
from app.extensions.wtforms import init_csrf
from app.models import create_all, drop_all
from conf import DevConf

load_dotenv()


def create_app(CONFIG=DevConf):
    app = Flask(__name__)
    app.config.from_object(CONFIG)
    app.secret_key = uuid.uuid4().hex

    init_csrf(app)
    init_flask_login(app)
    add_shell_contexts(app)
    celery_init_app(app)
    serve_react(app)

    if app.config["DROP_DB"]:
        drop_all()
    create_all()

    TEMP_DIR = pathlib.Path(os.environ.get("TEMP_DIR"))
    if not TEMP_DIR.is_dir():
        os.mkdir(TEMP_DIR)

    app.register_blueprint(auth)
    app.register_blueprint(yt_dler)

    return app
