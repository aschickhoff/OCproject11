from locust import HttpUser, task, between
from server import loadClubs, loadCompetitions


class LocustServerClient(HttpUser):
    wait_time = between(1, 5)
    club = loadClubs()[3]
    competition = loadCompetitions()[3]

    def on_start(self):
        self.client.get("/")

    @task
    def loadClubs(self):
        self.club = loadClubs()[3]

    @task
    def loadCompetitions(self):
        self.competition = loadCompetitions()[3]

    @task
    def showSummary(self):
        self.client.post("/showSummary", data={"email": self.club["email"]})

    @task()
    def book(self):
        self.client.get(f"/book/{self.competition['name']}/{self.club['name']}")

    @task
    def purchasePlaces(self):
        self.client.post(
            "/purchasePlaces",
            data={
                "places": 1,
                "club": self.club["name"],
                "competition": self.competition["name"],
            },
        )

    @task
    def logout(self):
        self.client.get("/logout")

    @task
    def overview(self):
        self.client.get("/overview")
