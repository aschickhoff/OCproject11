from server import app


def test_book_upcoming_competition(setup):
    flask_app = app.test_client()

    competition = setup[1]
    club = setup[0]

    response = flask_app.get(f"/book/{competition[0]['name']}/{club[0]['name']}")
    assert response.status_code == 200
    assert b"Places available:" in response.data
    assert b"How many places?" in response.data


def test_book_previous_competition(setup):
    flask_app = app.test_client()

    competition = setup[1]
    club = setup[0]

    try:
        response = flask_app.get(f"/book/{competition[2]['name']}/{club[0]['name']}")
    except IndexError:
        assert response.status_code == 403


def test_book_upcoming_competition_wrong_club(setup):
    flask_app = app.test_client()

    competition = setup[1]

    response = flask_app.get(f"/book/{competition[0]['name']}/Clubname")
    assert response.status_code == 403
