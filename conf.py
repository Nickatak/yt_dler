import os
import pathlib

from dotenv import load_dotenv

load_dotenv()
ROOT_DIR = pathlib.Path(__file__).parent


class DevConf:
    DEBUG = os.environ.get("DEBUG")
    DROP_DB = os.environ.get("DROP_DB")
    TEMP_DIR = os.environ.get("TEMP_DIR")
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")


class TestConf(DevConf):
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_TESTING_URI")
    TESTING = True
