from flask_wtf import CSRFProtect

csrf = CSRFProtect()


def init_csrf(app):
    """Enables CSRF protection for any WTForms Forms."""
    csrf.init_app(app)
