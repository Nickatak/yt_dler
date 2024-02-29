import pathlib

from flask import send_from_directory


def serve_react(app):
    """Adds a generic catchall route to serve our react app.

    This points both `/` and `/any_other_matching` to the same serve controller,
    which will then serve up any matching static files as well as the index page
    containing our React app.
    """

    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve(path):
        if path != "" and pathlib.Path(app.static_folder, path).exists():
            return send_from_directory(app.static_folder, path)
        else:
            return send_from_directory(app.static_folder, "index.html")
