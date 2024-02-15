from celery import Celery, Task


def celery_init_app(app):
    """Creates a new Celery instance.

    Any code (Tasks/etc.) attached to the celery_app reside
    within the celery_worker, so if you make a change to anything
    attached to the celery_app, you're going to have to restart the
    Celery worker.
    """

    class FlaskTask(Task):
        """Simple Task wrapper to provide app context while our Tasks run."""

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    # AMQP doesn't work as a result_backend for some reason.  We're going to have to
    # go with redis for now (and probably forever, I don't think it's bad).
    celery_opts = {
        "broker_url": "redis://redis:6379",
        "result_backend": "redis://redis:6379",
    }

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(celery_opts)
    celery_app.set_default()
    # At any time, we can use this to access the celery_app directly in our routes if we need to.
    app.extensions["celery"] = celery_app

    return celery_app
