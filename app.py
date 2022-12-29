# A webapp to log my workouts
# Includes pages with workouts, goals, progress, lifting cues/tips

import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from datetime import datetime


# Configure application
app = Flask(__name__)

# Configure session
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

'''
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response
'''

# Configure CS50 Library to use SQLite database
uri = os.getenv("DATABASE_URL")
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://")
db = SQL(uri)

'''
SQL table:

CREATE TABLE workouts
(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
exercise TEXT NOT NULL,
weight NUMERIC NOT NULL,
feedback TEXT NOT NULL,
day NUMERIC NOT NULL,
date TEXT NOT NULL);

CREATE TABLE bodyweight
(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
weight NUMERIC NOT NULL,
date TEXT NOT NULL);

CREATE TABLE graph
(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
exercise TEXT NOT NULL);
'''


# Load goals page
@app.route("/goals", methods=["GET", "POST"])
def goals():
    if request.method == "POST":
        # Get bodyweight and date and save into table
        bodyweight = request.form.get("bodyweight")
        date = datetime.today().strftime("%Y-%m-%d")
        if bodyweight is not None:
            db.execute("DELETE FROM bodyweight WHERE date = ?", date)
            db.execute("INSERT INTO bodyweight (weight,date) VALUES(?,?)", bodyweight,date)

        # Get exercise and save into session
        exercise1 = request.form.get("exercise")
        if exercise1 is not None:
            session['exercise'] = exercise1
        #db.execute("INSERT INTO graph (exercise) VALUES(?)", exercise)

    # If session is empty, display bodyweight
    if session['exercise'] is None:
        session['exercise'] = "Bodyweight"

    # Remember the last exercise that was requested to check progress for
    exercise = session['exercise']
    #exercise = db.execute("SELECT exercise FROM graph ORDER BY id DESC")[0]["exercise"]

    # Load last inputted bodyweight
    if len(db.execute("SELECT weight FROM bodyweight ORDER BY id DESC LIMIT 1")) > 0:
        bodyweight = db.execute("SELECT weight FROM bodyweight ORDER BY id DESC LIMIT 1")[0]["weight"]
    else:
        bodyweight = None

    # Get data for date and weight history of selected exercise (or for bodyweight)
    if exercise == "Bodyweight":
        data = db.execute("SELECT date, weight FROM bodyweight ORDER BY date")
    else:
        data = db.execute("SELECT date, weight FROM workouts WHERE exercise=? ORDER BY date", exercise)

    weights = []
    dates = []
    for i in range(len(data)):
        weights.append(data[i]["weight"])
        if i == 0:
            date = str(data[i]["date"])
        else:
            date = str(data[i]["date"])[-5:]
        dates.append(date)

    # Get a list of all exercises to be able to be selected in the graph
    options = db.execute("SELECT DISTINCT exercise FROM workouts ORDER BY exercise")
    '''
    link = url_for("goals") + "#myChart"
    return redirect(link)
    '''

    return render_template("goals.html", bodyweight=bodyweight, exercise=exercise, options=options, dates=dates, weights=weights)


# Load best lifts page
@app.route("/bestlifts")
def bestlifts():
    return render_template("bestlifts.html")


# Load squat lifting cues page
@app.route("/squat")
def squat():
    return render_template("squat.html")


# Load benchpress lifting cues page
@app.route("/bench")
def bench():
    return render_template("bench.html")


# Load deadlift lifting cues page
@app.route("/deadlift")
def deadlift():
    return render_template("deadlift.html")


# Load OHP lifting cues page
@app.route("/ohp")
def ohp():
    return render_template("ohp.html")


#############################
#        Workout pages      #
#############################

