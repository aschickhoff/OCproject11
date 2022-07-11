from server import app


def test_showSummary_valid_email(setup):
    flask_app = app.test_client()
    club = setup[0]

    response = flask_app.post("/showSummary", data={"email": club[0]["email"]})
    assert response.status_code == 200
    assert f"Welcome, {club[0]['email']}" in response.data.decode()


def test_showSummary_invalid_email(setup):
    flask_app = app.test_client()
    invalid_email = setup[2]

    response = flask_app.post("/showSummary", data={"email": invalid_email})
    assert response.status_code == 401


def test_showSummary_empty_email():
    flask_app = app.test_client()
    empty_email = ""

    response = flask_app.post("/showSummary", data={"email": empty_email})
    assert response.status_code == 401
