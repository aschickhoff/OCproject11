from server import app


def test_purchasePlaces_success(setup):
    flask_app = app.test_client()

    competition = setup[1]
    club = setup[0]

    response = flask_app.post(
        "/purchasePlaces",
        data={
            "places": 2,
            "club": club[0]["name"],
            "competition": competition[0]["name"],
        },
    )
    assert response.status_code == 200
    assert b"Great-booking complete" in response.data


def test_purchasePlaces_failed_missing_places(setup):
    flask_app = app.test_client()

    competition = setup[1]
    club = setup[0]

    response = flask_app.post(
        "/purchasePlaces",
        data={
            "places": 10,
            "club": club[0]["name"],
            "competition": competition[0]["name"],
        },
    )
    assert response.status_code == 403


def test_purchasePlaces_failed_missing_points(setup):
    flask_app = app.test_client()

    competition = setup[1]
    club = setup[0]

    response = flask_app.post(
        "/purchasePlaces",
        data={
            "places": 11,
            "club": club[1]["name"],
            "competition": competition[1]["name"],
        },
    )
    assert response.status_code == 403


def test_purchasePlaces_invalid_points_input(setup):
    flask_app = app.test_client()

    competition = setup[1]
    club = setup[0]

    response = flask_app.post(
        "/purchasePlaces",
        data={
            "places": -1,
            "club": club[1]["name"],
            "competition": competition[1]["name"],
        },
    )
    assert response.status_code == 403


def test_purchasePlaces_failed_more_than_allowed(setup):
    flask_app = app.test_client()

    competition = setup[1]
    club = setup[0]

    response = flask_app.post(
        "/purchasePlaces",
        data={
            "places": 14,
            "club": club[0]["name"],
            "competition": competition[1]["name"],
        },
    )
    assert response.status_code == 403


def test_purchasePlaces_failed_previous_competition(setup):
    flask_app = app.test_client()

    competition = setup[1]
    club = setup[0]

    response = flask_app.post(
        "/purchasePlaces",
        data={
            "places": 2,
            "club": club[0]["name"],
            "competition": competition[2]["name"],
        },
    )
    assert response.status_code == 403