# Load workout 1 page
@app.route("/workout1", methods=["GET", "POST"])
def workout1():
    # Get current date and day of the week
    date = datetime.today().strftime("%Y-%m-%d")
    day = 0

    if request.method == "POST":
        day=0
        # Get form data
        exercises = request.form.getlist("exercise")
        weights = request.form.getlist("weight")
        feedback = request.form.getlist("feedback")

        # Delete previous entries of today, if there are any
        db.execute("DELETE FROM workouts WHERE date = ?", date)

        # Insert workout data in sql table
        for i in range(len(exercises)):
            db.execute("INSERT INTO workouts (exercise, weight, feedback, day, date) VALUES(?,?,?,?,?)", exercises[i], weights[i], feedback, day, date)


    # Check if previous entries exist
    if len(db.execute("SELECT weight FROM workouts WHERE day = ?", day)) > 0:

        # Set number of exercises
        n = 5

        # Load weights
        workout = db.execute("SELECT weight FROM workouts WHERE day = ? ORDER BY id DESC LIMIT ?", day, n)

        # Get feedback from last week
        feedback = db.execute("SELECT feedback FROM workouts WHERE day = ? AND NOT date = ? ORDER BY id DESC LIMIT 1", day, date)[0]["feedback"]

        # Display "workout" page
        return render_template("workout1.html", feedback=feedback, weight1=workout[n-1]["weight"], weight2=workout[n-2]["weight"], weight3=workout[n-3]["weight"], weight4=workout[n-4]["weight"], weight5=workout[n-5]["weight"])

    # Display empty "workout" page
    else:
        return render_template("workout1.html")


# Load workout 2 page
@app.route("/workout2", methods=["GET", "POST"])
def workout2():
    # Get current date and day of the week
    date = datetime.today().strftime("%Y-%m-%d")
    day = 1
    if request.method == "POST":
        # Get form data
        exercises = request.form.getlist("exercise")
        weights = request.form.getlist("weight")
        feedback = request.form.getlist("feedback")

        # Delete previous entries of today, if there are any
        db.execute("DELETE FROM workouts WHERE date = ?", date)

        # Insert workout data in sql table
        for i in range(len(exercises)):
            db.execute("INSERT INTO workouts (exercise, weight, feedback, day, date) VALUES(?,?,?,?,?)", exercises[i], weights[i], feedback, day, date)

    # Check if previous entries exist
    if len(db.execute("SELECT weight FROM workouts WHERE day = ?", day)) > 0:
        # Set number of exercises
        n = 5

        # Load weights
        workout = db.execute("SELECT weight FROM workouts WHERE day = ? ORDER BY id DESC LIMIT ?", day, n)

        # Get feedback from last week
        feedback = db.execute("SELECT feedback FROM workouts WHERE day = ? AND NOT date = ? ORDER BY id DESC LIMIT 1", day, date)[0]["feedback"]

        # Display "workout" page
        return render_template("workout2.html", feedback=feedback, weight1=workout[n-1]["weight"], weight2=workout[n-2]["weight"], weight3=workout[n-3]["weight"], weight4=workout[n-4]["weight"], weight5=workout[n-5]["weight"])

    # Display empty "workout" page
    else:
        return render_template("workout2.html")


# Load workout 3 page
@app.route("/workout3", methods=["GET", "POST"])
def workout3():
    # Get current date and day of the week
    date = datetime.today().strftime("%Y-%m-%d")
    day = 2

    if request.method == "POST":
        # Get form data
        exercises = request.form.getlist("exercise")
        weights = request.form.getlist("weight")
        feedback = request.form.getlist("feedback")

        # Delete previous entries of today, if there are any
        db.execute("DELETE FROM workouts WHERE date = ?", date)

        # Insert workout data in sql table
        for i in range(len(exercises)):
            db.execute("INSERT INTO workouts (exercise, weight, feedback, day, date) VALUES(?,?,?,?,?)", exercises[i], weights[i], feedback, day, date)

    # Check if previous entries exist
    if len(db.execute("SELECT weight FROM workouts WHERE day = ?", day)) > 0:
        # Set number of exercises
        n = 5

        # Load weights
        workout = db.execute("SELECT weight FROM workouts WHERE day = ? ORDER BY id DESC LIMIT ?", day, n)

        # Get feedback from last week
        feedback = db.execute("SELECT feedback FROM workouts WHERE day = ? AND NOT date = ? ORDER BY id DESC LIMIT 1", day, date)[0]["feedback"]

        # Display "workout" page
        return render_template("workout3.html", feedback=feedback, weight1=workout[n-1]["weight"], weight2=workout[n-2]["weight"], weight3=workout[n-3]["weight"], weight4=workout[n-4]["weight"], weight5=workout[n-5]["weight"])

    # Display empty "workout" page
    else:
        return render_template("workout3.html")


