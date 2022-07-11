from server import app


def test_overviewClubs():
    flask_app = app.test_client()

    response = flask_app.get("/overview")
    assert response.status_code == 200
