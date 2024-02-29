from flask import url_for


def test_index_route_resolvable(app, client):
    with app.test_request_context():
        url = url_for("yt_dler.start_upload")
        assert url == "/upload"


def test_has_index_route(app, client):
    with app.test_request_context():
        # This is not finished
        client.get(url_for("yt_dler.start_upload"))
