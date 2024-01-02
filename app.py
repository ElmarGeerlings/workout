# A webapp to log my workouts
# Includes pages with workouts, goals, progress, lifting cues/tips

import os

import psycopg2

from cs50 import SQL
from flask import Flask, render_template, request, session
from flask_session import Session
from datetime import datetime

# Configure application
app = Flask(__name__)

# Configure session
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Configure CS50 Library to use SQLite database

uri = "postgres://workouts_8sdm_user:wLJUvQkB6RtzzNpKHjeEChoUqxF5SYRu@dpg-cm9te0ed3nmc73b8j8u0-a.frankfurt-postgres.render.com/workouts_8sdm"
#uri = os.getenv(url)
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://")

db = SQL(uri)


'''
conn = psycopg2.connect(
        host="dpg-ck0o9mu3ktkc738padr0-a",
        database="exercises_7g9i",
        user='exercises_7g9i_user',
        password='AkBujg6hJTVUnxPHU9QdoNld6c8YiOPB')

# Open a cursor to perform database operations
db = conn.cursor()
'''

'''
SQL tables:

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

    # If session is empty, display bodyweight progress
    if not session.get('exercise'):
        session['exercise'] = "Bodyweight"

    # Remember the last exercise that was requested to check progress for
    exercise = session['exercise']

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
        try:
            feedback = db.execute("SELECT feedback FROM workouts WHERE day = ? ORDER BY id DESC LIMIT ?", day, n+1)[n]["feedback"]
        except:
            feedback = "  "

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
    date = '2023-09-09'
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
        try:
            feedback = db.execute("SELECT feedback FROM workouts WHERE day = ? ORDER BY id DESC LIMIT ?", day, n+1)[n]["feedback"]
        except:
            feedback = "  "

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
        try:
            feedback = db.execute("SELECT feedback FROM workouts WHERE day = ? ORDER BY id DESC LIMIT ?", day, n+1)[n]["feedback"]
        except:
            feedback = "  "

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
        try:
            feedback = db.execute("SELECT feedback FROM workouts WHERE day = ? ORDER BY id DESC LIMIT ?", day, n+1)[n]["feedback"]
        except:
            feedback = "  "
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
        try:
            feedback = db.execute("SELECT feedback FROM workouts WHERE day = ? ORDER BY id DESC LIMIT ?", day, n+1)[n]["feedback"]
        except:
            feedback = "  "

        # Display "workout" page
        return render_template("workout5.html", feedback=feedback, weight1=workout[n-1]["weight"], weight2=workout[n-2]["weight"], weight3=workout[n-3]["weight"], weight4=workout[n-4]["weight"], weight5=workout[n-5]["weight"], weight6=workout[n-6]["weight"])

    # Display empty "workout" page
    else:
        return render_template("workout5.html")

# Load main page
@app.route("/")
def workout():
    # Initiate SQL tables if they don't yet exist
    db.execute("CREATE TABLE IF NOT EXISTS workouts(id SERIAL PRIMARY KEY NOT NULL,exercise TEXT NOT NULL,weight NUMERIC NOT NULL,feedback TEXT NOT NULL,day NUMERIC NOT NULL,date TEXT NOT NULL)")
    db.execute("CREATE TABLE IF NOT EXISTS bodyweight(id SERIAL PRIMARY KEY NOT NULL,weight NUMERIC NOT NULL,date TEXT NOT NULL)")
    db.execute("CREATE TABLE IF NOT EXISTS graph(id SERIAL PRIMARY KEY NOT NULL,exercise TEXT NOT NULL)")

    # Show today's workout based on the current day of the week
    day = datetime.today().weekday()

    # Load weights
    n = [5, 5, 5, 0, 3, 6, 0][day]
    if n > 0:
        workout = db.execute("SELECT weight FROM workouts WHERE day = ? ORDER BY id DESC LIMIT ?", day, n)
        if n > 0:
            for i in range(n):
                workout.append({"weight": 0})

    # Get feedback from last week
    try:
        feedback = db.execute("SELECT feedback FROM workouts WHERE day = ? ORDER BY id DESC LIMIT ?", day, n+1)[n]["feedback"]
    except:
        feedback = "  "

    if day == 0:
        # Number of exercises
        n = 5

        # Display "workout" page
        return render_template("workout1.html", feedback=feedback, weight1=workout[n-1]["weight"], weight2=workout[n-2]["weight"], weight3=workout[n-3]["weight"], weight4=workout[n-4]["weight"], weight5=workout[n-5]["weight"])
    elif day == 1:
        # Number of exercises
        n = 5

        # Display "workout" page
        return render_template("workout2.html", feedback=feedback, weight1=workout[n-1]["weight"], weight2=workout[n-2]["weight"], weight3=workout[n-3]["weight"], weight4=workout[n-4]["weight"], weight5=workout[n-5]["weight"])
    elif day == 2:
        # Number of exercises
        n = 5

        # Display "workout" page
        return render_template("workout3.html", feedback=feedback, weight1=workout[n-1]["weight"], weight2=workout[n-2]["weight"], weight3=workout[n-3]["weight"], weight4=workout[n-4]["weight"], weight5=workout[n-5]["weight"])
    elif day == 4:
        # Number of exercises
        n = 3

        feedback1 = feedback[0]
        feedback2 = feedback[1]

        # Display "workout" page
        return render_template("workout4.html", feedback1=feedback1, feedback2=feedback2, weight1=workout[n-1]["weight"], weight2=workout[n-2]["weight"], weight3=workout[n-3]["weight"])
    elif day == 5:
        # Number of exercises
        n = 6

        # Display "workout" page
        return render_template("workout5.html", feedback=feedback, weight1=workout[n-1]["weight"], weight2=workout[n-2]["weight"], weight3=workout[n-3]["weight"], weight4=workout[n-4]["weight"], weight5=workout[n-5]["weight"], weight6=workout[n-6]["weight"])
    # Return "noworkout" page
    else:
        return render_template("noworkout.html")

if __name__ == '__main__':
 app.debug = True
 port = int(os.environ.get('PORT', 5000))
 app.run(host='0.0.0.0', port=port)
