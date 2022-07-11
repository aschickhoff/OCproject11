import pytest
import server


@pytest.fixture
def setup():
    server.clubs = [
        {
            "name": "Copper Temple",
            "email": "admin@coppertemple.com",
            "points": "23",
        },
        {
            "name": "Carbon Temple",
            "email": "admin@carbontemple.com",
            "points": "10",
        },
    ]
    server.competitions = [
        {
            "name": "Spring Festival",
            "date": "2025-03-27 10:00:00",
            "numberOfPlaces": "9",
        },
        {
            "name": "Autumn Festival",
            "date": "2025-10-27 10:00:00",
            "numberOfPlaces": "26",
        },
        {
            "name": "Winter Festival",
            "date": "2020-12-27 10:00:00",
            "numberOfPlaces": "3",
        },
    ]
    invalid_email = "user@bronzetemple.com"
    yield server.clubs, server.competitions, invalid_email
    server.clubs = server.loadClubs()
    server.competitions = server.loadCompetitions()
    invalid_email = None
