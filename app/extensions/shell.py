from sqlalchemy import select

from app.models import User, db_session


def add_shell_contexts(app):
    """Simple shell context to add common variables.

    Adds the following variables to `flask shell`:
        :User: - The `app.models.users.User` class.
        :select: - SQLAlchemy's basic `select` statement.
        :db_session: - A SQLAlchemy session so we can execute queries.
    """

    @app.shell_context_processor
    def make_shell_context():
        return {
            "User": User,
            "select": select,
            "db_session": db_session,
        }
