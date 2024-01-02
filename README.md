# Elmar workout by Elmar Geerlings

#### Video Demo:  https://youtu.be/GVOlQa4heuQ
#### Website Link: https://elmarworkout.herokuapp.com/


#### Short description:
A webapp to log my workouts.
Includes pages with workouts, goals, progress, lifting cues/tips
The app is deployed on heroku, using the CS50 tutorial: https://cs50.readthedocs.io/heroku/


#### Long description (of every page):
The webapp is written in the python file "app.py" and uses flask.
It uses a SQL database named "workouts.db" to log weights for exercises and bodyweight.
The exercise table includes ID, exercise, weight, feedback, day(of the week) and date.
The bodyweight table includes ID, weight and date.
The code for the webpages is written in html templates, which are all extended from "layout.html".
Bootstrap is used for the header.
Most things are styled using a CSS file "styles.css" in the "static" folder
Static folder also includes videos of some of my best lifts.

# Today's workout
This is the homepage of the app, where the user will first land.
Displays a different workout depending on the current day of the week.
Displays a "no workout" page on days when I don't work out.

For every exercise I can submit the weight that I lifted.
For some exercises I can submit a feedback on whether I want to go up in weight next week,
where "+" means go up in weight, "=" means stay at the same weight, "-" means go down in weight.
This given feedback will then be shown the next week.
All this data will be saved in an SQL table, where the last submitted weights are shown on the page.
If multiple submissions are done in a day, only the last one will remain.

# Goals & Progress
An inspirational quote (by Mark Bell) at the top of the page.
The "Goals" section shows my lifting goals for the next couple of months.
The "Bodyweight" section makes me able to log my bodyweight.

In the "Progress" section I can choose an exercise (or my bodyweight) to show a progress graph of.
On the vertical axis it will show the weight (in KG) and on the horizontal axis the date(Month-Day).
It will remember what exercise is chosen (using flask session) for the next time this page is visited.
If no exercise is chosen yet, bodyweight will be displayed.

# Best Lifts
A page where I show some of the lifts (Squat, Bench, Deadlift) where I am most proud of.

# All Workouts
These are the same pages that will be displayed on the "Today's workout" page.
This just makes it able to navigate to every workout, independent of the current day of the week.
It has the same functionality as it would have been displayed on "Today's workout" page;
I can submit weight and feedback for the exercises via here as well.

# Lifting Cues
There's a page for every main lift: Bench Press, Squat, Deadlift, OHP.
It shows some tips or pointers that I should be aware of and will help me while lifting.
It also shows a youtube video that I found particularly helpful for the lift.
