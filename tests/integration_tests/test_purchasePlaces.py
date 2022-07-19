from server import app


def test_purchasePlaces_points_deducted(setup):
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
    assert b"Points available: 17" in response.data


def test_purchasePlaces_places_deducted(setup):
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
    assert b"Number of Places: 7" in response.data


def test_purchasePlaces_not_enough_places(setup):
    flask_app = app.test_client()

    competition = setup[1]
    club = setup[0]

    response = flask_app.post(
        "/purchasePlaces",
        data={
            "places": 10,
            "club": club[2]["name"],
            "competition": competition[0]["name"],
        },
    )
    assert b"Number of Places: 9" in response.data
    assert b"Points available: 100" in response.data
    assert b"There are not enough places available." in response.data


def test_purchasePlaces_not_enough_points(setup):
    flask_app = app.test_client()

    competition = setup[1]
    club = setup[0]

    response = flask_app.post(
        "/purchasePlaces",
        data={
            "places": 10,
            "club": club[1]["name"],
            "competition": competition[0]["name"],
        },
    )
    assert b"Number of Places: 9" in response.data
    assert b"Points available: 10" in response.data
