from flask import Blueprint


def test_auth_blueprint_is_importable():
    from app.blueprints import auth

    assert isinstance(auth, Blueprint)


def test_yt_dler_blueprint_is_importable():
    from app.blueprints import yt_dler

    assert isinstance(yt_dler, Blueprint)