# Load workout 4 page
@app.route("/workout4", methods=["GET", "POST"])
def workout4():
    # Get current date and day of the week
    date = datetime.today().strftime("%Y-%m-%d")
    day = 4

    if request.method == "POST":
        # Get form data
        exercises = request.form.getlist("exercise")
        weights = request.form.getlist("weight")
        feedback = request.form.get("feedback1") + request.form.get("feedback2")

        # Delete previous entries of today, if there are any
        db.execute("DELETE FROM workouts WHERE date = ?", date)

        # Insert workout data in sql table
        for i in range(len(exercises)):
            db.execute("INSERT INTO workouts (exercise, weight, feedback, day, date) VALUES(?,?,?,?,?)", exercises[i], weights[i], feedback, day, date)


    # Check if previous entries exist
    if len(db.execute("SELECT weight FROM workouts WHERE day = ?", day)) > 0:
        # Set number of exercises
        n = 3

        # Load weights
        workout = db.execute("SELECT weight FROM workouts WHERE day = ? ORDER BY id DESC LIMIT ?", day, n)

        # Get feedback from last week
        feedback = db.execute("SELECT feedback FROM workouts WHERE day = ? AND NOT date = ? ORDER BY id DESC LIMIT 1", day, date)[0]["feedback"]
        feedback1 = feedback[0]
        feedback2 = feedback[1]

        # Display "workout" page
        return render_template("workout4.html", feedback1=feedback1, feedback2=feedback2, weight1=workout[n-1]["weight"], weight2=workout[n-2]["weight"], weight3=workout[n-3]["weight"])

    # Display empty "workout" page
    else:
        return render_template("workout4.html")


# Load workout 5 page
@app.route("/workout5", methods=["GET", "POST"])
def workout5():
    # Get current date and day of the week
    date = datetime.today().strftime("%Y-%m-%d")
    day = 5

    if request.method == "POST":
        # Get form data
        exercises = request.form.getlist("exercise")
        weights = request.form.getlist("weight")
        feedback = request.form.getlist("feedback")

        # Delete previous entries of today, if there are any
        db.execute("DELETE FROM workouts WHERE date = ?", date)

        # Insert workout data in sql table
        for i in range(len(exercises)):
            db.execute("INSERT INTO workouts (exercise, weight, feedback, day, date) VALUES(?,?,?,?,?)", exercises[i], weights[i], feedback, day, date)

    # Check if previous entries exist
    if len(db.execute("SELECT weight FROM workouts WHERE day = ?", day)) > 0:
        # Set number of exercises
        n = 6

        # Load weights
        workout = db.execute("SELECT weight FROM workouts WHERE day = ? ORDER BY id DESC LIMIT ?", day, n)

        # Get feedback from last week
        feedback = db.execute("SELECT feedback FROM workouts WHERE day = ? AND NOT date = ? ORDER BY id DESC LIMIT 1", day, date)[0]["feedback"]

        # Display "workout" page
        return render_template("workout5.html", feedback=feedback, weight1=workout[n-1]["weight"], weight2=workout[n-2]["weight"], weight3=workout[n-3]["weight"], weight4=workout[n-4]["weight"], weight5=workout[n-5]["weight"], weight6=workout[n-6]["weight"])

    # Display empty "workout" page
    else:
        return render_template("workout5.html")

