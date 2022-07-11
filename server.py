from datetime import datetime
import json
from flask import Flask, render_template, request, redirect, flash, url_for


def loadClubs():
    with open("clubs.json") as c:
        listOfClubs = json.load(c)["clubs"]
        return listOfClubs


def loadCompetitions():
    with open("competitions.json") as comps:
        listOfCompetitions = json.load(comps)["competitions"]
        return listOfCompetitions


app = Flask(__name__)
app.secret_key = "something_special"

competitions = loadCompetitions()
clubs = loadClubs()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/showSummary", methods=["POST"])
def showSummary():
    if request.form["email"] == "":
        flash("The email address field is empty. Please enter your email address.")
        return render_template("index.html"), 401

    club = [club for club in clubs if club["email"] == request.form["email"]]

    if club:
        return render_template("welcome.html", club=club[0], competitions=competitions)
    else:
        flash("The entered email address does not exist in our database.")

    return render_template("index.html"), 401


@app.route("/book/<competition>/<club>")
def book(competition, club):
    foundClub = [c for c in clubs if c["name"] == club]
    foundCompetition = [c for c in competitions if c["name"] == competition]
    if foundClub and foundCompetition:
        if (
            datetime.strptime(foundCompetition[0]["date"], "%Y-%m-%d %H:%M:%S")
            < datetime.now()
        ):
            flash("The competition is in the past.")
            return (
                render_template(
                    "welcome.html", club=foundClub[0], competitions=competitions
                ),
                403,
            )
        return render_template(
            "booking.html", club=foundClub[0], competition=foundCompetition[0]
        )
    else:
        flash("Something went wrong-please try again")
        return (
            render_template("welcome.html", club=club, competitions=competitions),
            403,
        )


@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    competition = [c for c in competitions if c["name"] == request.form["competition"]][
        0
    ]
    club = [c for c in clubs if c["name"] == request.form["club"]][0]

    try:
        placesRequired = int(request.form["places"])
    except ValueError:
        flash("You need to enter a number of places!")
        return (
            render_template("welcome.html", club=club, competitions=competitions),
            403,
        )
    if 3 * placesRequired > int(club["points"]):
        flash("You don't have enough points!")
        return (
            render_template("welcome.html", club=club, competitions=competitions),
            403,
        )
    elif placesRequired <= 0:
        flash("That is an invalid amount of places!")
        return (
            render_template("welcome.html", club=club, competitions=competitions),
            403,
        )
    elif placesRequired > 12:
        flash("You are not allowed to book more than 12 places!")
        return (
            render_template("welcome.html", club=club, competitions=competitions),
            403,
        )
    elif datetime.strptime(competition["date"], "%Y-%m-%d %H:%M:%S") < datetime.now():
        flash("The competition is in the past.")
        return (
            render_template("welcome.html", club=club, competitions=competitions),
            403,
        )
    elif placesRequired > int(competition["numberOfPlaces"]):
        flash("There are not enough places available.")
        return (
            render_template("welcome.html", club=club, competitions=competitions),
            403,
        )
    else:
        competition["numberOfPlaces"] = (
            int(competition["numberOfPlaces"]) - placesRequired
        )
        flash("Great-booking complete!")
        club["points"] = int(club["points"]) - 3 * placesRequired
        return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/overview")
def overviewClubs():
    return render_template("overview.html", clubs=clubs)


@app.route("/logout")
def logout():
    return redirect(url_for("index"))
