from pathlib import Path

from flask import Flask


def test_app_should_exist(app):
    assert isinstance(app, Flask)


def test_temp_dir_should_exist(app):
    assert Path(app.config["TEMP_DIR"]).is_dir()


def test_db_file_should_exist(app):
    assert Path(Path(app.instance_path).parent, "test.db").is_file()
