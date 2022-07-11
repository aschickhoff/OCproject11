from server import app


def test_index():
    flask_app = app.test_client()

    response = flask_app.get("/")
    assert response.status_code == 200
    assert b"Welcome to the GUDLFT" in response.data


def test_index_post():
    flask_app = app.test_client()

    response = flask_app.post("/")
    assert response.status_code == 405
    assert b"Welcome to the GUDLFT" not in response.data
