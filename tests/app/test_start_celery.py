from celery import Celery

from app.start_celery import celery_app


def test_celery_app_should_exist():
    assert isinstance(celery_app, Celery)