# Load main page
@app.route("/")
def workout():
    # Show today's workout based on the current day of the week
    day = datetime.today().weekday()

    if day == 0:
        if len(db.execute("SELECT weight FROM workouts WHERE day = ?", day)) > 0:
            # Get current date
            date = datetime.today().strftime("%Y-%m-%d")
            n = 5

            # Load weights
            workout = db.execute("SELECT weight FROM workouts WHERE day = ? ORDER BY id DESC LIMIT ?", day, n)

            # Get feedback from last week
            feedback = db.execute("SELECT feedback FROM workouts WHERE day = ? AND NOT date = ? ORDER BY id DESC LIMIT 1", day, date)[0]["feedback"]

            # Display "workout" page
            return render_template("workout1.html", feedback=feedback, weight1=workout[n-1]["weight"], weight2=workout[n-2]["weight"], weight3=workout[n-3]["weight"], weight4=workout[n-4]["weight"], weight5=workout[n-5]["weight"])
        # Display empty "workout" page
        else:
            return render_template("workout1.html")
    elif day == 1:
        if len(db.execute("SELECT weight FROM workouts WHERE day = ?", day)) > 0:
            # Get current date
            date = datetime.today().strftime("%Y-%m-%d")
            n = 5

            # Load weights
            workout = db.execute("SELECT weight FROM workouts WHERE day = ? ORDER BY id DESC LIMIT ?", day, n)

            # Get feedback from last week
            feedback = db.execute("SELECT feedback FROM workouts WHERE day = ? AND NOT date = ? ORDER BY id DESC LIMIT 1", day, date)[0]["feedback"]

            # Display "workout" page
            return render_template("workout2.html", feedback=feedback, weight1=workout[n-1]["weight"], weight2=workout[n-2]["weight"], weight3=workout[n-3]["weight"], weight4=workout[n-4]["weight"], weight5=workout[n-5]["weight"])
        # Display empty "workout" page
        else:
            return render_template("workout2.html")
    elif day == 2:
        if len(db.execute("SELECT weight FROM workouts WHERE day = ?", day)) > 0:
            # Get current date
            date = datetime.today().strftime("%Y-%m-%d")
            n = 5

            # Load weights
            workout = db.execute("SELECT weight FROM workouts WHERE day = ? ORDER BY id DESC LIMIT ?", day, n)

            # Get feedback from last week
            feedback = db.execute("SELECT feedback FROM workouts WHERE day = ? AND NOT date = ? ORDER BY id DESC LIMIT 1", day, date)[0]["feedback"]

            # Display "workout" page
            return render_template("workout3.html", feedback=feedback, weight1=workout[n-1]["weight"], weight2=workout[n-2]["weight"], weight3=workout[n-3]["weight"], weight4=workout[n-4]["weight"], weight5=workout[n-5]["weight"])
        # Display empty "workout" page
        else:
            return render_template("workout3.html")
    elif day == 4:
        if len(db.execute("SELECT weight FROM workouts WHERE day = ?", day)) > 0:
            # Get current date
            date = datetime.today().strftime("%Y-%m-%d")
            n = 3

            # Load weights
            workout = db.execute("SELECT weight FROM workouts WHERE day = ? ORDER BY id DESC LIMIT ?", day, n)

            # Get feedback from last week
            feedback = db.execute("SELECT feedback FROM workouts WHERE day = ? AND NOT date = ? ORDER BY id DESC LIMIT 1", day, date)[0]["feedback"]
            feedback1 = feedback[0]
            feedback2 = feedback[1]

            # Display "workout" page
            return render_template("workout4.html", feedback1=feedback1, feedback2=feedback2, weight1=workout[n-1]["weight"], weight2=workout[n-2]["weight"], weight3=workout[n-3]["weight"])
        # Display empty "workout" page
        else:
            return render_template("workout4.html")
    elif day == 5:
        if len(db.execute("SELECT weight FROM workouts WHERE day = ?", day)) > 0:
            # Get current date
            date = datetime.today().strftime("%Y-%m-%d")
            n = 6

            # Load weights
            workout = db.execute("SELECT weight FROM workouts WHERE day = ? ORDER BY id DESC LIMIT ?", day, n)

            # Get feedback from last week
            feedback = db.execute("SELECT feedback FROM workouts WHERE day = ? AND NOT date = ? ORDER BY id DESC LIMIT 1", day, date)[0]["feedback"]

            # Display "workout" page
            return render_template("workout5.html", feedback=feedback, weight1=workout[n-1]["weight"], weight2=workout[n-2]["weight"], weight3=workout[n-3]["weight"], weight4=workout[n-4]["weight"], weight5=workout[n-5]["weight"], weight6=workout[n-6]["weight"])
        # Display empty "workout" page
        else:
            return render_template("workout5.html")
    # Return "noworkout" page
    else:
        return render_template("noworkout.html")