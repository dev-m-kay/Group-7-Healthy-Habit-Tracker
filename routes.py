import psycopg2
from flask import Flask, render_template, request, redirect
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

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
app.secret_key = 'your_secret_key'
#initialize Login Manager
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash

@login_manager.user_loader
def load_user(user_id):
    conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres", password="password", port=5432)
    cur = conn.cursor()
    cur.execute('SELECT * FROM habits.users WHERE id = %s', (user_id,))
    user_data = cur.fetchone()
    conn.close()

    if user_data:
        return User(id=user_data[0], username=user_data[1], password_hash=user_data[2])
    return None

@app.route("/")
@login_required
def index():
    return render_template("home.html",user= current_user.username)
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

@app.route("/insertworkout",methods = ["POST"])
def insertworkout():
    if request.method == 'POST':
        date = request.form.get('date')
        name = request.form.get('name')
        duration = request.form.get('duration')
        intensity = request.form.get('intensity')
        type = request.form.get('type')
        rating = request.form.get('rating')
        notes = request.form.get('notes')
        user = request.form.get('user')

        conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres", password="password", port=5432)
        cur = conn.cursor()

        cur.execute("""INSERT INTO
                            habits.workout (
                                workout_name,
                                workout_date,
                                workout_duration,
                                workout_intensity,
                                workout_type,
                                workout_log,
                                workout_rating,
                                user_detail_id
                            )
                        VALUES (
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s);
        """,(name,date,duration,intensity,type,notes,rating,user))
        conn.commit()

        cur.close()
        conn.close()
    return redirect("/workout")

@app.route("/insertsleep",methods = ["POST"])
def insertsleep():
    if request.method == 'POST':
        date = request.form.get('date')
        duration = request.form.get('duration')
        rating = request.form.get('rating')
        notes = request.form.get('notes')
        user = request.form.get('user')

        conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres", password="password", port=5432)
        cur = conn.cursor()

        cur.execute("""INSERT INTO
                            habits.sleep (
                                sleep_duration,
                                sleep_date,
                                sleep_log,
                                sleep_rating,
                                user_detail_id
                            )
                        VALUES (
                                %s,
                                %s,
                                %s,
                                %s,
                                %s);
""",(duration,date,notes,rating,user))
        conn.commit()

        cur.close()
        conn.close()
    return redirect("/sleep")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres", password="password", port=5432)
        cur = conn.cursor()
        cur.execute('SELECT * FROM habits.users WHERE username = %s', (username,))
        user_data = cur.fetchone()
        conn.close()
        if user_data and check_password_hash(user_data[2], password):
            user = User(id=user_data[0], username=user_data[1], password_hash=user_data[2])
            login_user(user)
            return redirect('/')
        else:
            return render_template('login.html', error="Incorrect username or password")
    return render_template('login.html')

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_hash = generate_password_hash(password)

        # Check if the username already exists
        conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres", password="password", port=5432)
        cur = conn.cursor()
        cur.execute('SELECT * FROM habits.users WHERE username = %s', (username,))
        existing_user = cur.fetchone()
        if existing_user:
            return render_template('signup.html', error='Username taken!')

        # Insert the new user into the database
        cur.execute('INSERT INTO habits.users (username, password_hash) VALUES (%s, %s)', (username, password_hash))
        conn.commit()
        conn.close()

        return redirect('/login')

    return render_template('signup.html')

@app.route("/sleep", methods=["GET"])
@login_required
def sleep():
    sleep_data = get_data("habits.sleep")
    return render_template("sleep.html", sleep_data=sleep_data, user= current_user.username)

@app.route("/diet", methods=["GET"])
@login_required
def diet():
    diet_data = get_data("habits.diet")
    return render_template("diet.html", diet_data=diet_data, user= current_user.username)

@app.route("/workout", methods=["GET"])
@login_required
def workout():
    workout_data = get_data("habits.workout")
    return render_template("workout.html", workout_data=workout_data,user= current_user.username)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"),500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=11596)
