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
    club = [club for club in clubs if club["email"] == request.form["email"]][0]
    return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/book/<competition>/<club>")
def book(competition, club):
    foundClub = [c for c in clubs if c["name"] == club]
    foundCompetition = [c for c in competitions if c["name"] == competition]
    if foundClub and foundCompetition:
        return render_template(
            "booking.html", club=foundClub[0], competition=foundCompetition[0]
        )
    else:
        flash("Something went wrong-please try again")
        return render_template("welcome.html", club=club, competitions=competitions)


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
    else:
        competition["numberOfPlaces"] = (
            int(competition["numberOfPlaces"]) - placesRequired
        )
        flash("Great-booking complete!")
        return render_template("welcome.html", club=club, competitions=competitions)


# TODO: Add route for points display


@app.route("/logout")
def logout():
    return redirect(url_for("index"))
