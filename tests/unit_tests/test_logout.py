from server import app


def test_logout():
    flask_app = app.test_client()

    response = flask_app.get("/logout")
    assert response.status_code == 302
