import psycopg2
from flask import Flask, render_template, request, redirect

conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres", password="password", port=5432)

cur = conn.cursor()

cur.execute(open("static/db/delete.sql", "r").read())
cur.execute(open("static/db/create.sql", "r").read())
cur.execute(open("static/db/insert.sql", "r").read())

conn.commit()

cur.close()
conn.close()
#initializes data for testing purposes, will be removed before final release

def get_data(table_name):
    conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres" ,password="password", port=5432)

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
@app.route("/insertdiet",methods = ["POST"])
def insertdiet():
    if request.method == 'POST':
        date = request.form.get('date')
        user = request.form.get('user')
        rating = request.form.get('rating')
        mealname = request.form.get('mealname')
        mealnotes=request.form.get('notes')

        conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres", password="password", port=5432)
        cur = conn.cursor()

        cur.execute("""INSERT INTO habits.diet (
                                diet_name,
                                diet_date,
                                diet_log,
                                diet_rating,
                                user_detail_id
                            )
                        VALUES (
                                %s,
                                %s,
                                %s,
                                %s,
                                %s);
        """,(mealname,date,mealnotes,rating,user))
        conn.commit()

        cur.close()
        conn.close()
    return redirect("/diet")


@app.route("/input")
def input():
    return render_template("input.html")

@app.route("/sleep", methods=["GET"])
def sleep():
    sleep_data = get_data("habits.sleep")
    return render_template("sleep.html", sleep_data=sleep_data)

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
