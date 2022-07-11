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
