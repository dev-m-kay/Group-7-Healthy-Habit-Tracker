import psycopg2
from flask import Flask, render_template, request, redirect


def get_data(table_name):
    conn = psycopg2.connect(host="localhost", dbname="habit_tracker", user="postgres" ,password="password", port=5432)

    cur = conn.cursor()

    cur.execute("SELECT * FROM {table}".format(table=table_name))
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows

def delete():
    pass
def create():
    pass

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("home.html")
@app.route("/insert",methods = ["POST"])
def insert():
    if request.method == 'POST':
        #insert into Database
        pass
    return redirect("/")

@app.route("/sleep")
def sleep():
    pass

@app.route("/workout")
def workout():
    pass

@app.route("/diet")
def diet():
    pass

@app.route("/input")
def input():
    return render_template("input.html")


@app.route("/diet", methods=["GET"])
def diet():
    diet_data = get_data("habits.diet")
    return render_template("diet.html", diet_data=diet_data)

@app.route("/workout", methods=["GET"])
def workout():
    workout_data = get_data("habits.workout")
    return render_template("workout.html", workout_data=workout_data)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html" ), 404
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html",),500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=11596)